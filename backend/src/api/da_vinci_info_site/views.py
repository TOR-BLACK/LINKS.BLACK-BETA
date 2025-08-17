from datetime import datetime

from django.db.models import Prefetch
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from api.da_vinci_info_site import serializers
from api.da_vinci_info_site.filters import OPTProductListFilter
from apps.dv_info_site.models import MainPageSlider, MainPageButtonBlock, MainPageReputationLink, Retail, FAQ, \
    Vacancy, Partnership, Project, DVInstruction, DVInstructionRow, Country, City, Product, ProductItem, Contact, FormTemplate, \
    FormQuestion, Calculator, BugReportSetting, ResourcePolicy, FormAnswerChoice
from apps.dv_info_site.services.export_products import generate_excel_file
from core.service.translator import update_bulk_objects_translate

import requests
from core.service.translator import translate_with_retries
from core.adapters.translaters import GoogleTranslator
from core.adapters.translaters import DeepLTranslator
from core.adapters.translaters import OpenAITranslator

class MainPageSliderListAPIView(generics.ListAPIView):
    """
    Слайдер Главной страницы
    Количество слайдов ограничено до 5 шт
    """
    serializer_class = serializers.MainPageSliderSerializer
    pagination_class = None

    def get_queryset(self):
        return MainPageSlider.objects.all()


class MainPageButtonBlockAPIView(generics.ListAPIView):
    """
    Блок кнопок главной страницы
    """
    serializer_class = serializers.MainPageButtonBlockSerializer
    pagination_class = None

    def get_queryset(self):
        return MainPageButtonBlock.objects.all()


class MainPageReputationLinkAPIView(generics.ListAPIView):
    """
    Репутационные ссылки
    """
    serializer_class = serializers.MainPageReputationLinkSerializer
    pagination_class = None

    def get_queryset(self):
        return MainPageReputationLink.objects.all()


class RetailAPIView(generics.ListAPIView):
    """Розница"""
    serializer_class = serializers.RetailSerializer
    pagination_class = None

    def get_queryset(self):
        return Retail.objects.all()


class ContactsAPIView(generics.ListAPIView):
    """
    Контакты
    contract_type = messenger, site
    """
    serializer_class = serializers.ContactSerializer
    pagination_class = None

    def get_queryset(self):
        return Contact.objects.all()


class FAQAPIView(generics.ListAPIView):
    """FAQ"""
    serializer_class = serializers.FAQSerializer
    pagination_class = None

    def get_queryset(self):
        return FAQ.objects.all()


class VacancyAPIView(generics.ListAPIView):
    """Вакансии"""
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('work_format',)
    serializer_class = serializers.VacancySerializer
    pagination_class = None

    def get_queryset(self):
        return Vacancy.objects.filter(is_active=True)


# class VacancyFormCreateAPIView(generics.CreateAPIView):
#     """Отклик на вакансию"""
#     serializer_class = serializers.VacancyFormCreateSerializer


class PartnershipAPIView(generics.ListAPIView):
    """Партнерство"""
    serializer_class = serializers.PartnershipSerializer
    pagination_class = None

    def get_queryset(self):
        return Partnership.objects.all()

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        if hasattr(request, 'LANGUAGE_CODE'):
            response['Content-Language'] = request.LANGUAGE_CODE
        return response


class ProjectAPIView(generics.ListAPIView):
    """Зеркало проектов"""
    serializer_class = serializers.ProjectSerializer
    pagination_class = None

    def get_queryset(self):
        return Project.objects.prefetch_related('links').all()


class DVInstructionAPIView(generics.ListAPIView):
    """DV инструкции"""
    serializer_class = serializers.DVInstructionSerializer
    pagination_class = None

    def get_queryset(self):
        return DVInstruction.objects.all()
        #return DVInstruction.objects.prefetch_related('rows').all()
        
"""
class DVInstructionRowAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.DVInstructionSerializer
    pagination_class = None

    def get_queryset(self):
        return DVInstructionRow.objects.select_related('instruction').all()
"""

class OPTCountryListAPIView(generics.ListAPIView):
    """Страны OPT"""
    serializer_class = serializers.CountrySerializer
    pagination_class = None

    def get_queryset(self):
        return Country.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                lookup='cities',
                queryset=City.objects.filter(is_active=True)
            )
        )


