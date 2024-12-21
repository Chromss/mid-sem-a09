from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core import serializers
from .models import Collection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Collection

from django.middleware.csrf import get_token
from django.http import JsonResponse

def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})


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
    return render(request, 'collection.html')



@login_required
@csrf_exempt
@require_http_methods(["DELETE"]) 
def delete_collection(request, collection_id):
    if request.method == 'DELETE':  # Add this check
        try:
            collection = Collection.objects.get(id=collection_id, user=request.user)
            collection.delete()
            return JsonResponse({'success': True})
        except Collection.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Collection not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

@login_required
@csrf_exempt
@require_http_methods(["POST"]) 
def delete_collection_flutter(request, collection_id):
    if request.method == 'POST':  # Add this check
        try:
            print("hai")
            collection = Collection.objects.get(id=collection_id, user=request.user)
            collection.delete()
            return JsonResponse({'success': True})
        except Collection.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Collection not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

@login_required
@csrf_exempt
def create_collection_json(request):
    print("Request method:", request.method)  # Debug print
    print("Request body:", request.body)  # Debug print

    if request.method == 'POST':
        try:
            # Try different ways of parsing the request body
            try:
                # Try parsing as JSON
                data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError:
                # Try parsing as form data
                data = request.POST.dict()
                if not data:
                    data = dict(request.POST)

            print("Parsed data:", data)  # Debug print

            # Validate name
            name = data.get('name')
            if not name:
                return JsonResponse({
                    'success': False, 
                    'error': 'Name is required'
                }, status=400)
            
            # Create collection
            collection = Collection.objects.create(
                name=name, 
                user=request.user  # Ensure user is authenticated
            )
            
            # Return success response
            return JsonResponse({
                'success': True, 
                'collection': {
                    'id': collection.id,
                    'name': collection.name
                }
            }, status=201)
        
        except Exception as e:
            print("Error:", str(e))  # Debug print
            return JsonResponse({
                'success': False, 
                'error': str(e)
            }, status=500)
    
    # If not a POST request
    return JsonResponse({
        'success': False, 
        'error': 'Method not allowed'
    }, status=405)

# 3. Show All Collections
@login_required
def show_collections(request):
    """
    Tampilkan semua koleksi user dalam HTML.
    """
    collections = Collection.objects.filter(user=request.user)
    return render(request, "collection.html", {
        'collections': collections,
    })


# 4. Show Collections as JSON
@login_required
def show_json(request):
    """
    Endpoint untuk menampilkan semua koleksi user dalam format JSON.
    """
    collections = Collection.objects.filter(user=request.user)
    data = serializers.serialize("json", collections)
    return HttpResponse(data, content_type="application/json")

def show_collection_places(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    places = collection.places.all()
    return render(request, 'collection_places.html', {
        'collection': collection,
        'places': places
    })

# 5. Show Collection Places
@login_required
def show_json_collection_places(request, collection_id):
    """
    Tampilkan semua tempat dalam koleksi tertentu dalam format JSON.
    """
    try:
        collection = get_object_or_404(Collection, id=collection_id, user=request.user)
        places = collection.places.all()

        places_data = [
            {
                "id": place.id,
                "name": place.name,
                "description": place.description,
                "image_url": place.image.url if hasattr(place, 'image') and place.image else None,
                # Hapus price dan stock karena tidak ada di model Place
                # Tambahkan field lain yang ada di model Place jika diperlukan
            }
            for place in places
        ]

        return JsonResponse({
            "success": True,
            "collection": collection.name,
            "places": places_data
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)

# 6. Delete Collection

def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

# 7. Show Collections as XML
@login_required
def show_xml(request):
    """
    Endpoint untuk menampilkan koleksi user dalam format XML.
    """
    collections = Collection.objects.filter(user=request.user)
    data = serializers.serialize("xml", collections)
    return HttpResponse(data, content_type="application/xml")
