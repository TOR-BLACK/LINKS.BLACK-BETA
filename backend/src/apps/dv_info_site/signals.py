from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps
import threading
import requests

import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv('SIGNAL_API_URL', '#')

def send_api_signal(instance, action):
    def _send():
        try:
            requests.get(API_URL)
        except Exception as e:
            print(f"[Signal Error] Failed to send GET request: {e}")

    if API_URL != "#":
        threading.Thread(target=_send).start()

def handle_post_save(sender, instance, created, **kwargs):
    send_api_signal(instance, 'created' if created else 'updated')

def handle_post_delete(sender, instance, **kwargs):
    send_api_signal(instance, 'deleted')

def connect_signals_to_all_models():
    for model in apps.get_models():
        post_save.connect(handle_post_save, sender=model, dispatch_uid=f"{model.__name__}_post_save")
        post_delete.connect(handle_post_delete, sender=model, dispatch_uid=f"{model.__name__}_post_delete")
