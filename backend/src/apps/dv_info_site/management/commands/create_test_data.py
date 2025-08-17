import random
from decimal import Decimal

from django.core.files.base import File
from django.core.management.base import BaseCommand

from apps.dv_info_site.model_utils import DEFAULT_COUNTRIES, ContactDepartment, FormTemplateType, \
    FormQuestionType, CalcFieldType
from apps.dv_info_site.models import MainPageSlider, MainPageButtonBlock, MainPageReputationLink, Retail, \
    Contact, FAQ, \
    Vacancy, Partnership, Project, ProjectLink, DVInstruction, Country, City, FormTemplate, FormQuestion, \
    FormAnswerChoice, Calculator, CalcField, CalcFieldChoice
from core.service.translator import update_object_translate


class Command(BaseCommand):

    def handle(self, *args, **options):
        # self.create_main_slider()
        # self.create_main_block_button()
        # self.create_main_page_reputation_link()
        # self.create_retail()
        # self.create_contacts()
        # self.create_faq()
        self.create_vacancy()
        # self.create_partnerships()
        # self.create_projects()
        # self.create_dv_instructions()
        # self.create_countries()

    def create_main_slider(self):
        MainPageSlider.objects.all().delete()
        with open('apps/dv_info_site/test_files/dl.png', 'rb') as f:
            file = File(f)
            for i in range(3):
                a = MainPageSlider(
                    title=f'Информационный ресурс для поиска работы и приобретения товаров {i}',
                    description='Мы стремимся быть надежным и доступным ресурсом для всех, кто ищет работу или хочет приобрести наши товары оптом и в розницу. Наша цель - предоставить всю информацию и приобретении наших товаров.'
                )
                a.image.save('image.png', file)
                a.save()
                update_object_translate(a, ['title', 'description'])

    def create_main_block_button(self):
        MainPageButtonBlock.objects.all().delete()
        with open('apps/dv_info_site/test_files/1.svg', 'rb') as f:
            file = File(f)
            b1 = MainPageButtonBlock(
                title='Менеджер по продажам',
                description='Вакансия с высоким уровнем оплаты',
                link='https://google.com',
            )
            b1.background_image.save('file.svg', file)
            b2 = MainPageButtonBlock(
                title='Обменник валют',
                description='Минимальные комиссии на обмен',
                link='https://google.com',
            )
            b2.background_image.save('file.svg', file)
            b3 = MainPageButtonBlock(
                title='Менеджер по продажам',
                description='Вакансия с высоким уровнем оплаты',
                link='https://google.com',
            )
            b3.background_image.save('file.svg', file)
            b4 = MainPageButtonBlock(
                title='Скидки и акции',
                description='Лучшие предложения на всём рынке',
                link='https://google.com',
            )
            b4.background_image.save('file.svg', file)
            b1.save()
            b2.save()
            b3.save()
            b4.save()
        update_object_translate(b1, ['title', 'description'])
        update_object_translate(b2, ['title', 'description'])
        update_object_translate(b3, ['title', 'description'])
        update_object_translate(b4, ['title', 'description'])

    def create_main_page_reputation_link(self):
        MainPageReputationLink.objects.all().delete()
        for i in range(6):
            with open('apps/dv_info_site/test_files/dl.png', 'rb') as f:
                file = File(f)
                a = MainPageReputationLink(
                    title=f'Сайт продаж {i}',
                    link='https://google.com',
                )
                a.image.save('file.svg', file)

            update_object_translate(a, ['title', ])

    def create_retail(self):
        Retail.objects.all().delete()
        for i in range(10):
            Retail.objects.create(
                name=f'Название {1}',
                link='https://google.com',
                link_type=f'Type-{i}'
            )

    def create_contacts(self):
        Contact.objects.all().delete()
        with open('apps/dv_info_site/test_files/dl.png', 'rb') as f:
            file = File(f)
            c1 = Contact(
                department=ContactDepartment.EMPLOYMENT,
                person='Reno',
                telegram='@nickname',
                session='@nickname',
                element='@nickname',
            )
            c1.person_avatar.save('file.png', file)
            c2 = Contact(
                department=ContactDepartment.OPT,
                person='Reno',
                telegram='@nickname',
                session='@nickname',
                element='@nickname',
            )
            c2.person_avatar.save('file.svg', file)
            c1.save()
            c2.save()

    def create_faq(self):
        FAQ.objects.all().delete()
        for i in range(9):
            faq = FAQ.objects.create(
                question='2. Как я могу оформить заказ и какие способы оплаты вы принимаете?',
                answer='Заказ можно оформить через наш интернет-магазин, выбрав необходимые товары и добавив их в корзину. Мы принимаем оплату банковскими картами, электронными кошельками, банковским переводом и наличными при получении (для розничных покупателей). Подробные инструкции по оплате будут предоставлены на этапе оформления заказа',
                position=i,
            )
            update_object_translate(faq, ['question', 'answer'])

    def create_vacancy(self):
        Vacancy.objects.all().delete()
        with open('apps/dv_info_site/test_files/dl.png', 'rb') as f:
            file = File(f)
            for i in range(1, 5):
                v = Vacancy(
                    title=f'Вакансия {i}',
                    description='Вакансия с высоким уровнем оплаты',
                    short_description='Вакансия с высоким уровнем оплаты Вакансия с высоким уровнем оплаты Вакансия с высоким уровнем оплаты Вакансия с высоким уровнем оплаты Вакансия с высоким уровнем оплаты Вакансия с высоким уровнем оплаты Вакансия с высоким уровнем оплаты Вакансия с высоким уровнем оплаты Вакансия с высоким уровнем оплаты',
                    salary=Decimal(random.randint(10, 20) * 10000),
                    form_template=self.create_form_template(FormTemplateType.VACANCY),
                    calculator=self.create_calculator()
                )
                v.image.save('file.svg', file)
                v.save()
                update_object_translate(v, ['title', 'description', 'short_description'])

    def create_partnerships(self):
        Partnership.objects.all().delete()
        with open('apps/dv_info_site/test_files/dl.png', 'rb') as f:
            file = File(f)
            for i in range(5):
                partner = Partnership(
                    title='Франшиза',
                    form_template=self.create_form_template(FormTemplateType.PARTNERSHIP),
                    description='Ознакомся с условиями и начинай зарабатывать вместе с нами! Da Vinci - это инновационная сеть химических лабораторий, специализирующаяся на оптовой и розничной продаже высококачественной продукции. Наша франшиза предлагает уникальную возможность стать частью быстрорастущего бизнеса в сфере химической промышленности.',
                )
                partner.image.save('file.svg', file)
                partner.save()
                update_object_translate(partner, ['title', 'description'])

    def create_projects(self):
        Project.objects.all().delete()
        ton = Project.objects.create(
            title='Тон',
            description='Также ознакомьтесь с инструкцией по доступу к нашему TON-зеркалу'
        )
        update_object_translate(ton, ['title', 'description'])

        for i in range(1, 5):
            ProjectLink.objects.create(
                project=ton,
                link='https://google.com',
                is_active=True,
            )

        ethereum = Project.objects.create(
            title='Ethereum',
            description='криптовалюта и платформа для создания децентрализованных онлайн-сервисов на базе блокчейна, работающих на базе умных контрактов'
        )
        update_object_translate(ton, ['title', 'description'])

        for i in range(1, 5):
            ProjectLink.objects.create(
                project=ethereum,
                link='https://google.com',
                is_active=True,
            )

    def create_dv_instructions(self):
        DVInstruction.objects.all().delete()
        with open('apps/dv_info_site/test_files/1.svg', 'rb') as f:
            file = File(f)
            for i in range(3):
                dv = DVInstruction(
                    title=f'КАК ЗАРЕГИСТРИРОВАТЬСЯ В ELEMENT, ИСПОЛЬЗУЯ СЕРВЕР VZV.SE? {i}',
                    description='Element — это защищенное приложение для обмена сообщениями и совместной работы со сквозным шифрованием.',
                )
                dv.icon.save('file.svg', file)
                dv.save()
                update_object_translate(dv, ['title', 'description'])

    def create_countries(self):
        Country.objects.all().delete()
        for code, country_data in DEFAULT_COUNTRIES.items():
            country = Country.objects.create(
                code=code,
                name=country_data['name'],
            )
            update_object_translate(country, ['name', ])
            for city_name in country_data['cities']:
                city = City.objects.create(
                    name=city_name,
                    country=country,
                )
                update_object_translate(city, ['name', ])

    def create_form_template(self, template_type):
        form_template = FormTemplate.objects.create(
            form_type=template_type,
            is_active=True,
        )
        q1 = FormQuestion.objects.create(
            form_template=form_template,
            question='ФИО',
            question_type=FormQuestionType.TEXT,
            position=1
        )
        update_object_translate(q1, ['question', ])
        q2 = FormQuestion.objects.create(
            form_template=form_template,
            question='Выбор одного варианта',
            question_type=FormQuestionType.SINGLE_CHOICE,
            position=2
        )
        for i in ['A', 'B', 'C', 'D']:
            a = FormAnswerChoice.objects.create(
                form_question=q2,
                value=f'Вариант {i}',
            )
            update_object_translate(a, ['value', ])
        update_object_translate(q2, ['question', ])

        q3 = FormQuestion.objects.create(
            form_template=form_template,
            question='Выбор нескольких вариантов',
            question_type=FormQuestionType.MULTI_CHOICE,
            position=3
        )
        for i in ['A', 'B', 'C', 'D']:
            a = FormAnswerChoice.objects.create(
                form_question=q3,
                value=f'Вариант {i}',
            )
            update_object_translate(a, ['value', ])
        update_object_translate(q3, ['question', ])

        q4 = FormQuestion.objects.create(
            form_template=form_template,
            question='Загрузите файл',
            question_type=FormQuestionType.FILE,
            position=4
        )
        update_object_translate(q4, ['question', ])

        q5 = FormQuestion.objects.create(
            form_template=form_template,
            question='Загрузите файл или ссылку',
            question_type=FormQuestionType.FILE_OR_LINK,
            position=5
        )
        update_object_translate(q5, ['question', ])
        return form_template

    def create_calculator(self):
        calc = Calculator.objects.create()
        field = CalcField.objects.create(
            calculator=calc,
            field_type=CalcFieldType.INPUT_RANGE,
            label='Количество доставок за 1 день:',
            default_value=Decimal(1),
            max_value=Decimal(1),
            min_value=Decimal(100),
            name='delivery_per_day',
            is_required=True,
            step=Decimal(1),
        )
        field = CalcField.objects.create(
            calculator=calc,
            field_type=CalcFieldType.INPUT_RANGE,
            label='Сумма Вашего депозита:',
            default_value=Decimal(1),
            max_value=Decimal(1),
            min_value=Decimal(100),
            name='deposit',
            is_required=True,
            step=Decimal(1),
        )

        field = CalcField.objects.create(
            calculator=calc,
            field_type=CalcFieldType.SINGLE_CHOICE,
            label='Готов к переезду?',
            name='aaa',
            is_required=True,
            step=Decimal(1),
        )
        CalcFieldChoice.objects.create(
            field=field,
            value=Decimal(1),
            label='Москва',
        )
        CalcFieldChoice.objects.create(
            field=field,
            value=Decimal(1),
            label='Дальний восток',
        )
        CalcFieldChoice.objects.create(
            field=field,
            value=Decimal(1),
            label='Остальные города',
        )
        return calc
