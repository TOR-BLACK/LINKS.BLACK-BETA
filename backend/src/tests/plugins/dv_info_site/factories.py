from decimal import Decimal

import pytest
from mixer.backend.django import mixer

from apps.dv_info_site.model_utils import ContactType, FormTemplateType, FormQuestionType, CalcFieldType
from apps.dv_info_site.models import (
    MainPageSlider,
    MainPageButtonBlock,
    MainPageReputationLink,
    ContactDepartment,
    Vacancy, Retail, FAQ, Partnership, Project, ProjectLink, DVInstruction, Country, City, Contact, FormTemplate,
    FormQuestion, FormAnswerChoice, Calculator, CalcField, BugReportSetting, ResourcePolicy
)
from tests.plugins.utils import generate_translate_field_value, get_test_file, get_test_image


@pytest.fixture()
def create_slider_factory():
    def factory(*args, **kwargs) -> MainPageSlider:
        title = kwargs.get("title", 'title')
        description = kwargs.get("description", 'description')
        image = kwargs.get("image", get_test_image())
        data = {
            'title': title,
            'description': description,
            'image': image,
        }
        data |= generate_translate_field_value('title', title)
        data |= generate_translate_field_value('description', description)

        slider = mixer.blend(
            MainPageSlider,
            **data
        )
        return slider

    return factory


@pytest.fixture()
def create_button_block_factory():
    def factory(*args, **kwargs) -> MainPageButtonBlock:
        title = kwargs.get("title", 'title')
        description = kwargs.get("description", 'description')
        data = {
            'title': title,
            'description': description,
            'background_image': kwargs.get("background_image", get_test_file()),
            'link': kwargs.get("link", 'https://link.com')
        }
        data = data | generate_translate_field_value('title', title) | generate_translate_field_value('description',
                                                                                                      description)
        button = mixer.blend(
            MainPageButtonBlock,
            **data

        )
        return button

    return factory


@pytest.fixture()
def create_reputation_link_factory():
    def factory(*args, **kwargs) -> MainPageReputationLink:
        title = kwargs.get("title", 'Title')
        data = {
            'title': title,
            'image': kwargs.get("image", get_test_image()),
            'link': kwargs.get("link", 'https://link.com')
        }
        data |= generate_translate_field_value('title', title)
        button = mixer.blend(
            MainPageReputationLink,
            **data

        )
        return button

    return factory


@pytest.fixture()
def create_contact_factory():
    def factory(*args, **kwargs) -> Contact:
        data = {
            'person': kwargs.get("person", 'Reno'),
            'person_avatar': kwargs.get("person", get_test_image()),
            'department': kwargs.get("department", ContactDepartment.EMPLOYMENT),
            'telegram': kwargs.get("telegram", '@tgnick'),
            'element': kwargs.get("telegram", '@element'),
            'session': kwargs.get("telegram", '@session'),

        }

        contact = mixer.blend(
            Contact,
            **data
        )
        return contact

    return factory


@pytest.fixture()
def create_vacancy_factory():
    def factory(*args, **kwargs) -> Vacancy:
        title = kwargs.get("title", 'Title')
        short_description = kwargs.get("short_description", 'short description')
        description = kwargs.get("description", 'description')
        data = {
            'title': title,
            'short_description': short_description,
            'description': description,
            'image': kwargs.get("image", get_test_image()),
            'salary': kwargs.get("salary", Decimal(1000000)),
            'salary_calc': kwargs.get("salary_calc", True),
            'is_active': kwargs.get("salary_calc", True)
        }
        data |= generate_translate_field_value('title', title)
        data |= generate_translate_field_value('description', description)
        data |= generate_translate_field_value('short_description', short_description)
        button = mixer.blend(
            Vacancy,
            **data

        )
        return button

    return factory


@pytest.fixture()
def create_retail_factory():
    def factory(*args, **kwargs) -> Retail:
        data = {
            'name': kwargs.get("name", 'name'),
            'link_type': kwargs.get("contact_type", 'link_type'),
            'link': kwargs.get("link", 'https://link.com')
        }

        retail = mixer.blend(
            Retail,
            **data
        )
        return retail

    return factory


@pytest.fixture()
def create_faq_factory():
    def factory(*args, **kwargs) -> FAQ:
        question = kwargs.get("question", 'Тестовый вопрос')
        answer = kwargs.get("answer", 'Тестовый ответ')

        data = {
            'question': question,
            'answer': answer,
            'image': kwargs.get("image", get_test_image()),
            'position': kwargs.get("position", 1)
        }
        data |= generate_translate_field_value('question', question)
        data |= generate_translate_field_value('answer', answer)

        faq = mixer.blend(
            FAQ,
            **data
        )
        return faq

    return factory


@pytest.fixture()
def create_partnership_factory():
    def factory(*args, **kwargs) -> Partnership:
        title = kwargs.get("title", 'Title')
        description = kwargs.get("description", 'description')
        data = {
            'title': title,
            'description': description,
            'image': kwargs.get("image", get_test_image()),
        }
        data |= generate_translate_field_value('title', title)
        data |= generate_translate_field_value('description', description)
        button = mixer.blend(
            Partnership,
            **data

        )
        return button

    return factory


