from rest_framework import authentication
from rest_framework import exceptions

from apps.users.services.auth import user_service, InvalidToken


class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTESSSSSSSSST")
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        return None
        '''if jwt_token is None:
            return None #raise exceptions.AuthenticationFailed()
        try:
            user = user_service.get_user(jwt_token)
            return user, None
        except InvalidToken as e:
            raise exceptions.AuthenticationFailed(str(e))
            # return Noneraise exceptions.AuthenticationFailed(e)'''