from django.urls import path

from api.da_vinci_info_site import views

app_name = 'dv-info'
urlpatterns = [
    path('main/slider/', views.MainPageSliderListAPIView.as_view(), name='main-slider-list'),
    path('main/button-block/', views.MainPageButtonBlockAPIView.as_view(), name='main-button-block-list'),
    path('main/reputation-links/', views.MainPageReputationLinkAPIView.as_view(), name='main-reputation-links-list'),
    path('retail/', views.RetailAPIView.as_view(), name='retail-list'),
    path('contacts/', views.ContactsAPIView.as_view(), name='contacts-list'),

    path('faq/', views.FAQAPIView.as_view(), name='faq-list'),
    # path('vacancies/form/', views.VacancyFormCreateAPIView.as_view(), name='vacancies-form'),
    path('vacancies/', views.VacancyAPIView.as_view(), name='vacancies-list'),

    path('partnerships/', views.PartnershipAPIView.as_view(), name='partnerships-list'),
    path('projects/', views.ProjectAPIView.as_view(), name='projects-list'),

    path('dv-instructions/', views.DVInstructionAPIView.as_view(), name='dv-instructions-list'),
    #path('dv-instruction-rows/', views.DVInstructionRowAPIView.as_view(), name='dv-instruction-rows-list'),
    
    path('opt/countries/', views.OPTCountryListAPIView.as_view(), name='opt-country-list'),

    path('opt/products/export/', views.OPTProductExportExcelAPIView.as_view(), name='opt-product-export-list'),
    path('opt/products/', views.OPTProductListAPIView.as_view(), name='opt-product-list'),

    path('form-template/<int:pk>/', views.FormTemplateRetrieveAPIView.as_view(), name='form-template'),
    path('form-template/complete/', views.FormTemplateCompleteAPIView.as_view(), name='form-template-complete'),
    path('file-upload/', views.FileUploadAPIView.as_view(), name='file-upload'),

    path('calculators/<int:pk>/', views.CalculatorRetrieveAPIView.as_view(), name='calculator-retrieve'),

    path('bugs/settings/', views.BugReportSettingAPIView.as_view(), name='bug-settings'),
    path('bugs/report/', views.BugReportCreateAPIView.as_view(), name='bug-report-create'),

    path('resource-policy/<int:pk>/', views.ResourcePolicyRetrieveAPIView.as_view(), name='resource-policy-retrieve'),
    path('resource-policy/', views.ResourcePolicyListCreateAPIView.as_view(), name='resource-policy-lc'),

    path('update-translations/', views.ResetTranslationsAPIView.as_view(), name='update-translations'),

    path('vacancies-transalted/', views.TranslatedVacanciesView.as_view(), name='translated-vacancies'),
]
