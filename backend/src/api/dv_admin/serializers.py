from django.utils import timezone
from rest_framework import serializers

from apps.dv_info_site.models import MainPageSlider, MainPageButtonBlock, MainPageReputationLink, Retail, FAQ, \
    Vacancy, Partnership, ProjectLink, Project, DVInstruction, Country, City, Product, ProductImage, ProductItem, \
    ProductUpdateFile, Contact, DVIContentFile, FormTemplate, FormQuestion, FormAnswerChoice, BugReport, \
    BugReportSetting, ResourcePolicy
from apps.dv_info_site.services.product_parsing import processing_product_update_file
from core.service.translator import TranslateFieldMixin

class DVIMainSliderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPageSlider
        fields = (
            'id', 'title', 'description', 'image'
        )


class DVIMainSliderCreateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = MainPageSlider
        fields = (
            'id', 'title', 'description', 'image'
        )
        translate_fields = ('title', 'description')


class DVIMainSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPageSlider
        fields = (
            'id', 'title', 'description', 'image'
        )


class DVIMainSliderUpdateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = MainPageSlider
        fields = (
            'id', 'title', 'description', 'image'
        )
        translate_fields = ('title', 'description')


class DVIMainButtonBlockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPageButtonBlock
        fields = (
            'id', 'title', 'description', 'background_image', 'link'
        )


class DVIMainButtonBlockCreateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = MainPageButtonBlock
        fields = (
            'id', 'title', 'description', 'background_image', 'link'
        )
        translate_fields = ('title', 'description')


class DVIMainButtonBlockUpdateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = MainPageButtonBlock
        fields = (
            'id', 'title', 'description', 'background_image', 'link'
        )
        translate_fields = ('title', 'description')


class DVIMainButtonBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPageButtonBlock
        fields = (
            'id', 'title', 'description', 'background_image', 'link'
        )


class DVIReputationLinkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPageReputationLink
        fields = (
            'id', 'title', 'image', 'link'
        )


class DVIReputationLinkCreateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = MainPageReputationLink
        fields = (
            'id', 'title', 'image', 'link'
        )
        translate_fields = ('title',)


class DVIReputationLinkUpdateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = MainPageReputationLink
        fields = (
            'id', 'title', 'image', 'link'
        )
        translate_fields = ('title',)


class DVIReputationLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPageReputationLink
        fields = (
            'id', 'title', 'image', 'link'
        )


class DVIContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'id', 'department', 'person', 'person_avatar', 'telegram', 'element', 'session'
        )


class DVIContactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'id', 'department', 'person', 'person_avatar', 'telegram', 'element', 'session'
        )


class DVIContactUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'id', 'department', 'person', 'person_avatar', 'telegram', 'element', 'session'
        )


class DVIContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'id', 'department', 'person', 'person_avatar', 'telegram', 'element', 'session'
        )


class DVIRetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retail
        fields = (
            'id', 'name', 'link_type', 'link'
        )


class DVIRetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retail
        fields = (
            'id', 'name', 'link_type', 'link'
        )


class DVIRetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retail
        fields = (
            'id', 'name', 'link_type', 'link'
        )


class DVIRetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retail
        fields = (
            'id', 'name', 'link_type', 'link'
        )


class DVIVacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = (
            'id', 'image', 'title', 'salary', 'short_description',
            'description', 'salary_calc', 'is_active'
        )


class DVIVacancyCreateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = (
            'id', 'image', 'title', 'salary', 'short_description',
            'description', 'salary_calc', 'is_active'
        )
        translate_fields = ('title', 'description', 'short_description')


class DVIVacancyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = (
            'id', 'image', 'title', 'salary', 'short_description',
            'description', 'salary_calc', 'is_active'
        )


class DVIVacancyUpdateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = (
            'id', 'image', 'title', 'salary', 'short_description',
            'description', 'salary_calc', 'is_active'
        )

        translate_fields = ('title', 'description', 'short_description')


class DVIFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = (
            'id', 'question', 'answer', 'image', 'position'
        )


class DVIFAQUpdateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = (
            'id', 'question', 'answer', 'image', 'position'
        )
        translate_fields = ('answer', 'question')


class DVIFAQCreateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = (
            'id', 'question', 'answer', 'image', 'position'
        )
        translate_fields = ('answer', 'question')


class DVIFAQListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = (
            'id', 'question', 'answer', 'image', 'position'
        )


class DVIPartnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partnership
        fields = (
            'id', 'title', 'description', 'image', 'short_description', 'form_template'
        )


class DVIPartnershipCreateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Partnership
        fields = (
            'id', 'title', 'description', 'image', 'short_description', 'form_template'
        )
        translate_fields = ('title', 'description', 'short_description')


class DVIPartnershipListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partnership
        fields = (
            'id', 'title', 'description', 'image', 'short_description', 'form_template'
        )


class DVIPartnershipUpdateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Partnership
        fields = (
            'id', 'title', 'description', 'image', 'short_description', 'form_template'
        )
        translate_fields = ('title', 'description', 'short_description')


class ProjectLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLink
        fields = (
            'id', 'link', 'is_active'
        )


class ProjectLinkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLink
        fields = (
            'id', 'link', 'is_active'
        )


class ProjectLinkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLink
        fields = (
            'id', 'link', 'is_active'
        )


class ProjectLinkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLink
        fields = (
            'id', 'project', 'link', 'is_active'
        )


class DVIProjectSerializer(serializers.ModelSerializer):
    links = ProjectLinkListSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = (
            'id', 'title', 'description', 'links'
        )


class DVIProjectCreateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id', 'title', 'description'
        )
        translate_fields = ('title', 'description')


class DVIProjectListSerializer(serializers.ModelSerializer):
    links = ProjectLinkListSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = (
            'id', 'title', 'description', 'links'
        )


class DVIProjectUpdateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id', 'title', 'description'
        )
        translate_fields = ('title', 'description')


class DVIInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DVInstruction
        fields = (
            'id', 'title', 'description', 'icon'
        )


class DVIInstructionCreateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = DVInstruction
        fields = (
            'id', 'title', 'description', 'icon'
        )
        translate_fields = ('title', 'description')


class DVIInstructionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DVInstruction
        fields = (
            'id', 'title', 'description', 'icon'
        )


class DVIInstructionUpdateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = DVInstruction
        fields = (
            'id', 'title', 'description', 'icon'
        )
        translate_fields = ('title', 'description')


class DVIOPTCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'id', 'name', 'country', 'is_active'
        )


class DVIOPTCityCreateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'id', 'name', 'country', 'is_active'
        )
        translate_fields = ('name',)


class DVIOPTCityUpdateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'id', 'name', 'country', 'is_active'
        )
        translate_fields = ('name',)


class DVIOPTCityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'id', 'name', 'is_active'
        )


class DVIOPTCountrySerializer(serializers.ModelSerializer):
    cities = DVIOPTCityListSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = (
            'id', 'name', 'code', 'is_active', 'cities'
        )


class DVIOPTCountryCreateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            'id', 'name', 'code', 'is_active'
        )
        translate_fields = ('name',)


class DVIOPTCountryUpdateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            'id', 'name', 'code', 'is_active'
        )
        translate_fields = ('name',)


class DVIOPTCountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            'id', 'name', 'code', 'is_active'
        )


class TranslateServiceSerializer(serializers.Serializer):
    text = serializers.CharField()


class ProductImageForProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            'id', 'image'
        )


class DVIOPTProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id', 'title', 'description'
        )


class DVIOPTProductListSerializer(serializers.ModelSerializer):
    images = ProductImageForProductListSerializer(many=True, read_only=True)
    #items = DVIOPTProductItemListSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'title', 'description', 'images'#, 'items'
        )


class DVIOPTProductUpdateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id', 'title', 'description'
        )
        translate_fields = ('title', 'description')


class DVIOPTProductCreateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id', 'title', 'description'
        )
        translate_fields = ('title', 'description')


class DVIOPTProductImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            'id', 'image', 'product'
        )


class DVIOPTProductItemListSerializer(serializers.ModelSerializer):
    city = DVIOPTCitySerializer()
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ProductItem
        fields = (
            'id', 'city', 'title', 'price', 'count', 'updated_at'
        )


class DVIOPTProductItemCreateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = (
            'id', 'city', 'title', 'price', 'count', 'product'
        )
        translate_fields = ('title',)


class DVIOPTProductItemUpdateSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = (
            'id', 'city', 'title', 'price', 'count', 'product'
        )
        translate_fields = ('title',)


class DVIOPTProductItemSerializer(serializers.ModelSerializer):
    city = DVIOPTCitySerializer()

    class Meta:
        model = ProductItem
        fields = (
            'id', 'city', 'title', 'price', 'count'
        )


class ProductUpdateFileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUpdateFile
        fields = (
            'id', 'file', 'status', 'update_date'
        )
        read_only_fields = ('status', 'update_date')

    def create(self, validated_data):
        validated_data['update_date'] = timezone.now().date()  # TODO нужно уточнить будут ли отправлять дату или
        instance = super().create(validated_data)
        processing_product_update_file.delay(instance.id)
        return instance


class ContentFileSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DVIContentFile
        fields = (
            'file',
        )


class FormTemplateAnswerChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormAnswerChoice
        fields = (
            'id', 'value'
        )


class FormTemplateAnswerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormAnswerChoice
        fields = (
            'id', 'value'
        )


class FormTemplateAnswerChoicesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormAnswerChoice
        fields = (
            'id', 'value', 'form_question'
        )


class FormTemplateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormTemplate
        fields = (
            'id', 'form_type', 'is_active'
        )


class FormTemplateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormTemplate
        fields = (
            'id', 'form_type', 'is_active'
        )


class FormTemplateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormTemplate
        fields = (
            'id', 'form_type', 'is_active'
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs.get('is_active'):
            is_exist_active_form = FormTemplate.objects.filter(
                is_active=True,
                form_type=attrs['form_type']
            ).exists()
            if is_exist_active_form:
                raise serializers.ValidationError({'detail': 'Активная анкета уже существует'})
        return attrs


class FormTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormTemplate
        fields = (
            'id', 'form_type', 'is_active'
        )


class FormTemplateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormQuestion
        fields = (
            'id', 'question', 'position', 'question_type'
        )


class FormTemplateQuestionListSerializer(serializers.ModelSerializer):
    choices = FormTemplateAnswerChoicesSerializer(many=True)

    class Meta:
        model = FormQuestion
        fields = (
            'id', 'question', 'position', 'question_type', 'choices'
        )


class FormTemplateQuestionCreateSerializer(serializers.ModelSerializer):
    # choices = FormTemplateAnswerChoicesCreateSerializer(many=True)

    class Meta:
        model = FormQuestion
        fields = (
            'id', 'form_template', 'question', 'position', 'question_type'
        )

    # @transaction.atomic
    # def create(self, validated_data):
    #     choices = validated_data.pop('choices', None)
    #     instance = super().create(validated_data)
    #     if choices:
    #         self.create_choices(instance, choices)
    #     return instance
    #
    # def create_choices(self, form_question, choices):
    #     for data in choices:
    #         serializer = FormTemplateQuestionSerializer(
    #             data={
    #                 'form_question': form_question,
    #                 'value': data['value'],
    #             },
    #             context=self.context
    #         )
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()


class FormTemplateQuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormQuestion
        fields = (
            'id', 'question', 'position', 'question_type'
        )


class BugReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugReport
        fields = (
            'id', 'title', 'description', 'file', 'created_at'
        )


class BugReportSettingSerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = BugReportSetting
        fields = (
            'title',
        )
        translate_fields = ('title',)

class ResourcePolicySerializer(TranslateFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = ResourcePolicy
        fields = (
             'id', 'heading', 'content', 'position'
        )
        translate_fields = ('heading', 'content')