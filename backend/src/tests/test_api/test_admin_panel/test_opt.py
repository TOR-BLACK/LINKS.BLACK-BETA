import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.dv_info_site.models import Country, City
from tests.plugins.dv_info_site.factories import create_country_fixture
from tests.plugins.utils import get_test_image


@pytest.mark.django_db()
def test_country_create(
        api_client: APIClient,
        get_user_jwt
):
    response = api_client.post(
        path=reverse('dv-admin:opt-country-lc'),
        data={
            'name': 'Россия',
            'code': 'ru',
            'is_active': True
        },

        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    country = Country.objects.first()
    assert country is not None
    for lang, _ in settings.LANGUAGES:
        assert getattr(country, f'name_{lang}') is not None


@pytest.mark.django_db()
def test_country_list(
        api_client: APIClient,
        get_user_jwt,
        create_country_fixture,
):
    country = create_country_fixture()
    response = api_client.get(
        path=reverse('dv-admin:opt-country-lc'),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert Country.objects.all().count() == response.data['count']
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:opt-country-lc'),
            headers={
                'Accept-Language': lang,
                'Authorization': get_user_jwt()
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert response.data['results'][0]['name'] == getattr(country, f'name_{lang}')


@pytest.mark.django_db()
def test_country_detail(
        api_client: APIClient,
        get_user_jwt,
        create_country_fixture,
):
    country = create_country_fixture()
    response = api_client.get(
        path=reverse('dv-admin:opt-country-rud', args=[country.id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert country.id == response.data['id']


@pytest.mark.django_db()
def test_country_update(
        api_client: APIClient,
        get_user_jwt,
        create_country_fixture,
):
    country = create_country_fixture()
    update_name = 'Казахстан'
    update_code = 'kz'
    update_is_active = False

    response = api_client.patch(
        path=reverse('dv-admin:opt-country-rud', args=[country.id]),
        headers={
            'Authorization': get_user_jwt()
        },
        data={
            'name': update_name,
            'code': update_code,
            'is_active': update_is_active
        }
    )
    country.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert country.name == update_name
    assert country.code == update_code
    assert country.is_active == update_is_active

    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:opt-country-rud', args=[country.id]),
            headers={
                'Authorization': get_user_jwt(),
                'Accept-Language': lang
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert country.id == response.data['id']
        assert response.data['name'] == getattr(country, f'name_{lang}')


@pytest.mark.django_db()
def test_country_delete(
        api_client: APIClient,
        get_user_jwt,
        create_country_fixture,
):
    country = create_country_fixture()
    country_id = country.id
    response = api_client.delete(
        path=reverse('dv-admin:opt-country-rud', args=[country_id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    assert Country.objects.filter(id=country_id).first() is None


@pytest.mark.django_db()
def test_city_create(
        api_client: APIClient,
        get_user_jwt,
        create_country_fixture
):
    country = create_country_fixture()
    response = api_client.post(
        path=reverse('dv-admin:opt-city-create'),
        data={
            'name': 'Москва',
            'country': country.pk,
            'is_active': True
        },

        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    city = City.objects.first()
    assert city is not None
    for lang, _ in settings.LANGUAGES:
        assert getattr(city, f'name_{lang}') is not None


@pytest.mark.django_db()
def test_city_detail(
        api_client: APIClient,
        get_user_jwt,
        create_city_fixture,
):
    city = create_city_fixture()
    response = api_client.get(
        path=reverse('dv-admin:opt-city-rud', args=[city.id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert city.id == response.data['id']


@pytest.mark.django_db()
def test_city_update(
        api_client: APIClient,
        get_user_jwt,
        create_city_fixture,
):
    city = create_city_fixture()
    update_name = 'Алматы'
    update_is_active = False

    response = api_client.patch(
        path=reverse('dv-admin:opt-city-rud', args=[city.id]),
        headers={
            'Authorization': get_user_jwt()
        },
        data={
            'name': update_name,
            'is_active': update_is_active
        }
    )
    city.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert city.name == update_name
    assert city.is_active == update_is_active

    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:opt-city-rud', args=[city.id]),
            headers={
                'Authorization': get_user_jwt(),
                'Accept-Language': lang
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert city.id == response.data['id']
        assert response.data['name'] == getattr(city, f'name_{lang}')


@pytest.mark.django_db()
def test_city_delete(
        api_client: APIClient,
        get_user_jwt,
        create_city_fixture,
):
    city = create_city_fixture()
    city_id = city.id
    response = api_client.delete(
        path=reverse('dv-admin:opt-city-rud', args=[city_id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    assert City.objects.filter(id=city_id).first() is None


