from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CollectionForm
from .models import PlaceCollection


def show_collections(request):
    collections = PlaceCollection.objects.all()
    context = {
        'collections': collections,  # Mengirimkan daftar koleksi ke template
    }
    return render(request, "collections.html", context)
