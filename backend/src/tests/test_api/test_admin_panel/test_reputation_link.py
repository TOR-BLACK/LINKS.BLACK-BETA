import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.dv_info_site.models import MainPageReputationLink
from tests.plugins.utils import get_test_image


# region REPUTATION LINK

@pytest.mark.django_db()
def test_create(
        api_client: APIClient,
        get_user_jwt
):
    response = api_client.post(
        path=reverse('dv-admin:main-reputation-link-lc'),
        data={
            'title': 'Название тестового кнопки',
            'image': get_test_image(),
            'link': 'https://google.com'
        },

        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    link = MainPageReputationLink.objects.first()
    assert link is not None
    for lang, _ in settings.LANGUAGES:
        assert getattr(link, f'title_{lang}') is not None


@pytest.mark.django_db()
def test_list(
        api_client: APIClient,
        get_user_jwt,
        create_reputation_link_factory,
):
    link = create_reputation_link_factory()
    response = api_client.get(
        path=reverse('dv-admin:main-reputation-link-lc'),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert MainPageReputationLink.objects.all().count() == len(response.data)
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:main-reputation-link-lc'),
            headers={
                'Accept-Language': lang,
                'Authorization': get_user_jwt()
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert response.data[0]['title'] == getattr(link, f'title_{lang}')


@pytest.mark.django_db()
def test_detail(
        api_client: APIClient,
        get_user_jwt,
        create_reputation_link_factory,
):
    link = create_reputation_link_factory()
    response = api_client.get(
        path=reverse('dv-admin:main-reputation-link-rud', args=[link.id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert link.id == response.data['id']


@pytest.mark.django_db()
def test_update(
        api_client: APIClient,
        get_user_jwt,
        create_reputation_link_factory,
):
    link = create_reputation_link_factory()
    update_title = 'Обновленное название'
    update_link = 'https://update-link.com'
    update_image = get_test_image()

    response = api_client.patch(
        path=reverse('dv-admin:main-reputation-link-rud', args=[link.id]),
        headers={
            'Authorization': get_user_jwt()
        },
        data={
            'title': update_title,
            'link': update_link,
            'image': update_image
        }
    )
    link.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert link.title == update_title
    assert link.link == update_link

    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:main-reputation-link-rud', args=[link.id]),
            headers={
                'Authorization': get_user_jwt(),
                'Accept-Language': lang
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert link.id == response.data['id']
        assert response.data['title'] == getattr(link, f'title_{lang}')


@pytest.mark.django_db()
def test_delete(
        api_client: APIClient,
        get_user_jwt,
        create_reputation_link_factory,
):
    link = create_reputation_link_factory()
    link_id = link.id
    response = api_client.delete(
        path=reverse('dv-admin:main-reputation-link-rud', args=[link_id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    assert MainPageReputationLink.objects.filter(id=link_id).first() is None

# endregion
