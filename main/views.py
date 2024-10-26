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
from .models import Itinerary
from django.shortcuts import render, get_object_or_404

def test(request):
    return render(request, 'test.html')

def landing_page(request):
    return render(request, 'landing_page.html')

def show_itineraries(request):
    itineraries = Itinerary.objects.all()  # Mendapatkan semua itinerary
    return render(request, 'itinerary_list.html', {'itineraries': itineraries})

# View untuk menampilkan daftar itinerary
def itinerary_list(request):
    itineraries = Itinerary.objects.all()
    return render(request, 'itinerary_list.html', {'itineraries': itineraries})

# View untuk menampilkan detail itinerary
def itinerary_detail(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk)
    return render(request, 'itinerary_detail.html', {'itinerary': itinerary})

def landing_page(request):
    return render(request, 'landing_page.html', {'user': request.user})


