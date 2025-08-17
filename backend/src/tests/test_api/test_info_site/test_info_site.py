import pytest
import requests
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.dv_info_site.models import MainPageSlider, MainPageButtonBlock, Product, MainPageReputationLink, Retail, \
    Contact, FAQ, Vacancy, Partnership, Project, DVInstruction, Country, BugReport, ResourcePolicy
from tests.plugins.utils import get_test_file, get_test_image


@pytest.mark.django_db()
def test_list_slider(
        api_client: APIClient,
        create_slider_factory,
):
    slider = create_slider_factory()
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-info:main-slider-list'),
            headers={
                'Accept-Language': lang,
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert MainPageSlider.objects.count() == len(response.data)
        assert response.data[0]['title'] == getattr(slider, f'title_{lang}')
        assert response.data[0]['description'] == getattr(slider, f'description_{lang}')


@pytest.mark.django_db()
def test_list_button_block(
        api_client: APIClient,
        create_button_block_factory
):
    button = create_button_block_factory()
    assert MainPageButtonBlock.objects.count() == 1
    response = api_client.get(
        path=reverse('dv-info:main-button-block-list'),
    )
    assert MainPageButtonBlock.objects.all().count() == len(response.data)
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-info:main-button-block-list'),
            headers={
                'Accept-Language': lang,
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert response.data[0]['title'] == getattr(button, f'title_{lang}')
        assert response.data[0]['description'] == getattr(button, f'description_{lang}')


@pytest.mark.django_db()
def test_list_reputation_links(
        api_client: APIClient,
        create_reputation_link_factory
):
    link = create_reputation_link_factory()
    response = api_client.get(
        path=reverse('dv-info:main-reputation-links-list'),
    )
    assert MainPageReputationLink.objects.all().count() == len(response.data)
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-info:main-reputation-links-list'),
            headers={
                'Accept-Language': lang
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert response.data[0]['title'] == getattr(link, f'title_{lang}')


@pytest.mark.django_db()
def test_list_retail(
        api_client: APIClient,
        create_retail_factory
):
    create_retail_factory()
    response = api_client.get(
        path=reverse('dv-info:retail-list')
    )
    assert response.status_code == status.HTTP_200_OK
    assert Retail.objects.all().count() == len(response.data)


@pytest.mark.django_db()
def test_list_contact(
        api_client: APIClient,
        create_contact_factory
):
    contact = create_contact_factory()
    response = api_client.get(
        path=reverse('dv-info:contacts-list')
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert Contact.objects.all().count() == len(response.data)


@pytest.mark.django_db()
def test_list_faq(
        api_client: APIClient,
        create_faq_factory
):
    faq = create_faq_factory()
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-info:faq-list'),
            headers={
                'Accept-Language': lang,
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert FAQ.objects.count() == len(response.data)
        assert response.data[0]['answer'] == getattr(faq, f'answer_{lang}')
        assert response.data[0]['question'] == getattr(faq, f'question_{lang}')


@pytest.mark.django_db()
def test_list_vacancies(
        api_client: APIClient,
        create_vacancy_factory
):
    vacancy = create_vacancy_factory()
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-info:vacancies-list'),
            headers={
                'Accept-Language': lang,
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert Vacancy.objects.count() == len(response.data)
        assert response.data[0]['title'] == getattr(vacancy, f'title_{lang}')
        assert response.data[0]['description'] == getattr(vacancy, f'description_{lang}')
        assert response.data[0]['short_description'] == getattr(vacancy, f'short_description_{lang}')


@pytest.mark.django_db()
def test_list_partnerships(
        api_client: APIClient,
        create_partnership_factory
):
    partnership = create_partnership_factory()
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-info:partnerships-list'),
            headers={
                'Accept-Language': lang
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert Partnership.objects.count() == len(response.data)
        assert response.data[0]['title'] == getattr(partnership, f'title_{lang}')
        assert response.data[0]['description'] == getattr(partnership, f'description_{lang}')


@pytest.mark.django_db()
def test_list_projects(
        api_client: APIClient,
        create_project_factory
):
    project = create_project_factory()
    response = api_client.get(
        path=reverse('dv-info:projects-list')
    )
    assert response.status_code == status.HTTP_200_OK
    assert Project.objects.all().count() == len(response.data)
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-info:projects-list'),
            headers={
                'Accept-Language': lang
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert response.data[0]['title'] == getattr(project, f'title_{lang}')
        assert response.data[0]['description'] == getattr(project, f'description_{lang}')


@pytest.mark.django_db()
def test_list_dv_instructions(
        api_client: APIClient,
        create_dv_instruction_factory
):
    dv_instruction = create_dv_instruction_factory()
    response = api_client.get(
        path=reverse('dv-info:dv-instructions-list')
    )
    assert response.status_code == status.HTTP_200_OK
    assert DVInstruction.objects.all().count() == len(response.data)
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-info:dv-instructions-list'),
            headers={
                'Accept-Language': lang
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert response.data[0]['title'] == getattr(dv_instruction, f'title_{lang}')
        assert response.data[0]['description'] == getattr(dv_instruction, f'description_{lang}')


@pytest.mark.django_db()
def test_list_opt_country(
        api_client: APIClient
):
    response = api_client.get(
        path=reverse('dv-info:opt-country-list')
    )
    assert response.status_code == status.HTTP_200_OK
    assert Country.objects.filter(is_active=True).count() == len(response.data)


@pytest.mark.django_db()
def test_list_opt_product_export(
        api_client: APIClient
):
    response = api_client.get(
        path=reverse('dv-info:opt-product-export-list')
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db()
def test_list_opt_product(
        api_client: APIClient
):
    response = api_client.get(
        path=reverse('dv-info:opt-product-list')
    )
    assert response.status_code == status.HTTP_200_OK
    assert Product.objects.all().count() == response.data['count']


@pytest.mark.django_db()
def test_form_template(
        api_client: APIClient,
        create_form_template_fixture,
        create_form_template_question_factory
):
    form_template = create_form_template_fixture()
    create_form_template_question_factory(form_template=form_template)
    response = api_client.get(
        path=reverse('dv-info:form-template', args=[form_template.pk])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None
    assert len(response.data['questions']) == 1


@pytest.mark.django_db()
def test_form_template_complete(
        api_client: APIClient,
        create_form_template_fixture,
        create_form_template_question_factory
):
    form_template = create_form_template_fixture()
    question = create_form_template_question_factory(form_template=form_template)
    answers = [
        {
            'question': question.pk,
            'text': 'Test',
            'file': None,
            'choices': None
        }
    ]
    response = api_client.post(
        path=reverse('dv-info:form-template-complete'),
        data={
            'form_template': form_template.pk,
            'answers': answers
        },
        format='json'
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data is not None


@pytest.mark.django_db()
def test_upload_file(
        api_client: APIClient,
):
    response = api_client.post(
        path=reverse('dv-info:file-upload'),
        data={
            'file': get_test_image()
        },
        format='multipart'
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data is not None
    assert 'id' in response.data


@pytest.mark.django_db()
def test_calculator(
        api_client: APIClient,
        create_vacancy_calculator_fixture,
):
    calc = create_vacancy_calculator_fixture()
    response = api_client.get(
        path=reverse('dv-info:calculator-retrieve', args=[calc.pk])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None


@pytest.mark.django_db()
def test_bugs_settings(
        api_client: APIClient,
        create_bug_settings_fixture,
):
    bug_settings = create_bug_settings_fixture()
    response = api_client.get(
        path=reverse('dv-info:bug-settings')
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None


@pytest.mark.django_db()
def test_bug_report_create(
        api_client: APIClient,
):
    response = api_client.post(
        path=reverse('dv-info:bug-report-create'),
        data={
            'title': 'Test',
            'description': 'Test',
            'file': get_test_image()
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data is not None
    assert BugReport.objects.count() == 1


@pytest.mark.django_db()
def test_list_resource_policy(
        api_client: APIClient,
        create_resource_policy_factory
):
    policy = create_resource_policy_factory()
    for lang, _ in settings.LANGUAGES:
        response = api_client.get(
            path=reverse('dv-info:resource-policy'),
            headers={
                'Accept-Language': lang,
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is not None
        assert ResourcePolicy.objects.count() == len(response.data)
        assert response.data[0]['title'] == getattr(policy, f'title_{lang}')
        assert response.data[0]['description'] == getattr(policy, f'description_{lang}')
        print(f"Title in {lang}: {response.data[0]['title']}")
        print(f"Description in {lang}: {response.data[0]['description']}")
