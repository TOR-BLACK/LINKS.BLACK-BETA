import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.dv_info_site.model_utils import ContactType
from apps.dv_info_site.models import Contact, DVInstruction
from tests.plugins.utils import get_test_image


@pytest.mark.django_db()
def test_create(
        api_client: APIClient,
        get_user_jwt,
        create_dv_instruction_factory,
):
    response = api_client.post(
        path=reverse('dv-admin:dv-instruction-lc'),
        data={
            'title': 'Тестовое название',
            'description': 'Тестовое описание',
            'icon': get_test_image(),
        },
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    dv_instruction = DVInstruction.objects.first()
    assert dv_instruction is not None
    for lang, _ in settings.LANGUAGES:
        assert getattr(dv_instruction, f'title_{lang}') is not None
        assert getattr(dv_instruction, f'description_{lang}') is not None


@pytest.mark.django_db()
def test_list(
        api_client: APIClient,
        get_user_jwt,
        create_dv_instruction_factory,
):
    dv_instruction = create_dv_instruction_factory()
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:dv-instruction-lc'),
            headers={
                'Accept-Language': lang,
                'Authorization': get_user_jwt()
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert DVInstruction.objects.count() == response.data['count']
        assert response.data['results'][0]['title'] == getattr(dv_instruction, f'title_{lang}')
        assert response.data['results'][0]['description'] == getattr(dv_instruction, f'description_{lang}')


@pytest.mark.django_db()
def test_detail(
        api_client: APIClient,
        get_user_jwt,
        create_dv_instruction_factory,
):
    dv_instruction = create_dv_instruction_factory()
    response = api_client.get(
        path=reverse('dv-admin:dv-instruction-rud', args=[dv_instruction.id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert dv_instruction.id == response.data['id']


@pytest.mark.django_db()
def test_update(
        api_client: APIClient,
        get_user_jwt,
        create_dv_instruction_factory,
):
    dv_instruction = create_dv_instruction_factory()
    update_title = 'Обновленное название'
    update_description = 'Обновленное описание'

    response = api_client.patch(
        path=reverse('dv-admin:dv-instruction-rud', args=[dv_instruction.id]),
        headers={
            'Authorization': get_user_jwt()
        },
        data={
            'title': update_title,
            'description': update_description,
            'icon': get_test_image(),
        }
    )
    dv_instruction.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert dv_instruction.title == update_title
    assert dv_instruction.description == update_description

    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:dv-instruction-rud', args=[dv_instruction.id]),
            headers={
                'Authorization': get_user_jwt(),
                'Accept-Language': lang
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert dv_instruction.id == response.data['id']
        assert response.data['title'] == getattr(dv_instruction, f'title_{lang}')
        assert response.data['description'] == getattr(dv_instruction, f'description_{lang}')


@pytest.mark.django_db()
def test_delete(
        api_client: APIClient,
        get_user_jwt,
        create_dv_instruction_factory,
):
    dv_instruction = create_dv_instruction_factory()
    dv_instruction_id = dv_instruction.id
    response = api_client.delete(
        path=reverse('dv-admin:dv-instruction-rud', args=[dv_instruction_id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    assert DVInstruction.objects.filter(id=dv_instruction_id).first() is None
