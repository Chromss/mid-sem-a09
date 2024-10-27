import datetime as d
from django.shortcuts import *
from django.contrib import *
from django.contrib.auth import *
from django.contrib.auth.forms import *
from django.contrib.auth.decorators import *
from django.core import serializers
from django.http import *
from django.views.decorators.csrf import *
from django.views.decorators.http import *
from django.utils.html import *
from django.urls import reverse
from main.forms import *
from main.models import *

def signup(request):
    return render(request, 'signup.html')

def signup_next(request):
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main:login')
    context = {'form': form}
    return render(request, 'signup_next.html', context)

def login_user(request):
    form = AuthenticationForm(request)
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:landing_page"))
            response.set_cookie('last_login', str(d.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            return response
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponse()
    response.delete_cookie('last_login')
    return response

def landing_page(request):
    return render(request, 'landing_page.html')

def about(request):
    user_data = None
    if request.user.is_authenticated:
        user_data = {
            'name': request.user.name,
            'username': request.user.username,
            'profile_picture': request.user.profile_picture.url
        }
    context = {'user': user_data}
    return render(request, 'about.html', context)

def show_xml(request):
    data = MlakuMlakuUser.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")