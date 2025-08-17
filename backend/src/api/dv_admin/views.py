from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.authentication import CustomJWTAuthentication
from api.dv_admin import serializers

from api.permissions import AdminPanelCustomPermission
from apps.dv_info_site.models import MainPageSlider, MainPageButtonBlock, MainPageReputationLink, Retail, FAQ, \
    Vacancy, Partnership, Project, DVInstruction, Country, City, Product, ProductItem, ProjectLink, ProductImage, \
    Contact, FormTemplate, FormQuestion, FormAnswerChoice, BugReport, ResourcePolicy
from apps.users.utils import UserRole
from core.service.translator import TRANSLATE_SERVICES


class DVIMainSliderListCreateAPIView(generics.ListCreateAPIView):
    """Слайдер Главной страницы"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIMainSliderListSerializer
        return serializers.DVIMainSliderCreateSerializer

    def get_queryset(self):
        return MainPageSlider.objects.all()

    def post(self, request, *args, **kwargs):
        if self.get_queryset().count() >= 5:
            raise ValidationError({'detail': 'Количество слайдов ограничено'})
        return super().post(request, *args, **kwargs)

    def get_parsers(self):
        return (JSONParser(),) if self.request.method == 'GET' else (MultiPartParser(),)


class DVIMainSliderRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Слайдер Главной страницы"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIMainSliderSerializer
        return serializers.DVIMainSliderUpdateSerializer

    def get_queryset(self):
        return MainPageSlider.objects.all()


class DVIMainButtonBlockListCreateAPIView(generics.ListCreateAPIView):
    """Блок кнопок главной страницы"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIMainButtonBlockListSerializer
        return serializers.DVIMainButtonBlockCreateSerializer

    def get_parsers(self):
        return (JSONParser(),) if self.request.method == 'GET' else (MultiPartParser(),)

    def get_queryset(self):
        return MainPageButtonBlock.objects.all()


class DVIMainButtonBlockRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Блок кнопок главной страницы"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIMainButtonBlockSerializer
        return serializers.DVIMainButtonBlockUpdateSerializer

    def get_queryset(self):
        return MainPageButtonBlock.objects.all()

    def get_parsers(self):
        return (JSONParser(),) if self.request.method == 'GET' else (MultiPartParser(),)


class DVIMainReputationLinkListCreateAPIView(generics.ListCreateAPIView):
    """Репутационные ссылки"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIReputationLinkListSerializer
        return serializers.DVIReputationLinkCreateSerializer

    def get_parsers(self):
        return (JSONParser(),) if self.request.method == 'GET' else (MultiPartParser(),)

    def get_queryset(self):
        return MainPageReputationLink.objects.all()


class DVIMainReputationLinkRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Репутационные ссылки"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIReputationLinkSerializer
        return serializers.DVIReputationLinkUpdateSerializer

    def get_queryset(self):
        return MainPageReputationLink.objects.all()

    def get_parsers(self):
        return (JSONParser(),) if self.request.method == 'GET' else (MultiPartParser(),)


class DVIContactListCreateAPIView(generics.ListCreateAPIView):
    """Контакты"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIContactListSerializer
        return serializers.DVIContactCreateSerializer

    def get_queryset(self):
        return Contact.objects.all()

    def get_parsers(self):
        return (JSONParser(),) if self.request.method == 'GET' else (MultiPartParser(),)


class DVIContactRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Контакты"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIContactSerializer
        return serializers.DVIContactUpdateSerializer

    def get_queryset(self):
        return Contact.objects.all()

    def get_parsers(self):
        return (JSONParser(),) if self.request.method == 'GET' else (MultiPartParser(),)


class DVIVacancyListCreateAPIView(generics.ListCreateAPIView):
    """Вакансии"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIVacancyListSerializer
        return serializers.DVIVacancyCreateSerializer

    def get_queryset(self):
        return Vacancy.objects.all()

    def get_parsers(self):
        return (JSONParser(),) if self.request.method == 'GET' else (MultiPartParser(),)


class DVIRetailRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Розница"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIRetailSerializer
        return serializers.DVIRetailUpdateSerializer

    def get_queryset(self):
        return Retail.objects.all()

    def get_parsers(self):
        return (JSONParser(),) if self.request.method == 'GET' else (MultiPartParser(),)


class DVIRetailListCreateAPIView(generics.ListCreateAPIView):
    """Розница"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIRetailListSerializer
        return serializers.DVIRetailCreateSerializer

    def get_queryset(self):
        return Retail.objects.all()

    def get_parsers(self):
        return (JSONParser(),) if self.request.method == 'GET' else (MultiPartParser(),)


class DVIVacancyRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Вакансии"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIVacancySerializer
        return serializers.DVIVacancyUpdateSerializer

    def get_queryset(self):
        return Vacancy.objects.all()

    def get_parsers(self):
        return (JSONParser(),) if self.request.method == 'GET' else (MultiPartParser(),)


