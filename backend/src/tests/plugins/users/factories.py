import datetime
import random
from typing import List

import jwt
import pytest
from django.conf import LazySettings, settings
from mixer.backend.django import mixer

from mimesis import Address, Person, Datetime, Numeric, Text, Cryptographic
from mimesis.builtins import RussiaSpecProvider
from pydantic.dataclasses import dataclass

from apps.dv_info_site.models import (
    MainPageSlider,
    MainPageButtonBlock,
    MainPageReputationLink,
    Retail,
    Contact,
    FAQ,
    Vacancy,
    Partnership,
    Project,
    ProjectLink,
    DVInstruction,
    Country,
    City,
    Product,
    ProductImage,
    ProductItem,
    ProductUpdateFile
)
from apps.users.models import User
from apps.users.utils import UserRole
from tests.plugins.utils import generate_translate_field_value


@pytest.fixture()
def get_user():
    def factory(*args, **kwargs) -> User:
        user_id = kwargs.get('user_id', 1)
        role = kwargs.get('role', UserRole.OWNER)
        user = mixer.blend(
            User,
            user_id=user_id,
            role=role
        )
        return user

    return factory


@pytest.fixture()
def get_user_jwt():
    def factory(*args, **kwargs) -> str:
        user_id = kwargs.get('user_id', 1)
        role = kwargs.get('role', UserRole.OWNER)
        return jwt.encode(
            payload={
                'id': user_id,
                'role': role,
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)

            },
            key=settings.AUTH_JWT_SECRET,
            algorithm=settings.AUTH_JWT_ALGORITHMS[0]
        )

    return factory
