from datetime import date

from django.db.models import TextChoices


class ContactType(TextChoices):
    MESSENGER = 'messenger', 'Мессенджер'
    SITE = 'site', 'Сайт'


class ProductUpdateFileStatus(TextChoices):
    WAITING = 'waiting', 'В ожидании'
    PROCESSING = 'processing', 'В обработке'
    PROCESSED = 'processed', 'Обработано'
    ERROR = 'error', 'Ошибка'


class ContactDepartment(TextChoices):
    OPT = 'opt', 'Отдел продаж'
    EMPLOYMENT = 'employment', 'Отдел трудоустройства'


class FormTemplateType(TextChoices):
    VACANCY = 'vacancy', 'Вакансия'
    PARTNERSHIP = 'partnership', 'Партнерство'


class CalcFieldType(TextChoices):
    INPUT = 'input', 'Ввод значения'
    SINGLE_CHOICE = 'single_choice', 'Выбор одного из вариантов'
    MULTI_CHOICE = 'multi_choice', 'Выбор нескольких вариантов'
    INPUT_RANGE = 'input_range', 'Ползунок'


class FormQuestionType(TextChoices):
    TEXT = 'text', 'Текст'
    FILE = 'file', 'Файл'
    FILE_OR_LINK = 'file_or_link', 'Файл или ссылка на файл'
    SINGLE_CHOICE = 'single_choice', 'Выбор из вариантов'
    MULTI_CHOICE = 'multi_choice', 'Выбор из вариантов'


class ProductUpdateFileType(TextChoices):
    XLSX = 'xlsx', 'XLSX'
    JSON = 'json', 'JSON'


class VacancyWorkFormat(TextChoices):
    ONLINE = 'online', 'Онлайн'
    OFFLINE = 'offline', 'Оффлайн'
    NO_EXPERIENCE = 'no_experience', 'Без опыта'


DEFAULT_COUNTRIES = {
    'RU': {
        'name': 'Россия',
        'cities': [
            'Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург',
            'Нижний Новгород', 'Казань', 'Челябинск', 'Самара',
            'Омск', 'Ростов-на-Дону', 'Уфа', 'Красноярск',
            'Пермь', 'Воронеж', 'Волгоград'
        ]
    },
    'UZ': {
        'name': 'Узбекистан',
        'cities': [
            'Ташкент', 'Самарканд', 'Бухара', 'Хива',
            'Коканд', 'Андижан', 'Наманган', 'Фергана',
            'Карши', 'Нукус', 'Навои', 'Термез',
            'Джизак', 'Гулистан', 'Зарафшан'
        ]
    },
    'BY': {
        'name': 'Беларусь',
        'cities': [
            'Минск', 'Гомель', 'Могилёв', 'Витебск',
            'Гродно', 'Брест', 'Барановичи', 'Борисов',
            'Пинск', 'Орша', 'Солигорск', 'Лида',
            'Новополоцк', 'Мозырь', 'Светлогорск'
        ]
    },
    'KZ': {
        'name': 'Казахстан',
        'cities': [
            'Алматы', 'Нур-Султан', 'Шымкент', 'Караганда',
            'Актобе', 'Тараз', 'Павлодар', 'Усть-Каменогорск',
            'Семей', 'Атырау', 'Костанай', 'Петропавловск',
            'Кызылорда', 'Темиртау', 'Туркестан'
        ]
    },
    'KG': {
        'name': 'Киргизия',
        'cities': [
            'Бишкек', 'Ош', 'Джалал-Абад', 'Каракол',
            'Талас', 'Нарын', 'Токмок', 'Кызыл-Кия',
            'Баткен', 'Кара-Балта', 'Кант', 'Балыкчы',
            'Кочкор-Ата', 'Исфана', 'Сулюкта'
        ]
    },
    'TJ': {
        'name': 'Таджикистан',
        'cities': [
            'Душанбе', 'Худжанд', 'Куляб', 'Бохтар',
            'Истаравшан', 'Курган-Тюбе', 'Турсунзаде', 'Пенджикент',
            'Исфара', 'Вахдат', 'Гиссар', 'Дангара',
            'Рогун', 'Айни', 'Яван'
        ]
    },
    'AM': {
        'name': 'Армения',
        'cities': [
            'Ереван', 'Гюмри', 'Ванадзор', 'Гавар',
            'Раздан', 'Эчмиадзин', 'Армавир', 'Арташат',
            'Капан', 'Алаверди', 'Иджеван', 'Севан',
            'Аштарак', 'Мартуни', 'Масис'
        ]
    }
}


def get_product_update_file_path(instance, filename) -> str:
    today = date.today()
    return f'product-update-files/{today.year}/{today.month}/{today.day}/{filename}'


def get_form_template_answer_file_path(instance, filename) -> str:
    return f'form-template/question-{instance.question_id}/{filename}'
