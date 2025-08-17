import jwt
from django.conf import settings
from django.db import transaction
from jwt import ExpiredSignatureError, InvalidTokenError

from apps.users.models import User


class InvalidToken(Exception):
    pass


class AuthService:
    @transaction.atomic
    def get_user(self, jwt_token) -> User:
        try:
            user_info = self.get_user_info(jwt_token)
            user = User.objects.filter(id=user_info['id']).first()
            if user is None:
                user = User.objects.create(user_id=user_info['id'], role=user_info['role'])
            return user
        except InvalidToken as e:
            raise InvalidToken(str(e))

    @staticmethod
    def get_user_info(jwt_token: str) -> dict:
        """
        Проверяет валидность JWT токена и возвращает данные, содержащиеся в токене.
        return: {
            'id': int,
            'role': str
        }
        """
        try:
            decoded_data = jwt.decode(jwt_token, settings.AUTH_JWT_SECRET, algorithms=settings.AUTH_JWT_ALGORITHMS)
            data = {
                'id': decoded_data['id'],
                'role': decoded_data['role']
            }
            return data
        except ExpiredSignatureError:
            raise InvalidToken("Токен истёк")
        except InvalidTokenError:
            raise InvalidToken("Недействительный токен")


user_service = AuthService()