class DVIFAQListCreateAPIView(generics.ListCreateAPIView):
    """FAQ"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIFAQListSerializer
        return serializers.DVIFAQCreateSerializer

    def get_queryset(self):
        return FAQ.objects.all()

    def get_parsers(self):
        return (JSONParser(),) if self.request.method == 'GET' else (MultiPartParser(),)


class DVIFAQRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """FAQ"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIFAQSerializer
        return serializers.DVIFAQUpdateSerializer

    def get_queryset(self):
        return FAQ.objects.all()

    def get_parsers(self):
        return (JSONParser(),) if self.request.method == 'GET' else (MultiPartParser(),)


class DVIPartnershipListCreateAPIView(generics.ListCreateAPIView):
    """Партнерство"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIPartnershipListSerializer
        return serializers.DVIPartnershipCreateSerializer

    def get_queryset(self):
        return Partnership.objects.all()

    def get_parsers(self):
        return (JSONParser(),) if self.request.method == 'GET' else (MultiPartParser(),)


class DVIPartnershipRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Партнерство"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIPartnershipSerializer
        return serializers.DVIPartnershipUpdateSerializer

    def get_queryset(self):
        return Partnership.objects.all()

    def get_parsers(self):
        return (JSONParser(),) if self.request.method == 'GET' else (MultiPartParser(),)


class DVIProjectListCreateAPIView(generics.ListCreateAPIView):
    """Проекты"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIProjectListSerializer
        return serializers.DVIProjectCreateSerializer

    def get_queryset(self):
        return Project.objects.prefetch_related('links').all()


class DVIProjectRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Проекты"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIProjectSerializer
        return serializers.DVIProjectUpdateSerializer

    def get_queryset(self):
        return Project.objects.all()


class DVIProjectLinkCreateAPIView(generics.CreateAPIView):
    """Создать ссылки на проекты"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    serializer_class = serializers.ProjectLinkCreateSerializer


class DVIProjectLinkListAPIView(generics.ListAPIView):
    """Ссылки на проекты"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ProjectLinkListSerializer
        return serializers.ProjectLinkCreateSerializer

    def get_queryset(self):
        return ProjectLink.objects.filter(project_id=self.kwargs['pk'])


class DVIProjectLinkRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Ссылки на проекты"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ProjectLinkSerializer
        return serializers.ProjectLinkUpdateSerializer

    def get_queryset(self):
        return ProjectLink.objects.all()


class DVIInstructionListCreateAPIView(generics.ListCreateAPIView):
    """Инструкции"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIInstructionListSerializer
        return serializers.DVIInstructionCreateSerializer

    def get_queryset(self):
        return DVInstruction.objects.all()

    def get_parsers(self):
        return (JSONParser(),) if self.request.method == 'GET' else (MultiPartParser(),)


class DVIInstructionRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Инструкции"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIInstructionSerializer
        return serializers.DVIInstructionUpdateSerializer

    def get_queryset(self):
        return DVInstruction.objects.all()

    def get_parsers(self):
        return (JSONParser(),) if self.request.method == 'GET' else (MultiPartParser(),)


class DVIOPTCountryListCreateAPIView(generics.ListCreateAPIView):
    """Страны ОПТ"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIOPTCountryListSerializer
        return serializers.DVIOPTCountryCreateSerializer

    def get_queryset(self):
        return Country.objects.all()


class DVIOPTCountryRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Страны ОПТ"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIOPTCountrySerializer
        return serializers.DVIOPTCountryUpdateSerializer

    def get_queryset(self):
        return Country.objects.all()


class DVIOPTCityCreateAPIView(generics.CreateAPIView):
    """Города ОПТ"""
    serializer_class = serializers.DVIOPTCityCreateSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)


class DVIOPTCityRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Города ОПТ"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIOPTCitySerializer
        return serializers.DVIOPTCityUpdateSerializer

    def get_queryset(self):
        return City.objects.all()


class TranslateServiceAPIView(generics.GenericAPIView):
    """Возвращает перевод текста из всех сервисов для выбора более подходящего"""
    serializer_class = serializers.TranslateServiceSerializer
    authentication_classes = ()
    pagination_class = None
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data['text']
        data = []
        for service, translator in TRANSLATE_SERVICES.items():
            data.append({
                'service': service,
                'text': translator.translate_text(text, 'en', 'ru')
            })
        return Response(data=data, status=status.HTTP_200_OK)


class DVIOPTProductListCreateAPIView(generics.ListCreateAPIView):
    """Продукты ОПТ"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIOPTProductListSerializer
        return serializers.DVIOPTProductCreateSerializer

    def get_queryset(self):
        return Product.objects.all().prefetch_related('images')


class DVIOPTProductRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Продукты ОПТ"""
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIOPTProductSerializer
        return serializers.DVIOPTProductUpdateSerializer

    def get_queryset(self):
        return Product.objects.all()


class DVIProductImageCreateAPIView(generics.CreateAPIView):
    """"""
    serializer_class = serializers.DVIOPTProductImageCreateSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)


