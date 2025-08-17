import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.dv_info_site.models import MainPageSlider


# region SLIDER
@pytest.mark.django_db()
def test_create(
        api_client: APIClient,
        get_user_jwt,
        create_slider_factory,
):
    response = api_client.post(
        path=reverse('dv-admin:main-slider-lc'),
        data={
            'title': 'Название тестового слайдера',
            'description': 'Описание тестового слайдера'
        },
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    slider = MainPageSlider.objects.first()
    assert slider is not None
    for lang, _ in settings.LANGUAGES:
        assert getattr(slider, f'title_{lang}') is not None
        assert getattr(slider, f'description_{lang}') is not None

    create_slider_factory()
    create_slider_factory()
    create_slider_factory()
    create_slider_factory()
    response = api_client.post(
        path=reverse('dv-admin:main-slider-lc'),
        data={
            'title': 'Название тестового слайдера',
            'description': 'Описание тестового слайдера'
        },
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db()
def test_list(
        api_client: APIClient,
        get_user_jwt,
        create_slider_factory,
):
    slider = create_slider_factory()
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:main-slider-lc'),
            headers={
                'Accept-Language': lang,
                'Authorization': get_user_jwt()
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert MainPageSlider.objects.count() == len(response.data)
        assert response.data[0]['title'] == getattr(slider, f'title_{lang}')
        assert response.data[0]['description'] == getattr(slider, f'description_{lang}')


@pytest.mark.django_db()
def test_detail(
        api_client: APIClient,
        get_user_jwt,
        create_slider_factory,
):
    slider = create_slider_factory()
    response = api_client.get(
        path=reverse('dv-admin:main-slider-rud', args=[slider.id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert slider.id == response.data['id']


@pytest.mark.django_db()
def test_update(
        api_client: APIClient,
        get_user_jwt,
        create_slider_factory,
):
    slider = create_slider_factory()
    update_title = 'Обновленное название'
    update_description = 'Обновленное описание'
    response = api_client.patch(
        path=reverse('dv-admin:main-slider-rud', args=[slider.id]),
        headers={
            'Authorization': get_user_jwt()
        },
        data={
            'title': update_title,
            'description': update_description,
        }
    )
    slider.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert slider.title == update_title
    assert slider.description == update_description
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:main-slider-rud', args=[slider.id]),
            headers={
                'Authorization': get_user_jwt(),
                'Accept-Language': lang
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert slider.id == response.data['id']
        assert response.data['title'] == getattr(slider, f'title_{lang}')
        assert response.data['description'] == getattr(slider, f'description_{lang}')


@pytest.mark.django_db()
def test_delete(
        api_client: APIClient,
        get_user_jwt,
        create_slider_factory,
):
    slider = create_slider_factory()
    slider_id = slider.id
    response = api_client.delete(
        path=reverse('dv-admin:main-slider-rud', args=[slider.id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    assert MainPageSlider.objects.filter(id=slider_id).first() is None

# endregion
