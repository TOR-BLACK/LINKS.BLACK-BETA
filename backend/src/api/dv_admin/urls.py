from django.urls import path
from api.dv_admin import views

app_name = 'dv-admin'
urlpatterns = [
    path('main/sitebar/<int:pk>/', views.DVIMainSliderRetrieveUpdateAPIView.as_view(), name='main-slider-rud'),
    path('main/sitebar/', views.DVIMainSliderListCreateAPIView.as_view(), name='main-slider-lc'),

    path('main/button-block/<int:pk>/', views.DVIMainButtonBlockRetrieveUpdateAPIView.as_view(),
         name='main-button-block-rud'),
    path('main/button-block/', views.DVIMainButtonBlockListCreateAPIView.as_view(), name='main-button-block-lc'),

    path('main/reputation-links/<int:pk>/', views.DVIMainReputationLinkRetrieveUpdateAPIView.as_view(),
         name='main-reputation-link-rud'),
    path('main/reputation-links/', views.DVIMainReputationLinkListCreateAPIView.as_view(),
         name='main-reputation-link-lc'),

    path('contacts/<int:pk>/', views.DVIContactRetrieveUpdateAPIView.as_view(), name='contact-rud'),
    path('contacts/', views.DVIContactListCreateAPIView.as_view(), name='contact-lc'),

    path('vacancies/<int:pk>/', views.DVIVacancyRetrieveUpdateAPIView.as_view(), name='vacancy-rud'),
    path('vacancies/', views.DVIVacancyListCreateAPIView.as_view(), name='vacancy-lc'),
    path('retail/<int:pk>/', views.DVIRetailRetrieveUpdateAPIView.as_view(), name='retail-rud'),
    path('retail/', views.DVIRetailListCreateAPIView.as_view(), name='retail-lc'),

    path('faq/<int:pk>/', views.DVIFAQRetrieveUpdateAPIView.as_view(), name='faq-rud'),
    path('faq/', views.DVIFAQListCreateAPIView.as_view(), name='faq-lc'),

    path('partnerships/<int:pk>/', views.DVIPartnershipRetrieveUpdateAPIView.as_view(), name='partnership-rud'),
    path('partnerships/', views.DVIPartnershipListCreateAPIView.as_view(), name='partnership-lc'),

    path('projects/<int:pk>/links/', views.DVIProjectLinkListAPIView.as_view(), name='project-links-list'),
    path('projects/links/<int:pk>/', views.DVIProjectLinkRetrieveUpdateAPIView.as_view(), name='project-link-rud'),
    path('projects/links/', views.DVIProjectLinkCreateAPIView.as_view(), name='project-link-create'),
    path('projects/<int:pk>/', views.DVIProjectRetrieveUpdateAPIView.as_view(), name='project-rud'),
    path('projects/', views.DVIProjectListCreateAPIView.as_view(), name='project-lc'),

    path('dv-instructions/<int:pk>/', views.DVIInstructionRetrieveUpdateAPIView.as_view(), name='dv-instruction-rud'),
    path('dv-instructions/', views.DVIInstructionListCreateAPIView.as_view(), name='dv-instruction-lc'),

    path('opt/countries/<int:pk>/', views.DVIOPTCountryRetrieveUpdateAPIView.as_view(), name='opt-country-rud'),
    path('opt/countries/', views.DVIOPTCountryListCreateAPIView.as_view(), name='opt-country-lc'),

    path('opt/cities/<int:pk>/', views.DVIOPTCityRetrieveUpdateAPIView.as_view(), name='opt-city-rud'),
    path('opt/cities/', views.DVIOPTCityCreateAPIView.as_view(), name='opt-city-create'),

    path('translate-service/', views.TranslateServiceAPIView.as_view(), name='translate-service'),

    path('opt/products/<int:pk>/items/', views.DVIOPTProductItemListAPIView.as_view()),
    path('opt/products/items/<int:pk>/', views.DVIOPTProductItemRetrieveUpdateAPIView.as_view()),
    path('opt/products/items/', views.DVIOPTProductItemCreateAPIView.as_view()),
    path('opt/products/<int:pk>/', views.DVIOPTProductRetrieveUpdateAPIView.as_view()),
    path('opt/products/images/<int:pk>/', views.DVIProductImageDestroyAPIView.as_view()),
    path('opt/products/images/', views.DVIProductImageCreateAPIView.as_view()),
    path('opt/products/update/', views.ProductUpdateFileCreateAPIView.as_view()),
    path('opt/products/', views.DVIOPTProductListCreateAPIView.as_view(), name='product-lc'),

    path('content/files/', views.ContentFileSaveAPIView.as_view(), name='content-files'),

    path('form-templates/questions/choices/<int:pk>/', views.FormTemplateQuestionChoiceRetrieveUpdateAPIView.as_view(),
         name='form-template-question-choice-rud'),
    path('form-templates/questions/choices/', views.FormTemplateQuestionChoiceCreateAPIView.as_view(),
         name='form-template-question-choice-create'),

    path('form-templates/<int:pk>/questions/', views.FormTemplateQuestionListAPIView.as_view(),
         name='form-template-question-list'),
    path('form-templates/questions/<int:pk>/', views.FormTemplateQuestionRetrieveUpdateAPIView.as_view(),
         name='form-template-question-rud'),
    path('form-templates/questions/', views.FormTemplateQuestionCreateAPIView.as_view(),
         name='form-template-question-create'),

    path('form-templates/<int:pk>/', views.FormTemplateRetrieveUpdateAPIView.as_view(), name='form-template-lc'),
    path('form-templates/', views.FormTemplateCreateListAPIView.as_view(), name='form-template-lc'),

    path('bug-reports/<int:pk>/', views.BugReportDestroyAPIView.as_view(), name='bug-report-destroy'),
    path('bug-reports/settings/', views.BugReportSettingUpdateAPIView.as_view(), name='bug-report-settings'),
    path('bug-reports/', views.BugReportListAPIView.as_view(), name='bug-report-list'),

    path('resource-policy/<int:pk>/', views.ResourcePolicyDetailAPIView.as_view(), name='resource-policy-retrieve'),
    path('resource-policy/', views.ResourcePolicyListCreateAPIView.as_view(), name='resource-policy-lc'),
]