class DVIProductImageDestroyAPIView(generics.DestroyAPIView):
    """"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)

    def get_queryset(self):
        return ProductImage.objects.all()


class DVIOPTProductItemListAPIView(generics.ListAPIView):
    """Продукты ОПТ"""
    serializer_class = serializers.DVIOPTProductItemListSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)

    def get_queryset(self):
        return ProductItem.objects.select_related('city').filter(product_id=self.kwargs['pk'])


class DVIOPTProductItemCreateAPIView(generics.CreateAPIView):
    """Продукты ОПТ"""
    serializer_class = serializers.DVIOPTProductItemCreateSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)


class DVIOPTProductItemRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Продукты ОПТ"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DVIOPTProductItemSerializer
        return serializers.DVIOPTProductItemUpdateSerializer

    def get_queryset(self):
        return ProductItem.objects.all()


class ProductUpdateFileCreateAPIView(generics.CreateAPIView):
    """Загрузка продуктов"""
    serializer_class = serializers.ProductUpdateFileCreateSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)
    parser_classes = (MultiPartParser,)


class ContentFileSaveAPIView(generics.CreateAPIView):
    """
    Загрузка файлов для контента
    """
    serializer_class = serializers.ContentFileSaveSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser,)


class FormTemplateCreateListAPIView(generics.ListCreateAPIView):
    """Анкета"""

    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.CONTENT_MANAGER,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('form_type',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.FormTemplateListSerializer
        return serializers.FormTemplateCreateSerializer

    def get_queryset(self):
        return FormTemplate.objects.all()


class FormTemplateRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Анкета"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.FormTemplateSerializer
        return serializers.FormTemplateUpdateSerializer

    def get_queryset(self):
        return FormTemplate.objects.all()


class FormTemplateQuestionListAPIView(generics.ListCreateAPIView):
    """Вопросы анкеты"""
    serializer_class = serializers.FormTemplateQuestionListSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)

    def get_queryset(self):
        return FormQuestion.objects.prefetch_related('choices').filter(form_template_id=self.kwargs['pk'])


class FormTemplateQuestionCreateAPIView(generics.CreateAPIView):
    """Вопросы анкеты"""
    serializer_class = serializers.FormTemplateQuestionCreateSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)


class FormTemplateQuestionRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Вопросы анкеты"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.FormTemplateQuestionSerializer
        return serializers.FormTemplateQuestionUpdateSerializer

    def get_queryset(self):
        return FormQuestion.objects.all()


class FormTemplateQuestionChoiceCreateAPIView(generics.CreateAPIView):
    """Вопросы анкеты"""
    serializer_class = serializers.FormTemplateAnswerChoicesCreateSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)


class FormTemplateQuestionChoiceRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Вопросы анкеты"""
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)
    http_method_names = ('get', 'patch')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.FormTemplateAnswerChoicesSerializer
        return serializers.FormTemplateAnswerUpdateSerializer

    def get_queryset(self):
        return FormAnswerChoice.objects.all()


class BugReportListAPIView(generics.ListAPIView):
    """Список багов"""
    serializer_class = serializers.BugReportListSerializer
    queryset = BugReport.objects.all()
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)


class BugReportDestroyAPIView(generics.DestroyAPIView):
    """Удалить баг"""
    queryset = BugReport.objects.all()
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)


class BugReportSettingUpdateAPIView(generics.UpdateAPIView):
    """Настройка раздела Ловли багов"""
    serializer_class = serializers.BugReportSettingSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)
    http_method_names = ('patch',)

class ResourcePolicyListAPIView(generics.ListAPIView):
    """Политика обработки данных"""
    serializer_class = serializers.ResourcePolicySerializer
    pagination_class = None

    def get_queryset(self):
        return ResourcePolicy.objects.all()
    
class ResourcePolicyCreateAPIView(generics.CreateAPIView):
    """Политика обработки данных"""
    serializer_class = serializers.ResourcePolicySerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)
    
class ResourcePolicyDestroyAPIView(generics.DestroyAPIView):
    """Удалить политику обработки данных"""
    queryset = ResourcePolicy.objects.all()
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)

class ResourcePolicyUpdateAPIView(generics.UpdateAPIView):
    """Политика обработки данных"""
    serializer_class = serializers.ResourcePolicySerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)
    http_method_names = ('patch',)

class ResourcePolicyAPIView(generics.ListAPIView):
    """Политика обработки данных"""
    serializer_class = serializers.ResourcePolicySerializer
    pagination_class = None

    def get_queryset(self):
        return ResourcePolicy.objects.all()

class ResourcePolicyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Политика обработки данных"""
    queryset = ResourcePolicy.objects.all()
    serializer_class = serializers.ResourcePolicySerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    http_method_names = ('get','patch','delete')

class ResourcePolicyRetrieveAPIView(generics.RetrieveAPIView):
    """Политика обработки данных"""
    serializer_class = serializers.ResourcePolicySerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)
    http_method_names = ('get',)

class ResourcePolicyListCreateAPIView(generics.ListCreateAPIView):
    """Политика обработки данных"""
    serializer_class = serializers.ResourcePolicySerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    #permission_required_roles = (UserRole.OPT_MANAGER,)
    pagination_class = None