import logging
from django.utils.translation import get_language
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class LanguageLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        accept_language = request.headers.get('Accept-Language')
        logger.info(f"Requested Accept-Language header: {accept_language}")
        logger.info(f"Django detected language: {get_language()}")
        return None

    def process_response(self, request, response):
        logger.info(f"Response Content-Language: {response.get('Content-Language', 'Not set')}")
        return response
