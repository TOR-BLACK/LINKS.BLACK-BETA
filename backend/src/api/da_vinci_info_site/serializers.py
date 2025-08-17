from django.db import transaction
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.utils.translation import get_language

from apps.dv_info_site.models import MainPageSlider, MainPageButtonBlock, MainPageReputationLink, Retail, FAQ, \
    Vacancy, Partnership, ProjectLink, Project, DVInstruction, DVInstructionRow, Country, City, Product, ProductImage, ProductItem, \
    Contact, FormTemplate, FormQuestion, FormAnswerChoice, FormAnswer, FormUser, DVIContentFile, Calculator, CalcField, \
    CalcFieldChoice, BugReportSetting, BugReport, ResourcePolicy


class MainPageSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPageSlider
        fields = (
            'id', 'title', 'description', 'image'
        )


class MainPageButtonBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPageButtonBlock
        fields = (
            'id', 'title', 'description', 'background_image', 'link'
        )


class MainPageReputationLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPageReputationLink
        fields = (
            'id', 'title', 'image', 'link'
        )


class RetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retail
        fields = (
            'id', 'name', 'link_type', 'link'
        )


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'id', 'person', 'person_avatar', 'department', 'element', 'telegram', 'is_telegram_active', 'session'
        )


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = (
            'id', 'position', 'question', 'answer', 'image'
        )


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = (
            'id', 'image', 'title', 'salary', 'short_description', 'description', 'salary_calc', 'form_template',
            'calculator'
        )


# class VacancyFormAnswerSerializer(serializers.ModelSerializer):
#     choices = serializers.ListField(
#         child=serializers.PrimaryKeyRelatedField(queryset=FormAnswerChoice.objects.all())
#     )
#
#     class Meta:
#         model = FormAnswer
#         fields = (
#             'question', 'text', 'file', 'choices'
#         )
#
#
# class VacancyFormCreateSerializer(serializers.Serializer):
#     vacancy = serializers.PrimaryKeyRelatedField(queryset=Vacancy.objects.all())
#     answers = VacancyFormAnswerSerializer(many=True)
#
#     def create(self, validated_data):
#         form_template = validated_data['vacancy'].form_template
#         user = FormUser.objects.create(
#             form_template=form_template,
#         )
#         answers = []
#         for answer in validated_data['answers']:
#             form_answer = FormAnswer(
#                 user=user,
#                 question=answer['question'],
#                 text=answer['text'],
#                 file=answer['file']
#             )
#             if answer['choices']:
#                 form_answer.save()
#                 form_answer.choices.add(*answer['choices'])
#             else:
#                 answers.append(form_answer)
#         if answers:
#             FormAnswer.objects.bulk_create(objs=answers)
#         return {
#             'vacancy': validated_data['vacancy'],
#             'answers': user.answers.all()
#         }


class PartnershipSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()

    class Meta:
        model = Partnership
        fields = (
            'id', 'title', 'description', 'image', 'form_template', 'short_description'
        )

    def get_translated_field(self, obj, field_name):
        """Helper method to get translated field value with fallback."""
        language = get_language()
        # Try to get translated value
        translated_value = getattr(obj, f'{field_name}_{language}', None)
        if translated_value:
            return translated_value
        # Fallback to default language value
        return getattr(obj, field_name)

    def get_title(self, obj):
        return self.get_translated_field(obj, 'title')

    def get_description(self, obj):
        return self.get_translated_field(obj, 'description')

    def get_short_description(self, obj):
        return self.get_translated_field(obj, 'short_description')


class ProjectLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLink
        fields = (
            'link', 'is_active'
        )


class ProjectSerializer(serializers.ModelSerializer):
    links = ProjectLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = (
            'id', 'title', 'description', 'links'
        )


class DVInstructionRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = DVInstructionRow
        #fields = ['id', 'content'] 
        fields = ('id', 'column1_text', 'column1_image', 'column2_text', 'column2_image', 'column3_text', 'column3_image')

'''class DVInstructionRowSerializer(serializers.ModelSerializer):
    instruction_title = serializers.CharField(source='instruction.title', read_only=True)
    instruction = serializers.PrimaryKeyRelatedField(read_only=True)'''

