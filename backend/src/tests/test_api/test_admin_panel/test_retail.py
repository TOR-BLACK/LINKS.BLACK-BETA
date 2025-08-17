import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.dv_info_site.models import Retail


@pytest.mark.django_db()
def test_create(
        api_client: APIClient,
        get_user_jwt,
        create_retail_factory,
):
    response = api_client.post(
        path=reverse('dv-admin:retail-lc'),
        data={
            'name': 'Тестовое название',
            'link': 'https://test.com',
            'link_type': 'link_type'
        },
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    retail = Retail.objects.first()
    assert retail is not None
    assert retail.id == response.data['id']


@pytest.mark.django_db()
def test_list(
        api_client: APIClient,
        get_user_jwt,
        create_retail_factory,
):
    retail = create_retail_factory()
    response = api_client.get(
        path=reverse('dv-admin:retail-lc'),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert Retail.objects.count() == response.data['count']


@pytest.mark.django_db()
def test_detail(
        api_client: APIClient,
        get_user_jwt,
        create_retail_factory,
):
    retail = create_retail_factory()
    response = api_client.get(
        path=reverse('dv-admin:retail-rud', args=[retail.id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert retail.id == response.data['id']


@pytest.mark.django_db()
def test_update(
        api_client: APIClient,
        get_user_jwt,
        create_retail_factory,
):
    retail = create_retail_factory()
    update_name = 'Обновленное название'
    update_link = 'https://test2.com'
    update_link_type = 'link_type_test'

    response = api_client.patch(
        path=reverse('dv-admin:retail-rud', args=[retail.id]),
        headers={
            'Authorization': get_user_jwt()
        },
        data={
            'name': update_name,
            'link': update_link,
            'link_type': update_link_type,
        }
    )
    retail.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert retail.name == update_name
    assert retail.link == update_link
    assert retail.link_type == update_link_type


@pytest.mark.django_db()
def test_delete(
        api_client: APIClient,
        get_user_jwt,
        create_retail_factory,
):
    retail = create_retail_factory()
    retail_id = retail.id
    response = api_client.delete(
        path=reverse('dv-admin:retail-rud', args=[retail_id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    assert Retail.objects.filter(id=retail_id).first() is None
