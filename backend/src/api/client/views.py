import base64
import logging

from django.conf import settings
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from loguru import logger
from sentry_sdk import capture_exception
from api.client import serializers


class ProductParseFileView(generics.CreateAPIView):
    """
    Авторизация:
    Authorization: Basic <Base64 encoded username and password>
    Структура данных файла:
    Excel файл:
    | Город | Название вариации товара | Цена товара | Название товара |
    Json файл:
    [{
    "city": <Город>,
    "product_item_title": <Название вариации товара>,
    "product_item_price": <Цена товара>,
    "product_title": <Название товара>
    }]
    """
    serializer_class = serializers.ProductUpdateFileCreateSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        if not self.is_valid_auth(request):
            raise AuthenticationFailed(detail='Authentication credentials were not provided.')
        return super().post(request, *args, **kwargs)

    def is_valid_auth(self, request) -> bool:
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if not auth_header:
                return False

            parts = auth_header.split()
            if len(parts) != 2:
                return False

            auth_type, credentials = parts
            client_credentials = f'{settings.DVI_CLIENT_AUTH["LOGIN"]}:{settings.DVI_CLIENT_AUTH["PASSWORD"]}'
            expected = base64.b64encode(client_credentials.encode()).decode()

            if auth_type == 'Basic' and credentials == expected:
                return True
            return False
        except Exception as e:
            logger.error(f"Authorization error: {e}")
            capture_exception(e)
            return False