@pytest.fixture()
def create_project_factory():
    def factory(*args, **kwargs) -> Project:
        title = kwargs.get("title", 'Title')
        description = kwargs.get("description", 'description')
        data = {
            'title': title,
            'description': description,
        }
        data |= generate_translate_field_value('title', title)
        data |= generate_translate_field_value('description', description)
        button = mixer.blend(
            Project,
            **data

        )
        return button

    return factory


@pytest.fixture()
def create_project_link_factory(create_project_factory):
    def factory(*args, **kwargs) -> ProjectLink:
        data = {
            'project': kwargs.get("project_id", create_project_factory()),
            'link': kwargs.get("link", 'https://link.com'),
            'is_active': kwargs.get("is_active", True)

        }
        button = mixer.blend(
            ProjectLink,
            **data

        )
        return button

    return factory


@pytest.fixture()
def create_dv_instruction_factory():
    def factory(*args, **kwargs) -> DVInstruction:
        title = kwargs.get("title", 'Title')
        description = kwargs.get("description", 'description')
        data = {
            'title': title,
            'description': description,
            'icon': kwargs.get("icon", get_test_image()),
        }
        data |= generate_translate_field_value('title', title)
        data |= generate_translate_field_value('description', description)
        button = mixer.blend(
            DVInstruction,
            **data

        )
        return button

    return factory


@pytest.fixture()
def create_country_fixture():
    def factory(*args, **kwargs) -> Country:
        name = kwargs.get("name", 'Россия')
        data = {
            'name': name,
            'code': kwargs.get("code", 'ru'),
            'is_active': kwargs.get("is_active", False),
        }
        data |= generate_translate_field_value('name', name)
        country = mixer.blend(
            Country,
            **data
        )
        return country

    return factory


@pytest.fixture()
def create_city_fixture(
        create_country_fixture
):
    def factory(*args, **kwargs) -> Country:
        name = kwargs.get("name", 'Москва')
        data = {
            'name': name,
            'country': kwargs.get("country", create_country_fixture()),
            'is_active': kwargs.get("is_active", False),
        }
        data |= generate_translate_field_value('name', name)
        city = mixer.blend(
            City,
            **data
        )
        return city

    return factory


@pytest.fixture()
def create_form_template_fixture():
    def factory(*args, **kwargs) -> FormTemplate:
        template_type = kwargs.get('template_type', FormTemplateType.VACANCY)
        is_active = kwargs.get('is_active', True)
        form_template = FormTemplate.objects.create(
            form_type=template_type,
            is_active=is_active,
        )
        return form_template

    return factory


@pytest.fixture()
def create_form_template_question_factory(
        create_form_template_fixture
):
    def factory(*args, **kwargs) -> FormQuestion:
        form_template = kwargs.get("form_template", create_form_template_fixture())
        question = kwargs.get("question", 'Вопрос')
        question_type = kwargs.get("question_type", FormQuestionType.TEXT)
        position = kwargs.get("position", 1)
        data = {
            'question': question,
            'form_template': form_template,
            'question_type': question_type,
            'position': position,
        }
        data |= generate_translate_field_value('question', question)
        question = mixer.blend(
            FormQuestion,
            **data
        )
        if 'choices' in kwargs:
            for value in kwargs['choices']:
                d = {
                    'value': value,
                    'form_question': question,
                }
                d |= generate_translate_field_value('value', value)
                FormAnswerChoice.objects.create(**d)
        return question

    return factory


@pytest.fixture()
def create_vacancy_calculator_fixture():
    def factory(*args, **kwargs) -> Calculator:
        formula = kwargs.get('formula', '')
        calculator = mixer.blend(Calculator, formula=formula)
        data = {
            'calculator': calculator,
            'field_type': CalcFieldType.INPUT,
            'label': 'Test',
            'name': 'name'
        }
        data |= generate_translate_field_value('label', 'test_label')
        field = mixer.blend(
            CalcField,
            **data

        )
        return calculator

    return factory


@pytest.fixture()
def create_bug_settings_fixture():
    def factory(*args, **kwargs) -> Calculator:
        title = kwargs.get('title', '')
        data = {}
        data |= generate_translate_field_value('title', title)
        bugs_settings = mixer.blend(BugReportSetting, **data)
        return bugs_settings

    return factory

@pytest.fixture()
def create_resource_policy_factory():
    def factory(*args, **kwargs) -> ResourcePolicy:
        title = kwargs.get("title", 'Правила и политика ресурса')
        description = kwargs.get("description", 'Описание политики')
        data = {
            'title': title,
            'description': description,
        }
        data |= generate_translate_field_value('title', title)
        data |= generate_translate_field_value('description', description)
        
        policy = mixer.blend(
            ResourcePolicy,
            **data
        )
        return policy

    return factory