import os

from celery import Celery
from kombu import Exchange, Queue

DEFAULT_QUEUE = 'default'
PARSE_PRODUCT_QUEUE = 'parse_product'
TRANSLATE_SERVICE_QUEUE = 'translate_service'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('dv_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.task_queues = (
    Queue(DEFAULT_QUEUE, Exchange(DEFAULT_QUEUE), routing_key=DEFAULT_QUEUE),
    Queue(PARSE_PRODUCT_QUEUE, Exchange(PARSE_PRODUCT_QUEUE), routing_key=PARSE_PRODUCT_QUEUE),
    Queue(TRANSLATE_SERVICE_QUEUE, Exchange(TRANSLATE_SERVICE_QUEUE), routing_key=TRANSLATE_SERVICE_QUEUE),
)

app.conf.task_default_queue = DEFAULT_QUEUE
app.conf.task_default_exchange_type = 'direct'
app.conf.task_default_routing_key = DEFAULT_QUEUE

# app.conf.beat_schedule = {
#
# }
