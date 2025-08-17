from django.contrib import admin
from django.db import models
from django.http import HttpResponseRedirect
from markdownx.widgets import AdminMarkdownxWidget

from apps.dv_info_site.models import MainPageSlider, MainPageButtonBlock, MainPageReputationLink, Retail, Contact, FAQ, \
    DVInstruction, DVInstructionRow, Vacancy, Partnership, Project, ProjectLink, City, Country, ProductUpdateFile, DVIContentFile, \
    ProductImage, Product, ProductItem, FormTemplate, FormQuestion, FormAnswerChoice, Calculator, CalcField, \
    CalcFieldChoice, FormAnswer, FormUser, BugReport, BugReportSetting, ResourcePolicy
from core.service.translator import TranslateFieldAdmin, update_object_translate
from django.db import transaction
from django.contrib import messages
from apps.dv_info_site.services.product_parsing import processing_product_update_file
from django.utils import timezone


@admin.register(MainPageSlider)
class MainPageSliderAdmin(TranslateFieldAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    fields = ('title', 'description', 'image')
    translate_fields = ('title',)


@admin.register(MainPageButtonBlock)
class MainPageButtonBlockAdmin(TranslateFieldAdmin):
    list_display = ('title', 'description', 'link', 'background_image', 'created_at', 'updated_at')
    fields = ('title', 'description', 'link', 'background_image')
    translate_fields = ('title', 'description')


@admin.register(MainPageReputationLink)
class MainPageReputationLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'link', 'created_at', 'updated_at')
    fields = ('title', 'image', 'link')
    translate_fields = ('title',)


@admin.register(Retail)
class RetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'link_type', 'created_at', 'updated_at')
    fields = ('name', 'link', 'link_type')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'department', 'person', 'person_avatar', 'element', 'telegram', 'is_telegram_active', 'session', 'created_at', 'updated_at'
    )
    fields = ('department', 'person', 'person_avatar', 'element', 'telegram','is_telegram_active', 'session')


@admin.register(FAQ)
class FAQAdmin(TranslateFieldAdmin):
    list_display = (
        'question', 'position', 'created_at', 'updated_at'
    )
    fields = ('question', 'answer', 'position', 'image')
    translate_fields = ('question', 'answer')
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }

class DVInstructionRowInline(admin.StackedInline):
    model = DVInstructionRow
    fields = ('column1_text', 'column1_image', 'column2_text', 'column2_image', 'column3_text', 'column3_image')
    extra = 1  # Количество пустых строк для добавления
    #template = 'admin/dv_info_site/dvinstruction_row_inline.html'

@admin.register(DVInstruction)
class DVInstructionAdmin(TranslateFieldAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    fields = ('title',)
    inlines = [DVInstructionRowInline]
    translate_fields = ('title',)
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }


@admin.register(Vacancy)
class VacancyAdmin(TranslateFieldAdmin):
    list_display = (
        'title', 'short_description', 'work_format', 'created_at', 'updated_at'
    )
    fields = (
        'title', 'image', 'short_description', 'description', 'salary',
        'salary_calc', 'is_active', 'form_template', 'calculator', 'work_format'
    )
    translate_fields = ('title', 'short_description', 'description')
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }


@admin.register(Partnership)
class PartnershipAdmin(TranslateFieldAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    fields = ('title', 'short_description', 'description', 'image', 'form_template')
    translate_fields = ('title', 'description', 'short_description')
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }


class ProjectLinkInline(admin.TabularInline):
    model = ProjectLink
    extra = 1
    fields = ('link', 'is_active')
    verbose_name = 'Ссылка'
    verbose_name_plural = 'Ссылки'


@admin.register(Project)
class ProjectAdmin(TranslateFieldAdmin):
    inlines = [ProjectLinkInline]
    list_display = ('title', 'description', 'created_at')
    fields = ('title', 'description')
    search_fields = ('title',)
    translate_fields = ('title', 'description')
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }


class CityInline(admin.TabularInline):
    model = City
    extra = 0
    fields = ['name', 'is_active']
    verbose_name = "Город"
    verbose_name_plural = "Города"


@admin.register(Country)
class CountryAdmin(TranslateFieldAdmin):
    list_display = ('name', 'code', 'is_active')
    fields = ('name', 'code', 'is_active')
    search_fields = ('name', 'code')
    inlines = (CityInline,)
    translate_fields = ('name',)
    change_form_template = 'admin/translate_change_form.html'

    def save_model(self, request, obj, form, change):
        """При сохранении страны обновляем её переводы"""
        super().save_model(request, obj, form, change)
        # Принудительно обновляем переводы страны
        transaction.on_commit(
            lambda: update_object_translate(obj, translate_fields=self.translate_fields, force_update=True)
        )

    def save_related(self, request, form, formsets, change):
        """При сохранении связанных городов обновляем их переводы"""
        super().save_related(request, form, formsets, change)
        # Обновляем переводы для всех городов
        for formset in formsets:
            if isinstance(formset.model, City):
                for form in formset.forms:
                    if form.instance.pk:  # Только для сохраненных городов
                        transaction.on_commit(
                            lambda instance=form.instance: update_object_translate(
                                instance,
                                translate_fields=('name',),
                                force_update=True  # Принудительно обновляем переводы
                            )
                        )

    def response_change(self, request, obj):
        if "_force_translate" in request.POST:
            # Обновляем переводы страны и всех её городов
            transaction.on_commit(
                lambda: update_object_translate(obj, translate_fields=self.translate_fields, force_update=True)
            )
            for city in obj.cities.all():
                transaction.on_commit(
                    lambda city=city: update_object_translate(city, translate_fields=('name',), force_update=True)
                )
            self.message_user(request, "Запущено обновление переводов страны и её городов.")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