class OPTProductBaseAPIView(generics.GenericAPIView):
    """"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OPTProductListFilter

    def get_queryset(self):
        queryset = Product.objects.all().prefetch_related('images')
        if 'cities' not in self.request.query_params:  # фильтрация по городам делается в OPTProductListFilter
            queryset.prefetch_related(
                Prefetch(
                    lookup='items',
                    queryset=ProductItem.objects.select_related('city')
                )
            )
        return queryset


class OPTProductListAPIView(OPTProductBaseAPIView, generics.ListAPIView):
    """Список продуктов ОПТ"""

    serializer_class = serializers.ProductListSerializer


class OPTProductExportExcelAPIView(OPTProductBaseAPIView):
    """Список продуктов ОПТ для экспорта в excel"""
    #serializer_class = None
    serializer_class = serializers.ProductListSerializer
    http_method_names = ('get',)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        date = datetime.today().strftime('%Y-%m-%d')
        return FileResponse(generate_excel_file(queryset), filename=f'products_{date}.xlsx')


class FormTemplateRetrieveAPIView(generics.RetrieveAPIView):
    """Анкета"""
    serializer_class = serializers.FormTemplateSerializer

    def get_queryset(self):
        return FormTemplate.objects.prefetch_related(
            Prefetch(
                lookup='questions',
                queryset=FormQuestion.objects.prefetch_related('choices')
            )
        )


class FormTemplateCompleteAPIView(generics.CreateAPIView):
    """Анкета"""
    serializer_class = serializers.FormTemplateCompleteSerializer


class FileUploadAPIView(generics.CreateAPIView):
    """Загрузка файлов"""
    serializer_class = serializers.FileUploadSerializer
    parser_classes = (MultiPartParser,)


class CalculatorRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.CalculatorSerializer
    queryset = Calculator.objects.all()


class BugReportSettingAPIView(generics.RetrieveAPIView):
    """Настройки раздела багов"""
    serializer_class = serializers.BugReportSettingSerializer

    def get_object(self):
        return BugReportSetting.load()


class BugReportCreateAPIView(generics.CreateAPIView):
    """Создать отчет о баге"""
    serializer_class = serializers.BugReportCreateSerializer
    parser_classes = (MultiPartParser,)

class ResourcePolicyAPIView(generics.ListAPIView):
    """Политика обработки данных"""
    serializer_class = serializers.ResourcePolicySerializer
    pagination_class = None

    def get_queryset(self):
        return ResourcePolicy.objects.all()

class ResourcePolicyRetrieveAPIView(generics.RetrieveAPIView):
    """Политика обработки данных"""
    serializer_class = serializers.ResourcePolicySerializer
    queryset = ResourcePolicy.objects.all()

class ResourcePolicyListCreateAPIView(generics.ListCreateAPIView):
    """Политика обработки данных"""
    serializer_class = serializers.ResourcePolicySerializer
    queryset = ResourcePolicy.objects.all()

class ResourcePolicyUpdateAPIView(generics.UpdateAPIView):
    """Политика обработки данных"""
    serializer_class = serializers.ResourcePolicySerializer
    queryset = ResourcePolicy.objects.all()

class ResourcePolicyDestroyAPIView(generics.DestroyAPIView):
    """Политика обработки данных"""
    serializer_class = serializers.ResourcePolicySerializer
    queryset = ResourcePolicy.objects.all()

class ResetTranslationsAPIView(APIView):
    """Сброс и обновление всех переводов для моделей"""
    def get(self, request, *args, **kwargs):
        # Обновление переводов для всех моделей
        models_to_update = [
            (MainPageSlider, ['title', 'description']),
            (MainPageButtonBlock, ['title', 'description']),
            (MainPageReputationLink, ['title', 'description']),
            (FAQ, ['question', 'answer']),
            (Vacancy, ['title', 'description', 'short_description']),
            (Partnership, ['title', 'description']),
            (Project, ['title', 'description']),
            (DVInstruction, ['title', 'description']),
            (DVInstructionRow, ['column1_text', 'column2_text', 'column3_text']),
            (City, ['name']),
            (Country, ['name']),
            (Product, ['name', 'description']),
            (ProductItem, ['name', 'description']),
            (FormQuestion, ['question']),
            (FormAnswerChoice, ['choice_text']),
            (BugReportSetting, ['title', 'description']),
            (ResourcePolicy, ['title', 'description']),
        ]

        for model, fields in models_to_update:
            objects = model.objects.all()
            update_bulk_objects_translate(objects, fields)

        return Response({"message": "All translations reset and updated successfully"}, status=status.HTTP_200_OK)

class TranslatedVacanciesView(APIView):
    """
    Получает список вакансий и возвращает их переведенные версии на запрашиваемом языке.
    """
    def get(self, request):
        translator = DeepLTranslator()
        language = request.query_params.get('lang', 'ru')
        is_test = request.query_params.get('test', 'true').lower() == 'true'
        base = "https://localhost/info2" if is_test else "https://localhost"
        base_url = f"{base}/api/admin/vacancies"
        response = requests.get(base_url)

        if response.status_code != 200:
            return Response({"error": "Failed to fetch vacancies"}, status=response.status_code)

        vacancies = response.json()

        translated_vacancies = []

        if (language == 'ru'):
            return Response(vacancies)

        for vacancy in vacancies:
            translated_vacancy = {
                **vacancy,
                'name': translate_with_retries(translator, vacancy['name'], to_lang=language, from_lang='ru')[0],
                'description': translate_with_retries(translator, vacancy['description'], to_lang=language, from_lang='ru')[0],
            }
            translated_vacancies.append(translated_vacancy)

        return Response(translated_vacancies)