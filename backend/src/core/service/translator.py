from dataclasses import fields
from grp import struct_group
from random import choices
from time import sleep

from loguru import logger

from django.apps import apps
from django.contrib import admin
from django.db import models, transaction
from django.db.models import Model, QuerySet
from django import forms
from modeltranslation.translator import translator, NotRegistered
from rest_framework import serializers
from sentry_sdk import capture_exception

from core.adapters.translaters import GoogleTranslator, OpenAITranslator, DeepLTranslator
from django.conf import settings

from core.celery import app, TRANSLATE_SERVICE_QUEUE

GOOGLE = 'google'
OPENAI = 'openai'
DEEPL = 'deepl'

DEFAULT_TRANSLATE_SERVICE = DEEPL

TRANSLATE_SERVICES = {
    GOOGLE: GoogleTranslator(),
    OPENAI: OpenAITranslator(),
    DEEPL: DeepLTranslator()
}


def get_model_translate_fields(model: Model) -> list:
    try:
        return translator.get_options_for_model(model).fields
    except NotRegistered:
        return []


def update_object_translate(
        obj: Model,
        translate_fields: list | tuple | None = None,
        from_lang: str = 'ru',
        translate_service: str = DEFAULT_TRANSLATE_SERVICE,
        force_update: bool = False,
) -> Model:
    if translate_fields is None:
        translate_fields = translator.get_options_for_model(obj._meta.model).fields
    update_object_translate_task.delay(
        app_label=obj._meta.app_label,
        model_name=obj._meta.model_name,
        instance_id=obj.pk,
        from_lang=from_lang,
        translate_service=translate_service,
        translate_fields=translate_fields,
        force_update=force_update,
    )
    return obj


def update_bulk_objects_translate(
        objs: QuerySet,
        translate_fields: list | tuple | None = None,
        from_lang: str = 'ru',
        translate_service: str = DEFAULT_TRANSLATE_SERVICE,
):
    for obj in objs:
        update_object_translate(obj, translate_fields, from_lang, translate_service)
    return objs


class TranslateFieldMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['translate_service'] = serializers.ChoiceField(required=False, write_only=True,
                                                                   choices=TRANSLATE_SERVICES.keys())

    def create(self, validated_data):
        translate_service = validated_data.pop('translate_service', DEFAULT_TRANSLATE_SERVICE)
        instance = super().create(validated_data)
        update_object_translate(instance, translate_fields=self.Meta.translate_fields,
                                translate_service=translate_service)
        return instance

    def update(self, instance, validated_data):
        translate_service = validated_data.pop('translate_service', DEFAULT_TRANSLATE_SERVICE)
        fields = []
        
        # Clear translations for changed fields
        for translate_field in self.Meta.translate_fields:
            if translate_field in validated_data:
                original_value = getattr(instance, translate_field)
                new_value = validated_data[translate_field]
                if original_value != new_value:
                    # Clear translations
                    for lang_code, _ in settings.LANGUAGES:
                        if lang_code != settings.MODELTRANSLATION_DEFAULT_LANGUAGE:
                            setattr(instance, f"{translate_field}_{lang_code}", None)
                    fields.append(translate_field)
        
        instance = super().update(instance, validated_data)
        
        if fields:
            update_object_translate(instance, translate_fields=fields,
                                translate_service=translate_service)
        return instance


def translate_with_retries(translator, text: str, to_lang: str, from_lang: str, max_retries: int = 3, retry_delay: int = 5) -> tuple[str | None, Exception | None]:
    """
    Attempt to translate text with retries on failure
    Returns tuple of (translation result, last error if any)
    """
    last_error = None
    
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                logger.info(f"Retry attempt {attempt + 1} for translating to {to_lang}")
                sleep(retry_delay)  # Wait before retry
                
            result = translator.translate_text(text, to_lang, from_lang)
            if result:
                return result, None
                
        except Exception as e:
            last_error = e
            logger.warning(f"Translation attempt {attempt + 1} failed: {str(e)}")
            continue
            
    return None, last_error


