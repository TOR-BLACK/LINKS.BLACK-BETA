from django.core.management.base import BaseCommand
from django.conf import settings
from apps.dv_info_site.models import Partnership
from core.service.translator import update_bulk_objects_translate
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Translate all Partnership records to configured languages'

    def handle(self, *args, **options):
        try:
            partnerships = Partnership.objects.all()
            count = partnerships.count()
            self.stdout.write(f"Found {count} partnerships to translate")
            
            # Get all languages except the source language (ru)
            target_languages = [lang[0] for lang in settings.LANGUAGES if lang[0] != 'ru']
            
            self.stdout.write(f"Starting translation to languages: {', '.join(target_languages)}")
            
            # Translate all partnerships
            update_bulk_objects_translate(
                partnerships,
                translate_fields=['title', 'description', 'short_description'],
                from_lang='ru'
            )
            
            self.stdout.write(self.style.SUCCESS(f'Successfully queued translations for {count} partnerships'))
            
        except Exception as e:
            logger.exception("Error during partnership translation")
            self.stdout.write(self.style.ERROR(f'Error during translation: {str(e)}'))
