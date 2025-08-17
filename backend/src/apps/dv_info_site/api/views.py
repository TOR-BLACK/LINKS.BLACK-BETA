from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication

from apps.dv_info_site.models import Country, City
from core.service.translator import update_object_translate


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def force_update_translations(request):
    """
    Force update translations for all countries and cities
    Only accessible by admin users
    
    Authentication:
    - Use Basic Auth with admin username and password
    """
    try:
        # Update all countries
        countries = Country.objects.all()
        for country in countries:
            update_object_translate(country, force_update=True)
            
            # Update cities for this country
            cities = City.objects.filter(country=country)
            for city in cities:
                update_object_translate(city, force_update=True)
        
        return Response({
            'status': 'success',
            'message': f'Started translation update for {countries.count()} countries and their cities'
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
