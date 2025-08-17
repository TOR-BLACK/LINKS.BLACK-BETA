import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.dv_info_site.models import MainPageButtonBlock
from tests.plugins.utils import get_test_file


@pytest.mark.django_db()
def test_create(
        api_client: APIClient,
        get_user_jwt
):
    response = api_client.post(
        path=reverse('dv-admin:main-button-block-lc'),
        data={
            'title': 'Название тестового кнопки',
            'description': 'Описание тестового слайдера',
            'background_image': get_test_file(),
            'link': 'https://google.com'
        },

        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    button = MainPageButtonBlock.objects.first()
    assert button is not None
    for lang, _ in settings.LANGUAGES:
        assert getattr(button, f'title_{lang}') is not None
        assert getattr(button, f'description_{lang}') is not None


@pytest.mark.django_db()
def test_list(
        api_client: APIClient,
        get_user_jwt,
        create_button_block_factory,
):
    button = create_button_block_factory()
    response = api_client.get(
        path=reverse('dv-admin:main-button-block-lc'),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert MainPageButtonBlock.objects.all().count() == len(response.data)
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:main-button-block-lc'),
            headers={
                'Accept-Language': lang,
                'Authorization': get_user_jwt()
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert response.data[0]['title'] == getattr(button, f'title_{lang}')
        assert response.data[0]['description'] == getattr(button, f'description_{lang}')


@pytest.mark.django_db()
def test_detail(
        api_client: APIClient,
        get_user_jwt,
        create_button_block_factory,
):
    button = create_button_block_factory()
    response = api_client.get(
        path=reverse('dv-admin:main-button-block-rud', args=[button.id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert button.id == response.data['id']


@pytest.mark.django_db()
def test_update(
        api_client: APIClient,
        get_user_jwt,
        create_button_block_factory,
):
    button = create_button_block_factory()
    update_title = 'Обновленное название'
    update_description = 'Обновленное описание'
    update_link = 'https://update-link.com'
    update_file = get_test_file()

    response = api_client.patch(
        path=reverse('dv-admin:main-button-block-rud', args=[button.id]),
        headers={
            'Authorization': get_user_jwt()
        },
        data={
            'title': update_title,
            'description': update_description,
            'link': update_link,
            'file': update_file
        }
    )
    button.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert button.title == update_title
    assert button.description == update_description
    assert button.link == update_link

    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:main-button-block-rud', args=[button.id]),
            headers={
                'Authorization': get_user_jwt(),
                'Accept-Language': lang
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert button.id == response.data['id']
        assert response.data['title'] == getattr(button, f'title_{lang}')
        assert response.data['description'] == getattr(button, f'description_{lang}')
        assert response.data['link'] == button.link


@pytest.mark.django_db()
def test_delete(
        api_client: APIClient,
        get_user_jwt,
        create_button_block_factory,
):
    button = create_button_block_factory()
    button_id = button.id
    response = api_client.delete(
        path=reverse('dv-admin:main-button-block-rud', args=[button_id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    assert MainPageButtonBlock.objects.filter(id=button_id).first() is None
