import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db()
def test_translate_service(
        api_client: APIClient,
        get_user_jwt
):
    response = api_client.post(
        path=reverse('dv-admin:translate-service'),
        headers={
            'Authorization': get_user_jwt()
        },
        data={
            'text': 'Тестовый текс который который нужно перевести'
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
