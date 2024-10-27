# views.py
from django.shortcuts import render, get_object_or_404
from .models import Collection
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["DELETE"])
def delete_collection(request, collection_id):
    try:
        collection = Collection.objects.get(id=collection_id)
        collection.delete()
        return JsonResponse({'success': True})
    except Collection.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Collection not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def create_collection(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            try:
                collection = Collection.objects.create(name=name)
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
    collections = Collection.objects.all()
    return render(request, "collection.html", {
        'collections': collections,
    })


def show_collection_places(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    places = collection.places.all()
    return render(request, 'collection_places.html', {
        'collection': collection,
        'places': places
    })
