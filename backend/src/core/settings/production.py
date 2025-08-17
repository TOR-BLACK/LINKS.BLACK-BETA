import sentry_sdk
from loguru import logger
from sentry_sdk.integrations.django import DjangoIntegration

from core.settings.base import *

SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(' ')

MEDIA_URL = '/media/'
MEDIA_ROOT = Path(BASE_DIR).joinpath('media')
STATIC_URL = '/static/'
STATIC_ROOT = Path(BASE_DIR).joinpath('static')

logger.add(f'{BASE_DIR}/logs/project/info.log', level='INFO', rotation='00:00', compression='zip')

SENTRY_DSN = os.environ.get('SENTRY_DSN', None)
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=1.0,
        integrations=[DjangoIntegration()],
        environment='production',
    )
