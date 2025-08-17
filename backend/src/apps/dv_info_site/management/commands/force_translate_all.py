from django.core.management.base import BaseCommand
from django.conf import settings
from apps.dv_info_site.models import (
    Partnership, Product, MainPageSlider, MainPageButtonBlock,
    MainPageReputationLink, FAQ, Vacancy
)
from core.service.translator import update_object_translate

MODELS_TO_TRANSLATE = {
    Partnership: ['title', 'description', 'short_description'],
    Product: ['title', 'description'],
    MainPageSlider: ['title', 'description'],
    MainPageButtonBlock: ['title', 'description'],
    MainPageReputationLink: ['title'],
    FAQ: ['question', 'answer'],
    Vacancy: ['title', 'short_description', 'description'],
}

class Command(BaseCommand):
    help = 'Force retranslate all content for all models'

    def handle(self, *args, **options):
        self.stdout.write('Starting force retranslation for all models...')
        
        total_objects = 0
        for model, fields in MODELS_TO_TRANSLATE.items():
            self.stdout.write(f'\nProcessing {model.__name__}...')
            objects = model.objects.all()
            count = objects.count()
            total_objects += count
            
            for obj in objects:
                # Clear all translations
                for field in fields:
                    for lang_code, _ in settings.LANGUAGES:
                        if lang_code != settings.MODELTRANSLATION_DEFAULT_LANGUAGE:
                            setattr(obj, f"{field}_{lang_code}", None)
                obj.save()
                
                # Force new translations
                update_object_translate(obj, translate_fields=fields)
                self.stdout.write(f'Queued translation for {model.__name__} {obj.id}')
            
            self.stdout.write(f'Processed {count} {model.__name__} objects')
        
        self.stdout.write(f'\nForce retranslation queued for {total_objects} objects in total!')
