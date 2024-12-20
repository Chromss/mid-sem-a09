# views.py
from django.shortcuts import render, get_object_or_404
from .models import Collection
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core import serializers


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

# views.py
from django.contrib.auth.decorators import login_required

@login_required
def create_collection(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            try:
                collection = Collection.objects.create(name=name, user=request.user)  # Menambahkan user
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
    return render(request, 'create_collection.html')
# @login_required(login_url='login')
# def create_collection(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         if name:
#             try:
#                 collection = Collection.objects.create(name=name)
#                 created_at = collection.created_at.strftime('%b %d, %Y')
#                 return JsonResponse({
#                     'success': True,
#                     'name': collection.name,
#                     'created_at': created_at,
#                     'id': collection.id
#                 })
#             except Exception as e:
#                 return JsonResponse({'success': False, 'error': str(e)})
#         return JsonResponse({'success': False, 'error': 'Name is required'})
#     return render(request, 'placeCollection/create_collection.html')
#     # return JsonResponse({'success': False, 'error': 'Invalid request method'})

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

def show_xml(request):
    # Get all journals for the current user
    data = Collection.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@login_required
def show_json(request):
    # Get all journals for the current user
    data = Collection.objects.filter(user=request.user)
    print(data)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required
def show_json_collection_places(request, collection_id):
    """
    Returns JSON data for all places in a specific collection.
    """
    try:
        collection = get_object_or_404(Collection, id=collection_id, user=request.user)
        places = collection.places.all()

        places_data = [
            {
                "id": place.id,
                "name": place.name,
                "description": place.description,
                "image_url": place.image.url if place.image else None,
                "price": place.price,
                "stock": place.stock,
            }
            for place in places
        ]

        return JsonResponse({"collection": collection.name, "places": places_data}, safe=False)

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

