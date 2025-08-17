import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.dv_info_site.models import Project, ProjectLink


@pytest.mark.django_db()
def test_project_create(
        api_client: APIClient,
        get_user_jwt,
        create_project_factory,
):
    response = api_client.post(
        path=reverse('dv-admin:project-lc'),
        data={
            'title': 'Тестовое название',
            'description': 'Тестовое описание'
        },
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    project = Project.objects.first()
    assert project is not None
    for lang, _ in settings.LANGUAGES:
        assert getattr(project, f'title_{lang}') is not None
        assert getattr(project, f'description_{lang}') is not None


@pytest.mark.django_db()
def test_project_list(
        api_client: APIClient,
        get_user_jwt,
        create_project_factory,
):
    project = create_project_factory()
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:project-lc'),
            headers={
                'Accept-Language': lang,
                'Authorization': get_user_jwt()
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert Project.objects.count() == response.data['count']
        assert response.data['results'][0]['title'] == getattr(project, f'title_{lang}')
        assert response.data['results'][0]['description'] == getattr(project, f'description_{lang}')


@pytest.mark.django_db()
def test_project_detail(
        api_client: APIClient,
        get_user_jwt,
        create_project_factory,
):
    project = create_project_factory()
    response = api_client.get(
        path=reverse('dv-admin:project-rud', args=[project.id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert project.id == response.data['id']


@pytest.mark.django_db()
def test_project_update(
        api_client: APIClient,
        get_user_jwt,
        create_project_factory,
):
    project = create_project_factory()
    update_title = 'Обновленное название'
    update_description = 'Обновленное описание'

    response = api_client.patch(
        path=reverse('dv-admin:project-rud', args=[project.id]),
        headers={
            'Authorization': get_user_jwt()
        },
        data={
            'title': update_title,
            'description': update_description
        }
    )
    project.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert project.title == update_title
    assert project.description == update_description

    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-admin:project-rud', args=[project.id]),
            headers={
                'Authorization': get_user_jwt(),
                'Accept-Language': lang
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert project.id == response.data['id']
        assert response.data['title'] == getattr(project, f'title_{lang}')
        assert response.data['description'] == getattr(project, f'description_{lang}')


@pytest.mark.django_db()
def test_project_delete(
        api_client: APIClient,
        get_user_jwt,
        create_project_factory,
):
    project = create_project_factory()
    project_id = project.id
    response = api_client.delete(
        path=reverse('dv-admin:project-rud', args=[project_id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    assert Project.objects.filter(id=project_id).first() is None


@pytest.mark.django_db()
def test_create_project_link(
        api_client: APIClient,
        get_user_jwt,
        create_project_factory,
):
    project = create_project_factory()
    response = api_client.post(
        path=reverse('dv-admin:project-link-create'),
        data={
            'project': project.id,
            'link': 'https://test.com',
            'is_active': True
        },
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    project_link = ProjectLink.objects.first()
    assert project_link is not None
    assert project_link.id == response.data['id']


@pytest.mark.django_db()
def test_project_link_list(
        api_client: APIClient,
        get_user_jwt,
        create_project_link_factory,
):
    link = create_project_link_factory()
    response = api_client.get(
        path=reverse('dv-admin:project-links-list', args=[link.project_id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert ProjectLink.objects.count() == response.data['count']


@pytest.mark.django_db()
def test_project_link_detail(
        api_client: APIClient,
        get_user_jwt,
        create_project_link_factory,
):
    link = create_project_link_factory()
    response = api_client.get(
        path=reverse('dv-admin:project-link-rud', args=[link.id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert link.id == response.data['id']


@pytest.mark.django_db()
def test_project_link_update(
        api_client: APIClient,
        get_user_jwt,
        create_project_link_factory,
):
    link = create_project_link_factory()
    update_link = 'https://test2.com'
    update_is_active = False

    response = api_client.patch(
        path=reverse('dv-admin:project-link-rud', args=[link.id]),
        headers={
            'Authorization': get_user_jwt()
        },
        data={
            'link': update_link,
            'is_active': update_is_active,
        }
    )
    link.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert link.link == update_link
    assert link.is_active == update_is_active


@pytest.mark.django_db()
def test_project_link_delete(
        api_client: APIClient,
        get_user_jwt,
        create_project_link_factory,
):
    link = create_project_link_factory()
    link_id = link.id
    response = api_client.delete(
        path=reverse('dv-admin:project-link-rud', args=[link_id]),
        headers={
            'Authorization': get_user_jwt()
        }
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    assert ProjectLink.objects.filter(id=link_id).first() is None