def is_valid_translation(text: str, translation: str) -> bool:
    """
    Проверяет качество перевода
    """
    if not translation:
        return False
        
    # Проверяем, что перевод не слишком длинный по сравнению с оригиналом
    if len(translation) > len(text) * 3:
        return False
        
    # Проверяем, что перевод не содержит оригинальный текст
    if text.lower() in translation.lower():
        return False
        
    # Проверяем, что перевод не содержит слова "translate" или "translation"
    if any(word in translation.lower() for word in ['translate', 'translation', 'переводится']):
        return False
        
    return True


@app.task(ignore_result=True, queue=TRANSLATE_SERVICE_QUEUE)
def update_object_translate_task(
        app_label: str,
        model_name: str,
        instance_id: int | str,
        translate_fields: list | tuple,
        from_lang: str = 'ru',
        translate_service: str = DEFAULT_TRANSLATE_SERVICE,
        force_update: bool = False,
        retry_count: int = 0
):
    """Задача для обновления переводов объекта

    Args:
        app_label: Метка приложения модели
        model_name: Имя модели
        instance_id: ID объекта
        translate_fields: Список полей для перевода
        from_lang: Исходный язык
        translate_service: Сервис перевода
        force_update: Принудительно обновить переводы
        retry_count: Количество попыток перевода
    """
    try:
        model = apps.get_model(app_label, model_name)
        obj = model.objects.get(pk=instance_id)
        
        logger.debug(f'Обновление перевода для {model_name} с ID {instance_id}')
        
        # Получаем список полей для перевода
        if not translate_fields:
            translate_fields = get_model_translate_fields(model)
        
        # Получаем основной и резервные переводчики
        primary_translator = TRANSLATE_SERVICES[translate_service]
        fallback_translators = [
            (service, translator) 
            for service, translator in TRANSLATE_SERVICES.items() 
            if service != translate_service
        ]
        
        update_fields = []
        
        for field in translate_fields:
            original_text = getattr(obj, field, None)
            
            # Пропускаем пустые значения
            if not original_text:
                logger.debug(f'Пропуск пустого поля {field}')
                continue
            
            for lang, _ in settings.LANGUAGES:
                if lang == from_lang:
                    continue
                
                # Получаем текущий перевод
                update_field = f'{field}_{lang}'
                current_translation = getattr(obj, update_field, None)
                
                # Проверяем необходимость обновления
                #if current_translation and not force_update:
                #    continue
                
                # Пытаемся перевести основным переводчиком
                translation, error = translate_with_retries(
                    primary_translator, 
                    original_text, 
                    lang, 
                    from_lang,
                    max_retries=3,
                    retry_delay=5
                )
                
                # Проверяем качество перевода основного переводчика
                if translation and not is_valid_translation(original_text, translation):
                    logger.warning(f"Некачественный перевод основным переводчиком {translate_service} для {field} на {lang}: {translation}")
                    translation = None
                
                # Если основной переводчик не справился, пробуем резервные
                if not translation:
                    logger.warning(f"Основной переводчик {translate_service} не справился для {field} на {lang}: {error}")
                    
                    for fallback_service, fallback_translator in fallback_translators:
                        logger.info(f"Попытка резервного переводчика {fallback_service}")
                        translation, error = translate_with_retries(
                            fallback_translator,
                            original_text,
                            lang,
                            from_lang,
                            max_retries=2,
                            retry_delay=5
                        )
                        
                        # Проверяем качество перевода резервного переводчика
                        if translation and not is_valid_translation(original_text, translation):
                            logger.warning(f"Некачественный перевод от {fallback_service} для {field} на {lang}: {translation}")
                            translation = None
                        
                        if translation:
                            logger.info(f"Успешный перевод с помощью {fallback_service}")
                            break
                
                # Сохраняем перевод, если он успешен
                if translation:
                    setattr(obj, update_field, translation)
                    update_fields.append(update_field)
                else:
                    logger.error(f"Не удалось перевести {field} на {lang} ни одним сервисом")
        
        # Сохраняем объект с обновленными переводами
        if update_fields:
            logger.debug(f'Обновление полей: {update_fields}')
            obj.save(update_fields=update_fields)
    
    except model.DoesNotExist:
        logger.warning(f'Объект {model_name} с ID {instance_id} не найден. Пропуск перевода.')
        return
    except Exception as e:
        logger.error(f"Ошибка при обновлении переводов: {str(e)}", exc_info=True)
        capture_exception(e)
        if retry_count < 3:  # Максимум 3 попытки
            # Повторяем задачу через 5 минут
            update_object_translate_task.apply_async(
                args=(app_label, model_name, instance_id, translate_fields),
                kwargs={
                    'from_lang': from_lang,
                    'translate_service': translate_service,
                    'force_update': force_update,
                    'retry_count': retry_count + 1
                },
                countdown=300  # 5 минут
            )