@admin.register(City)
class CityAdmin(TranslateFieldAdmin):
    list_display = ('name', 'country', 'is_active')
    fields = ('name', 'country', 'is_active')
    search_fields = ('name', 'country__name')
    list_filter = ('country', 'is_active')
    translate_fields = ('name',)
    change_form_template = 'admin/translate_change_form.html'

    def save_model(self, request, obj, form, change):
        """При сохранении города обновляем его переводы"""
        super().save_model(request, obj, form, change)
        # Принудительно обновляем переводы города
        transaction.on_commit(
            lambda: update_object_translate(obj, translate_fields=self.translate_fields, force_update=True)
        )

    def response_change(self, request, obj):
        if "_force_translate" in request.POST:
            # Принудительно обновляем переводы города
            transaction.on_commit(
                lambda: update_object_translate(obj, translate_fields=self.translate_fields, force_update=True)
            )
            self.message_user(request, "Запущено обновление переводов города.")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


@admin.register(ProductUpdateFile)
class ProductUpdateFileAdmin(admin.ModelAdmin):
    list_display = (
        'update_date', 'status', 'file'
    )


@admin.register(DVIContentFile)
class ProductUpdateFileAdmin(admin.ModelAdmin):
    list_display = (
        'file',
    )

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    fields = ('image',)
    verbose_name = "Фото"
    verbose_name_plural = "Фото"

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.max_num = 3  # Устанавливаем максимальное количество форм
        return formset

class ProductItemInline(admin.TabularInline):
    model = ProductItem
    extra = 1
    fields = ['city', 'title', 'price', 'count', 'availability_status']


class ProductAdmin(TranslateFieldAdmin):
    list_display = ('title', 'description', 'buy_url')
    fields = ('title', 'description', 'buy_url')
    search_fields = ('title',)
    inlines = [ProductItemInline, ProductImageInline]
    translate_fields = ('title', 'description')
    change_form_template = 'admin/product_change_form.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_file_upload'] = True
        return super().change_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        if 'file' in request.FILES:
            file = request.FILES['file']
            try:
                product_update_file = ProductUpdateFile.objects.create(
                    file=file,
                    file_type='xlsx',
                    update_date=timezone.now().date()
                )
                processing_product_update_file.delay(product_update_file.id)
                messages.success(request, 'Файл успешно загружен и обрабатывается')
            except Exception as e:
                messages.error(request, f'Ошибка при загрузке файла: {str(e)}')
        return super().response_change(request, obj)


admin.site.register(Product, ProductAdmin)


@admin.register(ProductItem)
class ProductItemAdmin(TranslateFieldAdmin):
    list_display = ('title', 'product', 'city', 'price', 'count', 'updated_at', 'created_at')
    fields = ('title', 'product', 'city', 'price', 'count')
    search_fields = ('title',)
    list_filter = ('city', 'product')
    translate_fields = ('title',)


@admin.register(FormTemplate)
class FormTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_type', 'is_active')
    fields = ('form_type', 'is_active')
    list_filter = ('form_type',)


class FormQuestionInline(admin.TabularInline):
    model = FormAnswerChoice
    extra = 0
    fields = ('value',)
    verbose_name = "Варианты ответов"
    verbose_name_plural = "Варианты ответов"


@admin.register(FormQuestion)
class FormQuestionAdmin(TranslateFieldAdmin):
    list_display = ('form_template', 'question', 'question_type')
    fields = ('form_template', 'question', 'question_type', 'position')
    translate_fields = ('question',)
    list_filter = ('form_template',)
    inlines = (FormQuestionInline,)


@admin.register(Calculator)
class CalculatorAdmin(admin.ModelAdmin):
    list_display = ('id',)
    fields = ('formula',)


class CalcFieldChoiceInline(admin.TabularInline):
    model = CalcFieldChoice
    extra = 0
    verbose_name = "Поля для выбора"
    verbose_name_plural = "Поля для выбора"


@admin.register(CalcField)
class CalcFieldAdmin(TranslateFieldAdmin):
    list_display = ('calculator', 'label', 'field_type')
    fields = (
        'calculator', 'field_type', 'label', 'name', 'default_value',
        'is_required', 'min_value', 'max_value', 'step', 'position'
    )
    translate_fields = ('label',)
    list_filter = ('calculator',)
    inlines = (CalcFieldChoiceInline,)


class UserFormAnswerInline(admin.TabularInline):
    model = FormAnswer
    extra = 0
    readonly_fields = ('question', 'text', 'file', 'choices')


@admin.register(FormUser)
class FormUserAdmin(admin.ModelAdmin):
    list_display = ('form_template', 'created_at', 'updated_at')
    readonly_fields = ('form_template',)
    inlines = (UserFormAnswerInline,)
    list_filter = ('form_template__vacancies', 'form_template__partnerships')


@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


@admin.register(BugReportSetting)
class BugReportSettingAdmin(TranslateFieldAdmin):
    fields = ('title',)
    translate_fields = ('title',)

@admin.register(ResourcePolicy)
class ResourcePolicyAdmin(admin.ModelAdmin):
    list_display = ('heading', 'content', 'position')
    fields = ('heading', 'content', 'position')   
    translate_fields = ('heading', 'content')
