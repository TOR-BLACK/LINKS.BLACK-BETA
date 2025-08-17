from django.conf import settings
from django.urls import include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.da_vinci_info_site import urls as da_vinci_info_site_urls
from api.dv_admin import urls as dv_admin_urls
from api.client import urls as client_urls

da_vinci_site_info_schema = get_schema_view(
    openapi.Info(
        title='DA VINCI INFO SITE API DOCUMENTATION',
        default_version='v1',
        description=f"""
        Во всех апи нужно отправлять в хедере Accept-Language
        Доступные языки: {','.join(lang[0] for lang in settings.LANGUAGES)}
        """
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=[
        re_path(r'api/v1/dvi/', include(da_vinci_info_site_urls)),
    ],
    url=settings.SWAGGER_API_URL,

)

da_vinci_admin_schema = get_schema_view(
    openapi.Info(
        title='DA VINCI ADMIN PANEL API DOCUMENTATION',
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=[
        re_path(r'api/v1/dv-admin/', include(dv_admin_urls)),
    ],
    url=settings.SWAGGER_API_URL
)

da_vinci_client_schema = get_schema_view(
    openapi.Info(
        title='DA VINCI CLIENT API DOCUMENTATION',
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=[
        re_path(r'api/v1/dv-client/', include(client_urls)),
    ],
    url=settings.SWAGGER_API_URL
)
