from modeltranslation.translator import register, TranslationOptions

from apps.dv_info_site.models import MainPageSlider, MainPageButtonBlock, MainPageReputationLink, FAQ, Vacancy, \
    Partnership, Project, DVInstruction, DVInstructionRow, City, Country, Product, ProductItem, FormQuestion, FormAnswerChoice, \
    BugReportSetting, ResourcePolicy


@register(MainPageSlider)
class MainPageSliderTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(MainPageButtonBlock)
class MainPageButtonBlockTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(MainPageReputationLink)
class MainPageReputationLinkTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ('answer', 'question')


@register(Vacancy)
class VacancyTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'short_description')


@register(Partnership)
class PartnershipTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'short_description')


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(DVInstruction)
class DVInstructionTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(DVInstructionRow)
class DVInstructionRowTranslationOptions(TranslationOptions):
    fields = ('column1_text', 'column2_text', 'column3_text') 

@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(ProductItem)
class ProductItemTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(FormQuestion)
class FormQuestionTranslationOptions(TranslationOptions):
    fields = ('question',)


@register(FormAnswerChoice)
class ProductItemTranslationOptions(TranslationOptions):
    fields = ('value',)


@register(BugReportSetting)
class BugReportSettingOptions(TranslationOptions):
    fields = ('title',)

@register(ResourcePolicy)
class ResourcePolicyOptions(TranslationOptions):
    fields = ('heading', 'content')