from django.db.models import TextChoices


class UserRole(TextChoices):
    OWNER = 'owner', 'Администратор'
    CONTENT_MANAGER = 'content_manager', 'Контента менеджер'
    OPT_MANAGER = 'opt_manager', 'OPT manager'
