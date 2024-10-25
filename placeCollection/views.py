from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CollectionForm
from .models import PlaceCollection


def show_collections(request):
    collection = PlaceCollection.objects.all()
    context = {
        'collection': collection,  # Mengirimkan daftar koleksi ke template
    }
    return render(request, "collection.html", context)
