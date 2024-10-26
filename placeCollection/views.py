from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CollectionForm
from .models import Collection
from django.shortcuts import render, get_object_or_404
# from .models import Place  # Asumsi model Place sudah ada nantinya

def show_collection_places(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    # places = Place.objects.filter(collection=collection)  # Asumsi akan ada relasi ke Collection
    context = {
        'collection': collection,
        # 'places': places,
    }
    return render(request, "collection_places.html", context)


def show_collections(request):
    collection = Collection.objects.all()
    context = {
        'collection': collection,  # Mengirimkan daftar koleksi ke template
    }
    return render(request, "collection.html", context)

def create_collection(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            collection = Collection.objects.create(name=name)
            created_at = collection.created_at.strftime('%b %d, %Y')  # Format date manually
            return JsonResponse({
                'success': True,
                'name': collection.name,
                'created_at': created_at,
                'id': collection.id
            })
        return JsonResponse({'success': False, 'error': 'Name is required'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
