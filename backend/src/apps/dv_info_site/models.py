from django.db import models

from apps.dv_info_site.model_utils import ProductUpdateFileStatus, get_product_update_file_path, \
    ContactDepartment, FormTemplateType, CalcFieldType, FormQuestionType, ProductUpdateFileType, VacancyWorkFormat
from core.generics.models import ModelWithDate, SingletonModel

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class MainPageSlider(ModelWithDate):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='dvi-slider-images/', null=True, blank=True)

    class Meta:
        db_table = 'dvi_main_page_sliders'
        verbose_name = 'Слайдер главной страницы'
        verbose_name_plural = 'Слайдер главной страницы'

    def __str__(self):
        return f'{self.title}'


class MainPageButtonBlock(ModelWithDate):
    title = models.CharField(max_length=255)
    description = models.TextField()
    background_image = models.FileField(upload_to='dvi/main-page-button/')
    link = models.URLField(max_length=255)

    class Meta:
        db_table = 'dvi_main_page_button_blocks'
        verbose_name = 'Блок кнопок главной страницы'
        verbose_name_plural = 'Блок кнопок главной страницы'

    def __str__(self):
        return f'{self.title}'


class MainPageReputationLink(ModelWithDate):
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='dvi/main-page-reputation/')
    link = models.URLField(max_length=255)

    class Meta:
        db_table = 'dvi_main_page_reputations'
        verbose_name = 'Репутационный ссылки'
        verbose_name_plural = 'Репутационные ссылки'

    def __str__(self):
        return f'{self.title}'


class Retail(ModelWithDate):
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    link_type = models.CharField(max_length=255)

    class Meta:
        db_table = 'dvi_retail'
        verbose_name = 'Розница'
        verbose_name_plural = 'Розница'

    def __str__(self):
        return f'{self.name}'


class Contact(ModelWithDate):
    department = models.CharField(max_length=255, choices=ContactDepartment)
    person = models.CharField(max_length=255)
    person_avatar = models.ImageField(upload_to='dvi/department-contact/')

    telegram = models.CharField(max_length=255)
    is_telegram_active = models.BooleanField(default=True)
    element = models.CharField(max_length=255)
    session = models.CharField(max_length=255)

    class Meta:
        db_table = 'dvi_contacts'
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f'{self.department}-{self.person}'


class FAQ(ModelWithDate):
    question = models.TextField()
    answer = models.TextField()
    image = models.FileField(upload_to='dvi/faq-images/', null=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'dvi_faq'
        ordering = ('position',)


class Vacancy(ModelWithDate):
    form_template = models.ForeignKey('FormTemplate', on_delete=models.CASCADE, null=True, related_name='vacancies')
    calculator = models.ForeignKey('Calculator', on_delete=models.CASCADE, null=True, related_name='vacancies')
    image = models.ImageField(upload_to='dvi/vacancies/')
    work_format = models.CharField(max_length=50, choices=VacancyWorkFormat.choices, default=VacancyWorkFormat.ONLINE)
    title = models.CharField(max_length=255)
    salary = models.DecimalField(default=0, decimal_places=0, max_digits=10)
    short_description = models.TextField()
    description = models.TextField()
    salary_calc = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'dvi_vacancies'
        verbose_name = 'Вакансии'
        verbose_name_plural = 'Вакансии'


class Partnership(ModelWithDate):
    form_template = models.ForeignKey(
        'FormTemplate', on_delete=models.CASCADE, null=True, related_name='partnerships'
    )
    title = models.CharField(max_length=255)
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='dvi/partnership/')

    class Meta:
        db_table = 'dvi_partnerships'
        verbose_name = 'Партнерство'


class Project(ModelWithDate):
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = 'dvi_projects'
        verbose_name = 'Проекты'
        verbose_name_plural = 'Проекты'


class ProjectLink(ModelWithDate):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='links')
    link = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'dvi_project_links'
        verbose_name = 'Ссылки проекта'
        verbose_name_plural = 'Ссылки проекта'

