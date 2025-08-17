from django.urls import path

from api.client import views

app_name = 'dv-client'
urlpatterns = [
    path('update-products/', views.ProductParseFileView.as_view(), name='update-products'),
]
