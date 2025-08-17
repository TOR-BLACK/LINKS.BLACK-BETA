import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.dv_info_site.model_utils import ContactType, ContactDepartment
from apps.dv_info_site.models import Contact
from tests.plugins.utils import get_test_image


@pytest.mark.django_db()
def test_create(
        api_client: APIClient,
        get_user_jwt,
        create_contact_factory,
):
    response = api_client.post(
        path=reverse('dv-admin:contact-lc'),
        data={
            'department': ContactDepartment.EMPLOYMENT,
            'person': 'Person',
            'person_avatar': get_test_image(),
            'telegram': 'telegram_nick',
            'element': 'element_nick',
            'session': 'session_nick',
        },
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    contact = Contact.objects.first()
    assert contact is not None
    assert contact.id == response.data['id']


@pytest.mark.django_db()
def test_list(
        api_client: APIClient,
        get_user_jwt,
        create_contact_factory,
):
    contact = create_contact_factory()
    response = api_client.get(
        path=reverse('dv-admin:contact-lc'),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert Contact.objects.count() == response.data['count']


@pytest.mark.django_db()
def test_detail(
        api_client: APIClient,
        get_user_jwt,
        create_contact_factory,
):
    contact = create_contact_factory()
    response = api_client.get(
        path=reverse('dv-admin:contact-rud', args=[contact.id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert contact.id == response.data['id']


@pytest.mark.django_db()
def test_update(
        api_client: APIClient,
        get_user_jwt,
        create_contact_factory,
):
    contact = create_contact_factory()
    update_person = 'Reno Test'
    update_telegram = 'update_telegram'
    update_element = 'update_element'
    update_session = 'update_session'
    update_department = ContactDepartment.OPT
    update_image = get_test_image()

    response = api_client.patch(
        path=reverse('dv-admin:contact-rud', args=[contact.id]),
        headers={
            'Authorization': get_user_jwt()
        },
        data={
            'department': update_department,
            'person': update_person,
            'person_avatar': update_image,
            'telegram': update_telegram,
            'element': update_element,
            'session': update_session,
        }
    )
    contact.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert contact.person == update_person
    assert contact.element == update_element
    assert contact.telegram == update_telegram
    assert contact.session == update_session
    assert contact.department == update_department


@pytest.mark.django_db()
def test_delete(
        api_client: APIClient,
        get_user_jwt,
        create_contact_factory,
):
    contact = create_contact_factory()
    contact_id = contact.id
    response = api_client.delete(
        path=reverse('dv-admin:contact-rud', args=[contact.id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    assert Contact.objects.filter(id=contact_id).first() is None
