from django.db.models import Prefetch
from django_filters import rest_framework as filters

from apps.dv_info_site.models import Product, ProductItem
from core.generics.filters import NumberInFilter


class OPTProductListFilter(filters.FilterSet):
    country = filters.NumberFilter(method='filter_country')
    cities = NumberInFilter(field_name='items__city', lookup_expr='in')
    availability = filters.CharFilter(field_name='items__availability_status')

    class Meta:
        model = Product
        fields = (
            'country', 'cities', 'availability'
        )

    def get_filtered_items_queryset(self):
        """Получаем отфильтрованный queryset для items"""
        items_queryset = ProductItem.objects.select_related('city')
        
        if 'country' in self.data:
            items_queryset = items_queryset.filter(city__country=self.data['country'])
            
        if 'cities' in self.data:
            cities = self.data.getlist('cities')[0].split(',')  # Разбиваем строку с городами на список
            items_queryset = items_queryset.filter(city_id__in=cities)
        
        if 'availability' in self.data:
            items_queryset = items_queryset.filter(availability_status=self.data['availability'])
            
        return items_queryset

    def filter_queryset(self, queryset):
        """Переопределяем основной метод фильтрации"""
        queryset = super().filter_queryset(queryset)
        
        if 'country' in self.data or 'cities' in self.data or 'availability' in self.data:
            items_queryset = self.get_filtered_items_queryset()
            queryset = queryset.prefetch_related(
                'images',
                Prefetch('items', queryset=items_queryset)
            )
        
        return queryset.distinct()

    def filter_country(self, queryset, name, value):
        return queryset
