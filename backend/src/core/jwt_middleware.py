import json
import requests
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse

User = get_user_model()

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Пропускаем запросы к статическим файлам и админке
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        # Проверяем наличие jwt в GET параметрах
        jwt_token = request.GET.get('jwt')
        
        if jwt_token and not request.user.is_authenticated:
            try:
                # Отправляем запрос в общую админку для проверки токена
                response = requests.post(
                    f"{settings.MAIN_ADMIN_URL}/adm/api/jwt_user",
                    json={"token": jwt_token},
                    timeout=5
                )
                
                if response.status_code == 200:
                    user_data = response.json()
                    
                    # Получаем или создаем пользователя
                    user, created = User.objects.get_or_create(
                        username=user_data['login'],
                        defaults={
                            'email': user_data.get('email', ''),
                            'first_name': user_data.get('name', ''),
                            'is_staff': True,  # Даем доступ к админке
                            'is_active': True
                        }
                    )
                    
                    if created:
                        # Устанавливаем случайный пароль для нового пользователя
                        user.set_password(User.objects.make_random_password())
                        user.save()
                    
                    # Авторизуем пользователя
                    login(request, user)
                else:
                    return HttpResponseRedirect(reverse('admin:login'))
                    
            except Exception as e:
                print(f"JWT authentication error: {str(e)}")
                return HttpResponseRedirect(reverse('admin:login'))
        
        response = self.get_response(request)
        return response
