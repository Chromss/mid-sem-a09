# views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CollectionForm
from .models import PlaceCollection

def create_collection(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Cara modern mengecek AJAX
        try:
            name = request.POST.get('name')
            if not name:
                return JsonResponse({
                    'success': False,
                    'message': 'Collection name is required'
                })
            
            collection = PlaceCollection.objects.create(name=name)
            
            return JsonResponse({
                'success': True,
                'collection': {
                    'name': collection.name,
                    'id': collection.id,
                    'created_at': collection.created_at.strftime('%B %d, %Y')
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    # Untuk non-AJAX requests
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save()
            return redirect('placecollections:show_collections')
    else:
        form = CollectionForm()

    return render(request, 'placecollections/create_collection.html', {'form': form})

def show_collections(request):
    collections = PlaceCollection.objects.all().order_by('-created_at')
    return render(request, "placecollections/collections.html", {'collections': collections})