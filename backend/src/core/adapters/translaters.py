from abc import ABC, abstractmethod

import deepl
from django.conf import settings
from django.core.cache import cache
from google.cloud import translate_v2 as google_translate
from google.oauth2 import service_account
from openai import OpenAI
import logging
import hashlib

logger = logging.getLogger(__name__)

class TranslatorAbstract(ABC):
    @abstractmethod
    def translate_text(self, text: str, to_language: str, from_language: str) -> str:
        raise NotImplementedError


class DeepLTranslator(TranslatorAbstract):
    # Маппинг для специальных случаев, когда нужно указать конкретный вариант языка
    LANG_MAPPING = {
        'en': 'en-gb',  # Используем британский английский по умолчанию
        'pt': 'pt-pt',  # Европейский португальский по умолчанию
        'zh': 'zh-hans'  # Упрощенный китайский по умолчанию
    }

    # Языки, которые поддерживает DeepL API
    SUPPORTED_LANGUAGES = {
        'ar', 'bg', 'cs', 'da', 'de', 'el', 'en', 'es', 'et', 'fi', 'fr', 'hu',
        'id', 'it', 'ja', 'ko', 'lt', 'lv', 'nb', 'nl', 'pl', 'pt', 'ro', 'ru',
        'sk', 'sl', 'sv', 'tr', 'uk', 'zh',
    }

    def get_cache_key(self, text: str, to_language: str, from_language: str) -> str:
        """Generate a cache key for the translation."""
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return f"translation:{text_hash}:{from_language}:{to_language}"

    def translate_text(self, text: str, to_language: str, from_language: str) -> str:
        logger.info(f"DeepL Translation started: text='{text}', to_language='{to_language}', from_language='{from_language}'")
        
        # If same language, return original
        if to_language == from_language:
            logger.info("Same language, returning original text")
            return text

        # Check cache first
        cache_key = self.get_cache_key(text, to_language, from_language)
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info("Retrieved translation from cache")
            return cached_result

        # Get base language
        base_language = to_language[:2].lower()
        logger.info(f"Base language detected: {base_language}")

        try:
            translator = deepl.Translator(settings.DEEPL_API_KEY)
            
            # Handle unsupported languages
            if base_language not in self.SUPPORTED_LANGUAGES:
                logger.warning(f"Language {base_language} not supported by DeepL, using en-gb instead")
                to_language = 'en-gb'
            elif base_language in self.LANG_MAPPING:
                to_language = self.LANG_MAPPING[base_language]
                logger.info(f"Using language mapping: {base_language} -> {to_language}")

            logger.info(f"Making DeepL API call with target_lang={to_language}")
            result = translator.translate_text(text, target_lang=to_language, source_lang=from_language)
            translated_text = result.text
            
            # Cache the result for 24 hours
            cache.set(cache_key, translated_text, timeout=86400)
            
            logger.info(f"Translation result: '{translated_text}'")
            return translated_text

        except deepl.exceptions.QuotaExceededException:
            logger.error("DeepL quota exceeded")
            # Return original text when quota is exceeded
            return text
        except Exception as e:
            logger.exception(f"DeepL translation error: {e}")
            return text


class GoogleTranslator(TranslatorAbstract):

    def translate_text(self, text: str, to_language: str, from_language: str) -> str:
        credentials = service_account.Credentials.from_service_account_info(
            settings.GOOGLE_OAUTH2_CREDENTIALS
        )
        translate_client = google_translate.Client(credentials=credentials)
        if to_language == from_language:
            return text
        result = translate_client.translate(
            text,
            target_language=to_language,
            source_language=from_language
        )
        return result['translatedText']


class OpenAITranslator(TranslatorAbstract):
    API_KEY = settings.OPENAI_API_KEY

    def translate_text(self, text: str, to_language: str, from_language: str) -> str:
        client = self.get_client()
        if to_language == from_language:
            return text
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Translate text to {to_language} from {from_language}"},
                {"role": "user", "content": text},
            ]
        )

        return response.choices[0].message.content

    def get_client(self) -> OpenAI:
        client = OpenAI(api_key=self.API_KEY)
        return client
