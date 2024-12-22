from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token


from django.contrib.auth.models import User
import json
from django.contrib.auth import logout as auth_logout

# Create your views here.
@csrf_exempt
def login(request):
    print("Login request received")
    print("Session before login:", request.session.session_key)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)


    if user is not None and user.is_active:
        # Login the user and create session
        auth_login(request, user)
        request.session.save()
        session_key = request.session.session_key
        print("Session after login:", session_key)
        print("Session data:", dict(request.session))
        
        # Create response
        response = JsonResponse({
            "username": user.username,
            "status": True,
            "message": "Login sukses!",
            "sessionid": session_key,
        })
        
        # Set session cookie
        response.set_cookie(
            'sessionid',
            session_key,
            httponly=False,     # Allow JavaScript access
            samesite='None',    # Allow cross-site cookies
            secure=False,       # Set to True in production with HTTPS
            max_age=1209600,    # 2 weeks
            domain='127.0.0.1', # Match your backend domain
            path='/'           # Allow cookie for all paths
        )
        
        # Set CORS headers
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Origin"] = "http://localhost:57880"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, X-CSRFToken"
        
        return response
    else:
        error_response = JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)
        
        # Add CORS headers to error response as well
        error_response["Access-Control-Allow-Credentials"] = "true"
        error_response["Access-Control-Allow-Origin"] = "http://localhost:57880"
        
        return error_response




# @csrf_exempt
# def login(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         if user.is_active:
#             auth_login(request, user)
#             return JsonResponse({
#                 "username": user.username,
#                 "status": True,
#                 "message": "Login sukses!"
#             }, status=200)
#         else:
#             return JsonResponse({
#                 "status": False,
#                 "message": "Login gagal, akun dinonaktifkan."
#             }, status=401)

#     else:
#         return JsonResponse({
#             "status": False,
#             "message": "Login gagal, periksa kembali email atau kata sandi."
#         }, status=401)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
        
        # Create the new user
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        
        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)
    
@csrf_exempt
def logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)
