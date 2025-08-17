import json
from rest_framework.renderers import JSONRenderer
from django.conf import settings
from django.utils.translation import override

class MultiLanguageJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        request = renderer_context.get('request')
        view = renderer_context.get('view')

        if request and request.headers.get('Accept-Language', '').strip().lower() == 'all':
            translations = {}

            for lang_code, _ in settings.LANGUAGES:
                with override(lang_code):
                    serializer = view.get_serializer(instance=view.get_queryset(), many=True)
                    translations[lang_code] = serializer.data

            return super().render(translations, accepted_media_type, renderer_context)

        return super().render(data, accepted_media_type, renderer_context)