class DVInstruction(ModelWithDate):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)

    class Meta:
        db_table = 'dvi_dv_instructions'
        verbose_name = 'Инструкция от localhost'
        verbose_name_plural = 'Инструкция от localhost'

    def __str__(self):
        return self.title

class DVInstructionRow(models.Model):
    instruction = models.ForeignKey(DVInstruction, related_name='rows', on_delete=models.CASCADE)
    column1_text = models.TextField(blank=True, null=True)
    column1_image = models.FileField(upload_to='dvi/dv-icons/', blank=True, null=True)
    column2_text = models.TextField(blank=True, null=True)
    column2_image = models.FileField(upload_to='dvi/dv-icons/', blank=True, null=True)
    column3_text = models.TextField(blank=True, null=True)
    column3_image = models.FileField(upload_to='dvi/dv-icons/', blank=True, null=True)

    class Meta:
        db_table = 'dvi_dv_instruction_rows'
        verbose_name = 'Строка инструкции'
        verbose_name_plural = 'Строки инструкции'

    def __str__(self):
        return f'{self.id}'

class Country(ModelWithDate):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'dvi_countries'
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return f'{self.name}'

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.name:
            raise ValidationError({'name': 'Русское название страны обязательно'})
        # Проверяем, что название на русском языке
        if any(ord(char) < 128 for char in self.name):
            raise ValidationError({'name': 'Название должно быть на русском языке'})


class City(ModelWithDate):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'dvi_cities'
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return f'{self.name}'


class Product(ModelWithDate):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    buy_url = models.TextField(max_length=200, verbose_name="Ссылка для покупки", blank=True, null=True)

    class Meta:
        db_table = 'dvi_products'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title


class ProductImage(ModelWithDate):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='dvi/product-image/')

    class Meta:
        db_table = 'dvi_product_images'

    def save(self, *args, **kwargs):
        if self.image:
            self.image = self.resize_image(self.image)
        super().save(*args, **kwargs)

    def resize_image(self, image, max_width=300, max_height=500):
            img = Image.open(image)
            img.thumbnail((max_width, max_height), Image.LANCZOS)
            img_io = BytesIO()
            if img.format == 'PNG':
                img.save(img_io, format='PNG')
            elif img.format == 'GIF':
                img.save(img_io, format='GIF')
            else:
                img.save(img_io, format='JPEG', quality=85)         
            return ContentFile(img_io.getvalue(), name=image.name)

class ProductItem(ModelWithDate):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='product_items')
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    count = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    
    AVAILABILITY_CHOICES = [
        ('preorder', 'Предзаказ'),
        ('in_stock', 'В наличии')
    ]
    availability_status = models.CharField(
        max_length=20, 
        choices=AVAILABILITY_CHOICES, 
        default='preorder',
        verbose_name='Статус наличия'
    )

    class Meta:
        db_table = 'dvi_product_items'
        verbose_name = 'Вариация продукта'
        verbose_name_plural = 'Вариации продуктов'

    def __str__(self):
        return self.title


class ProductUpdateFile(ModelWithDate):
    file = models.FileField(upload_to=get_product_update_file_path)
    file_type = models.CharField(max_length=50, choices=ProductUpdateFileType.choices,
                                 default=ProductUpdateFileType.XLSX)
    update_date = models.DateField()
    status = models.CharField(max_length=255, choices=ProductUpdateFileStatus.choices,
                              default=ProductUpdateFileStatus.WAITING)

    class Meta:
        db_table = 'dvi_product_update_files'
        verbose_name = 'Файл для обновления продуктов'
        verbose_name_plural = 'Файлы для обновления продуктов'

    def __str__(self):
        return f'Обновление-продуктов-{self.update_date}'


class DVIContentFile(ModelWithDate):
    file = models.ImageField(upload_to='dvi/content-images/')

    class Meta:
        db_table = 'dvi_content_images'
        verbose_name = 'Файл DVI контента'
        verbose_name_plural = 'Файлы DVI контента'