class DVInstructionSerializer(serializers.ModelSerializer):
    rows = DVInstructionRowSerializer(many=True, read_only=True)

    class Meta:
        model = DVInstruction
        fields = (
            'id', 'title', 'rows'
        )

    def get_queryset(self):
        return DVInstruction.objects.prefetch_related('rows').all().order_by('id')

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'id', 'name'
        )


class CountrySerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = (
            'id', 'name', 'cities', 'code'
        )


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class ProductItemSerializer(serializers.ModelSerializer):
    #updated_at = serializers.DateTimeField(source='updated_at', read_only=True)
    class Meta:
        model = ProductItem
        fields = (
            'id', 'title', 'price', 'count', 'availability_status', 'city', 'updated_at'
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        availability = self.request.query_params.get('availability', None)
        if availability:
            queryset = queryset.filter(availability_status=availability)
        return queryset


class ProductItemAggregateSerializer(serializers.Serializer):
    city = CitySerializer(read_only=True)
    items = ProductItemSerializer(many=True, read_only=True)


class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    items = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'title', 'description', 'buy_url', 'images', 'items'
        )

    @swagger_serializer_method(ProductItemAggregateSerializer)
    def get_items(self, obj):
        cities = {}
        for item in obj.items.all():
            if item.city_id in cities:
                items = cities[item.city_id]['items']
                items.append(item)
                cities[item.city_id]['items'] = items
            else:
                cities[item.city_id] = {
                    'items': [item],
                    'city': item.city
                }
        return ProductItemAggregateSerializer(cities.values(), many=True, context=self.context).data


class FormQuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormAnswerChoice
        fields = (
            'id', 'value'
        )


class FormQuestionSerializer(serializers.ModelSerializer):
    choices = FormQuestionChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = FormQuestion
        fields = (
            'id', 'question', 'question_type', 'position', 'choices'
        )


class FormTemplateSerializer(serializers.ModelSerializer):
    questions = FormQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = FormTemplate
        fields = (
            'id', 'questions'
        )


class FormTemplateAnswerSerializer(serializers.ModelSerializer):
    choices = serializers.ListSerializer(
        child=serializers.PrimaryKeyRelatedField(queryset=FormAnswerChoice.objects.all()),
        allow_null=True,
        allow_empty=True
    )

    class Meta:
        model = FormAnswer
        fields = (
            'question', 'text', 'file', 'choices'
        )


class FormTemplateCompleteSerializer(serializers.Serializer):
    form_template = serializers.PrimaryKeyRelatedField(queryset=FormTemplate.objects.all())
    answers = FormTemplateAnswerSerializer(many=True)

    @transaction.atomic
    def create(self, validated_data):
        user = FormUser.objects.create(form_template=validated_data['form_template'])
        answers = []
        for answer in validated_data['answers']:
            a = FormAnswer(
                user=user,
                question=answer['question'],
                text=answer['text'],
                file=answer['file'],
            )
            if answer.get('choices'):
                a.save()
                a.choices.add(*answer['choices'])
            else:
                answers.append(a)
        if answers:
            FormAnswer.objects.bulk_create(objs=answers)
        return {
            'form_template': validated_data['form_template'],
            'answers': user.answers.all()
        }


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DVIContentFile
        fields = (
            'id', 'file'
        )
        extra_kwargs = {
            'id': {'read_only': True}
        }


class CalcFieldChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalcFieldChoice
        fields = (
            'id', 'label', 'value'
        )


class CalculatorFieldSerializer(serializers.ModelSerializer):
    choices = CalcFieldChoiceSerializer(many=True)

    class Meta:
        model = CalcField
        fields = (
            'id', 'field_type', 'label', 'name', 'default_value', 'is_required', 'min_value',
            'max_value', 'step', 'position', 'choices'
        )


class CalculatorSerializer(serializers.ModelSerializer):
    fields = CalculatorFieldSerializer(many=True)

    class Meta:
        model = Calculator
        fields = (
            'formula', 'fields'
        )


class BugReportSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugReportSetting
        fields = (
            'title',
        )


class BugReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugReport
        fields = (
            'title', 'description', 'file'
        )

class ResourcePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourcePolicy
        fields = (
            'id', 'heading', 'content', 'position'
        )