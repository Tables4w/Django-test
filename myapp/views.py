import MySQLdb
import os
import base64
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from myapp.models import Avatar
import json

# Подключение к БД
def get_db_connection():
    return MySQLdb.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        passwd=os.environ.get('DB_PASSWORD'),
        db=os.environ.get('DB_NAME'),
        charset='utf8mb4'
    )

# SSR и бэкэнд-логика login
User = get_user_model()

@ensure_csrf_cookie
def register_view(request):
    if (request.method != 'POST') and (request.method != 'GET'):
        return JsonResponse({'status': 'error', 'message': 'Only POST/GET allowed' + ' not ' + request.method}, status=405)
    
    elif request.method == 'GET':
        return render(request, 'myapp/register.html')
    
    else: 
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            gender = request.POST.get('gender')
            image_file = request.FILES.get('avatar')

            if any(val in ['', ' ', None, Ellipsis] for val in [username, password, gender]):
                return JsonResponse({'status': 'error', 'message': 'Invalid input'})

            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 'error', 'message': 'Username already exists'})

            if image_file:
                image_data = image_file.read()
            else:
                default_path = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'default_avatar.png')
                with open(default_path, 'rb') as f:
                    image_data = f.read()

            user = User.objects.create_user(username=username, password=password, gender=gender)
            Avatar.objects.create(user=user, image=image_data)
            return JsonResponse({'status': 'success', 'message': 'User registered successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

@ensure_csrf_cookie
def login_view(request):
    if (request.method != 'POST') and (request.method != 'GET'):
        return JsonResponse({'status': 'error', 'message': 'Only POST/GET allowed'}, status=405)
    
    elif request.method == 'GET':
        return render(request, 'myapp/login.html')

    else:
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            if any(val in ['', ' ', None, Ellipsis] for val in [username, password]):
                return JsonResponse({'status': 'error', 'message': 'Invalid input'})

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'success', 'message': 'Login successful, your gender: ' + user.gender})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid username or password'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        
@login_required(login_url='/login/')
@ensure_csrf_cookie
def home_view(request):
    avatar_base64 = None
    try:
        avatar = request.user.avatar_set.first()
        avatar_base64 = base64.b64encode(avatar.image).decode('utf-8')
        print("Ok")
    except Exception as e:
        print(e)
        pass
    

    return render(request, 'myapp/home.html', {
        'avatar_base64': avatar_base64
    })

@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return JsonResponse({'status': 'success', 'message': 'Logged out'})