class FormTemplate(ModelWithDate):
    form_type = models.CharField(max_length=255, choices=FormTemplateType.choices)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'form_templates'
        verbose_name = 'Шаблон анкеты'
        verbose_name_plural = 'Шаблон анкеты'

    def __str__(self):
        return f'Шаблон анкеты: {self.form_type}-{self.id}'


class FormQuestion(ModelWithDate):
    form_template = models.ForeignKey(FormTemplate, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    question_type = models.CharField(max_length=255, choices=FormQuestionType.choices)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'form_questions'
        ordering = ('position',)
        unique_together = (('form_template', 'position'),)
        verbose_name = 'Вопрос анкеты'
        verbose_name_plural = 'Вопросы анкет'

    def __str__(self):
        return self.question


class FormAnswerChoice(ModelWithDate):
    value = models.TextField()
    form_question = models.ForeignKey(FormQuestion, on_delete=models.CASCADE, related_name='choices')

    class Meta:
        db_table = 'form_template_answer_choices'
        unique_together = (('form_question', 'value'),)
        ordering = ('created_at',)

    def __str__(self):
        return self.value


class FormUser(ModelWithDate):
    form_template = models.ForeignKey(FormTemplate, on_delete=models.CASCADE, related_name='users')

    class Meta:
        db_table = 'form_users'
        verbose_name = 'Отклик пользователей'
        verbose_name_plural = 'Отклик пользователей'


class FormAnswer(ModelWithDate):
    user = models.ForeignKey(FormUser, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(FormQuestion, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField(null=True)
    file = models.ForeignKey(DVIContentFile, on_delete=models.CASCADE, related_name='form_answers', null=True)
    choices = models.ManyToManyField(FormAnswerChoice, blank=True)

    class Meta:
        db_table = 'form_answers'
        verbose_name = 'Ответы'
        verbose_name_plural = 'Ответы'


class Calculator(ModelWithDate):
    formula = models.TextField(null=True)

    class Meta:
        db_table = 'calculators'
        verbose_name = 'Калькулятор вакансии'
        verbose_name_plural = 'Калькулятор вакансии'

    def __str__(self):
        return f'Калькулятор-{self.id}'


class CalcField(ModelWithDate):
    calculator = models.ForeignKey(Calculator, on_delete=models.CASCADE, related_name='fields')
    field_type = models.CharField(max_length=255, choices=CalcFieldType.choices)
    label = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    default_value = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    is_required = models.BooleanField(default=True)
    min_value = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    max_value = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    step = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    position = models.PositiveSmallIntegerField(default=1)

    class Meta:
        db_table = 'calculator_fields'
        unique_together = ('calculator', 'name')
        verbose_name = 'Поле калькулятора'
        verbose_name_plural = 'Поля калькулятора'


class CalcFieldChoice(ModelWithDate):
    field = models.ForeignKey(CalcField, on_delete=models.CASCADE, related_name='choices')
    label = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    class Meta:
        db_table = 'calculator_field_items'
        verbose_name = 'Варианты для выбора'
        verbose_name_plural = 'Варианты для выбора'


class BugReportSetting(SingletonModel):
    title = models.CharField(max_length=255, default='Охота на баги')

    class Meta:
        db_table = 'bug_report_settings'
        verbose_name = 'Настройки раздела Багов'
        verbose_name_plural = 'Настройки раздела Багов'


class BugReport(ModelWithDate):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    file = models.ImageField(upload_to='bugreports/', null=True, blank=True)

    class Meta:
        db_table = 'bug_reports'
        verbose_name = 'Баги'
        verbose_name_plural = 'Баги'
        ordering = ('-created_at',)


class ResourcePolicy(models.Model):
    heading = models.CharField(max_length=255)
    content = models.TextField()
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'dvi_resource_policy'
        verbose_name = 'Правила и политика ресурса'
        verbose_name_plural = 'Правила и политика ресурса'
        ordering = ('position',)