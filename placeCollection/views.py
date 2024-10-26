# views.py
from django.shortcuts import render, get_object_or_404
from .models import PlaceCollection
from django.http import JsonResponse

def create_collection(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            try:
                collection = PlaceCollection.objects.create(name=name)
                created_at = collection.created_at.strftime('%b %d, %Y')
                return JsonResponse({
                    'success': True,
                    'name': collection.name,
                    'created_at': created_at,
                    'id': collection.id
                })
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        return JsonResponse({'success': False, 'error': 'Name is required'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def show_collections(request):
    collections = PlaceCollection.objects.all()
    return render(request, "collection.html", {
        'collections': collections,
    })

def show_collection_places(request, collection_id):
    collection = get_object_or_404(PlaceCollection, id=collection_id)
    places = collection.places.all()
    return render(request, 'collection_places.html', {
        'collection': collection,
        'places': places,
    })