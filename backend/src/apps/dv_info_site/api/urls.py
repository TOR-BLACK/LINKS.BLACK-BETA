from django.urls import path
from .views import force_update_translations

urlpatterns = [
    path('force-update-translations/', force_update_translations, name='force-update-translations'),
]