class TranslateFieldAdmin(admin.ModelAdmin):
    translate_fields = []
    change_form_template = 'admin/translate_change_form.html'

    def save_model(self, request, obj, form, change):
        updated_fields = []
        if change:
            original_obj = obj.__class__.objects.get(pk=obj.pk)
            for field in self.translate_fields:
                original_value = getattr(original_obj, field)
                new_value = getattr(obj, field)
                
                # Проверяем, что новое значение не пустое
                if not new_value:
                    from django.core.exceptions import ValidationError
                    raise ValidationError({field: f'Поле {field} не может быть пустым'})
                    
                if original_value != new_value:
                    # Clear translations for this field
                    for lang_code, _ in settings.LANGUAGES:
                        if lang_code != settings.MODELTRANSLATION_DEFAULT_LANGUAGE:
                            setattr(obj, f"{field}_{lang_code}", None)
                    updated_fields.append(field)
        else:
            # Для новых объектов проверяем все поля для перевода
            for field in self.translate_fields:
                value = getattr(obj, field)
                if not value:
                    from django.core.exceptions import ValidationError
                    raise ValidationError({field: f'Поле {field} не может быть пустым'})
            updated_fields = self.translate_fields
            
        super().save_model(request, obj, form, change)
        if updated_fields:
            transaction.on_commit(lambda: update_object_translate(obj, translate_fields=updated_fields))

    def save_related(self, request, form, formsets, change):
        translate_objects = []
        for formset in formsets:
            translate_fields = get_model_translate_fields(formset.model)
            if not translate_fields:
                continue
            for inline_form in formset.forms:
                inline_obj = inline_form.instance
                updated_inline_fields = []
                if inline_obj.pk:
                    original_inline_obj = inline_obj.__class__.objects.get(pk=inline_obj.pk)
                    for field in translate_fields:
                        original_value = getattr(original_inline_obj, field, None)
                        new_value = getattr(inline_obj, field, None)
                        if original_value != new_value:
                            updated_inline_fields.append(field)
                else:
                    updated_inline_fields = translate_fields
                if updated_inline_fields:
                    translate_objects.append((inline_obj, updated_inline_fields))
        super().save_related(request, form, formsets, change)

        transaction.on_commit(lambda: [
            update_object_translate(inline_obj, translate_fields=updated_inline_fields)
            for inline_obj, updated_inline_fields in translate_objects
        ])

    def response_change(self, request, obj):
        if "_force_translate" in request.POST:
            # Force update translations for all translate fields
            transaction.on_commit(
                lambda: update_object_translate(
                    obj, 
                    translate_fields=self.translate_fields,
                    force_update=True
                )
            )
            self.message_user(request, "Translation update initiated.")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)
