from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

@csrf_exempt
def login(request):
    print("Login request received")
    print("Session before login:", request.session.session_key)

    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return JsonResponse({
            "status": False,
            "message": "Username and password are required."
        }, status=400)

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