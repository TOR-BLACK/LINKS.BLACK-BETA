from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.core.cache import cache
from django.db import models

from apps.users.utils import UserRole


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create(self, user_id: int, role: str):
        user = self.model(
            id=user_id,
            role=role,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.model(
            id=kwargs.get('id'),
            role=UserRole.OWNER,
            is_superuser=True,
        )
        user.set_password(kwargs.get('password'))
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigIntegerField(primary_key=True)
    role = models.CharField(max_length=255, choices=UserRole.choices)

    USERNAME_FIELD = 'id'
    objects = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def permissions(self) -> list:
        user_key = settings.USER_CHANNELS_CACHE_KEY.format(user_id=self.pk)
        data = cache.get(user_key, list())
        return data

    @permissions.setter
    def permissions(self, value: list) -> None:
        user_key = settings.USER_CHANNELS_CACHE_KEY.format(user_id=self.pk)
        cache.set(user_key, value, settings.USER_CHANNELS_CACHE_TIMEOUT)

    @property
    def is_staff(self) -> bool:
        return self.role == UserRole.OWNER
