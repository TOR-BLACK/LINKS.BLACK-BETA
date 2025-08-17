import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.dv_info_site.models import FAQ
from tests.plugins.utils import get_test_image


# region SLIDER
@pytest.mark.django_db()
def test_create(
        api_client: APIClient,
        get_user_jwt,
        create_faq_factory,
):
    response = api_client.post(
        path=reverse('dv-admin:faq-lc'),
        data={
            'question': 'Тестовый вопрос',
            'answer': 'Тестовый ответ',
            'image': get_test_image(),
            'position': 1
        },
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    faq = FAQ.objects.first()
    assert faq is not None
    for lang, _ in settings.LANGUAGES:
        assert getattr(faq, f'question_{lang}') is not None
        assert getattr(faq, f'answer_{lang}') is not None


@pytest.mark.django_db()
def test_list(
        api_client: APIClient,
        get_user_jwt,
        create_faq_factory,
):
    faq = create_faq_factory()
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:faq-lc'),
            headers={
                'Accept-Language': lang,
                'Authorization': get_user_jwt()
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert FAQ.objects.count() == response.data['count']
        assert response.data['results'][0]['answer'] == getattr(faq, f'answer_{lang}')
        assert response.data['results'][0]['question'] == getattr(faq, f'question_{lang}')


@pytest.mark.django_db()
def test_detail(
        api_client: APIClient,
        get_user_jwt,
        create_faq_factory,
):
    faq = create_faq_factory()
    response = api_client.get(
        path=reverse('dv-admin:faq-rud', args=[faq.id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert faq.id == response.data['id']


@pytest.mark.django_db()
def test_update(
        api_client: APIClient,
        get_user_jwt,
        create_faq_factory,
):
    faq = create_faq_factory()
    update_answer = 'Обновленный ответ'
    update_question = 'Обновленное вопрос'
    update_position = 2

    response = api_client.patch(
        path=reverse('dv-admin:faq-rud', args=[faq.id]),
        headers={
            'Authorization': get_user_jwt()
        },
        data={
            'answer': update_answer,
            'question': update_question,
            'position': update_position,
            'image': get_test_image()
        }
    )
    faq.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert faq.answer == update_answer
    assert faq.question == update_question
    assert faq.position == update_position

    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:faq-rud', args=[faq.id]),
            headers={
                'Authorization': get_user_jwt(),
                'Accept-Language': lang
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert faq.id == response.data['id']
        assert response.data['answer'] == getattr(faq, f'answer_{lang}')
        assert response.data['question'] == getattr(faq, f'question_{lang}')


@pytest.mark.django_db()
def test_delete(
        api_client: APIClient,
        get_user_jwt,
        create_faq_factory,
):
    faq = create_faq_factory()
    faq_id = faq.id
    response = api_client.delete(
        path=reverse('dv-admin:faq-rud', args=[faq_id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    assert FAQ.objects.filter(id=faq_id).first() is None

# endregion
