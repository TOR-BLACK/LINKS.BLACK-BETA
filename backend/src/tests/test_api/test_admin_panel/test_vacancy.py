from decimal import Decimal

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.dv_info_site.models import Vacancy
from tests.plugins.utils import get_test_image


# region SLIDER
@pytest.mark.django_db()
def test_create(
        api_client: APIClient,
        get_user_jwt,
        create_vacancy_factory,
):
    response = api_client.post(
        path=reverse('dv-admin:vacancy-lc'),
        data={
            'title': 'Название тестового слайдера',
            'description': 'Описание тестового слайдера',
            'short_description': 'Описание тестового слайдера',
            'image': get_test_image(),
            'salary_calc': True,
            'salary': Decimal(100000),
            'is_active': True
        },
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    vacancy = Vacancy.objects.first()
    assert vacancy is not None
    for lang, _ in settings.LANGUAGES:
        assert getattr(vacancy, f'title_{lang}') is not None
        assert getattr(vacancy, f'description_{lang}') is not None
        assert getattr(vacancy, f'short_description_{lang}') is not None


@pytest.mark.django_db()
def test_list(
        api_client: APIClient,
        get_user_jwt,
        create_vacancy_factory,
):
    vacancy = create_vacancy_factory()
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:vacancy-lc'),
            headers={
                'Accept-Language': lang,
                'Authorization': get_user_jwt()
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert Vacancy.objects.count() == len(response.data)
        assert response.data[0]['title'] == getattr(vacancy, f'title_{lang}')
        assert response.data[0]['description'] == getattr(vacancy, f'description_{lang}')
        assert response.data[0]['short_description'] == getattr(vacancy, f'short_description_{lang}')


@pytest.mark.django_db()
def test_detail(
        api_client: APIClient,
        get_user_jwt,
        create_vacancy_factory,
):
    vacancy = create_vacancy_factory()
    response = api_client.get(
        path=reverse('dv-admin:vacancy-rud', args=[vacancy.id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert vacancy.id == response.data['id']


@pytest.mark.django_db()
def test_update(
        api_client: APIClient,
        get_user_jwt,
        create_vacancy_factory,
):
    vacancy = create_vacancy_factory()
    update_title = 'Обновленное название'
    update_description = 'Обновленное описание'
    update_short_description = 'Обновленное описание'
    update_salary = Decimal(999999)
    update_is_active = False
    update_salary_calc = False

    response = api_client.patch(
        path=reverse('dv-admin:vacancy-rud', args=[vacancy.id]),
        headers={
            'Authorization': get_user_jwt()
        },
        data={
            'title': update_title,
            'description': update_description,
            'short_description': update_short_description,
            'salary': update_salary,
            'is_active': update_is_active,
            'salary_calc': update_salary_calc,
            'image': get_test_image()
        }
    )
    vacancy.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert vacancy.title == update_title
    assert vacancy.description == update_description
    assert vacancy.short_description == update_short_description
    assert vacancy.salary == update_salary
    assert vacancy.is_active == update_is_active
    assert vacancy.salary_calc == update_salary_calc

    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:vacancy-rud', args=[vacancy.id]),
            headers={
                'Authorization': get_user_jwt(),
                'Accept-Language': lang
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert vacancy.id == response.data['id']
        assert response.data['title'] == getattr(vacancy, f'title_{lang}')
        assert response.data['description'] == getattr(vacancy, f'description_{lang}')
        assert response.data['short_description'] == getattr(vacancy, f'short_description_{lang}')


@pytest.mark.django_db()
def test_delete(
        api_client: APIClient,
        get_user_jwt,
        create_vacancy_factory,
):
    vacancy = create_vacancy_factory()
    vacancy_id = vacancy.id
    response = api_client.delete(
        path=reverse('dv-admin:vacancy-rud', args=[vacancy_id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    assert Vacancy.objects.filter(id=vacancy_id).first() is None

# endregion
