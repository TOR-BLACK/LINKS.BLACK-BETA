import pytest
import random
from django.core.cache import caches
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.conf import LazySettings
    from django.core.cache import BaseCache


@pytest.fixture(autouse=True)
def _sync_processing_celery_task(settings: 'LazySettings') -> None:
    """ Sets TEST_BASE_URL for files """
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True

@pytest.fixture(autouse=True)
def _media_root(
        settings: 'LazySettings',
        tmpdir_factory: pytest.TempPathFactory,
) -> None:
    """Forces django to save media and static files into temp folder."""
    settings.MEDIA_ROOT = tmpdir_factory.mktemp('media', numbered=True)
    settings.STATIC_ROOT = tmpdir_factory.mktemp('static', numbered=True)
