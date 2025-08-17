from django.utils import timezone
from rest_framework import serializers
from apps.dv_info_site.services.product_parsing import processing_product_update_file

from apps.dv_info_site.models import ProductUpdateFile


class ProductUpdateFileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUpdateFile
        fields = (
            'id', 'file', 'status', 'update_date', 'file_type'
        )
        read_only_fields = ('status', 'update_date')

    def create(self, validated_data):
        validated_data['update_date'] = timezone.now().date()  # TODO нужно уточнить будут ли отправлять дату или
        instance = super().create(validated_data)
        processing_product_update_file(instance.id)
        return instance
