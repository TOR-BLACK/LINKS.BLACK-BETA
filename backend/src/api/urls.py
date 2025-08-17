from django.conf import settings
from django.urls import include, path, re_path

from api.swagger import da_vinci_site_info_schema, da_vinci_admin_schema, da_vinci_client_schema

urlpatterns = [
    path('dvi/', include('api.da_vinci_info_site.urls')),
    path('dv-admin/', include('api.dv_admin.urls')),
    path('dv-client/', include('api.client.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^dvi-docs/$", da_vinci_site_info_schema.with_ui('swagger', cache_timeout=0),
            name='dvi-schema-swagger',
        ),
        re_path(
            r"^dv-admin-docs/$", da_vinci_admin_schema.with_ui('swagger', cache_timeout=0),
            name='dv-admin-schema-swagger',
        ),
        re_path(
            r"^dv-client-docs/$", da_vinci_client_schema.with_ui('swagger', cache_timeout=0),
            name='dv-client-schema-swagger',
        ),

    ]
