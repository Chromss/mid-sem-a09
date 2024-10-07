import datetime as d
from django.shortcuts import *
from django.contrib import *
from django.contrib.auth import *
from django.contrib.auth.forms import *
from django.contrib.auth.decorators import *
from django.core import *
from django.http import *
from django.views.decorators.csrf import *
from django.views.decorators.http import*
from django.utils.html import *
from main.forms import *
from main.models import *

def test(request):
    return render(request, 'test.html')

def landing_page(request):
    return render(request, 'landing_page.html')