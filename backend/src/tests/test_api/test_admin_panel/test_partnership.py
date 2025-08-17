import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.dv_info_site.models import Partnership
from tests.plugins.utils import get_test_image


@pytest.mark.django_db()
def test_create(
        api_client: APIClient,
        get_user_jwt,
        create_partnership_factory,
):
    response = api_client.post(
        path=reverse('dv-admin:partnership-lc'),
        data={
            'title': 'Тестовое название',
            'description': 'Тестовое описание',
            'image': get_test_image(),
        },
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    partnership = Partnership.objects.first()
    assert partnership is not None
    for lang, _ in settings.LANGUAGES:
        assert getattr(partnership, f'title_{lang}') is not None
        assert getattr(partnership, f'description_{lang}') is not None


@pytest.mark.django_db()
def test_list(
        api_client: APIClient,
        get_user_jwt,
        create_partnership_factory,
):
    partnership = create_partnership_factory()
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:partnership-lc'),
            headers={
                'Accept-Language': lang,
                'Authorization': get_user_jwt()
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert Partnership.objects.count() == response.data['count']
        assert response.data['results'][0]['title'] == getattr(partnership, f'title_{lang}')
        assert response.data['results'][0]['description'] == getattr(partnership, f'description_{lang}')


@pytest.mark.django_db()
def test_detail(
        api_client: APIClient,
        get_user_jwt,
        create_partnership_factory,
):
    partnership = create_partnership_factory()
    response = api_client.get(
        path=reverse('dv-admin:partnership-rud', args=[partnership.id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert partnership.id == response.data['id']


@pytest.mark.django_db()
def test_update(
        api_client: APIClient,
        get_user_jwt,
        create_partnership_factory,
):
    partnership = create_partnership_factory()
    update_title = 'Обновленное название'
    update_description = 'Обновленное описание'

    response = api_client.patch(
        path=reverse('dv-admin:partnership-rud', args=[partnership.id]),
        headers={
            'Authorization': get_user_jwt()
        },
        data={
            'title': update_title,
            'description': update_description,
            'image': get_test_image()
        }
    )
    partnership.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert partnership.title == update_title
    assert partnership.description == update_description

    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:partnership-rud', args=[partnership.id]),
            headers={
                'Authorization': get_user_jwt(),
                'Accept-Language': lang
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert partnership.id == response.data['id']
        assert response.data['title'] == getattr(partnership, f'title_{lang}')
        assert response.data['description'] == getattr(partnership, f'description_{lang}')


@pytest.mark.django_db()
def test_delete(
        api_client: APIClient,
        get_user_jwt,
        create_partnership_factory,
):
    partnership = create_partnership_factory()
    partnership_id = partnership.id
    response = api_client.delete(
        path=reverse('dv-admin:partnership-rud', args=[partnership_id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    assert Partnership.objects.filter(id=partnership_id).first() is None
