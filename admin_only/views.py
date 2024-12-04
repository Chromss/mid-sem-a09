from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from places.models import *
from django.http import HttpResponse
from django.core import serializers
from django.core.files.storage import default_storage
import os

def show_json_place(request):
    data = Place.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_souvenir(request):
    place_pk = request.GET.get('place_pk', None)
    if place_pk:
        try:
            place = Place.objects.get(pk=place_pk)
            souvenirs = Souvenir.objects.filter(place=place)
        except Place.DoesNotExist:
            return HttpResponse('Place not found', status=404)
    else:
        souvenirs = Souvenir.objects.all()
    return HttpResponse(serializers.serialize("json", souvenirs), content_type="application/json")

def show_places(request):
    places = Place.objects.all()
    places_data = [
        {'id': place.id, 'name': place.name, 'description': place.description}
        for place in places
    ]
    return JsonResponse({'places': places_data})

@csrf_exempt
def create_place(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        place = Place.objects.create(name=name, description=description, image=image)
        return JsonResponse({'id': place.id, 'name': place.name})
    return JsonResponse({'error': 'Invalid method'}, status=400)

@csrf_exempt
def create_souvenir(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        place_id = request.POST.get('place')
        image = request.FILES.get('image')

        if not all([name, price, stock, place_id, image]):
            return JsonResponse({'error': 'All fields are required!'}, status=400)

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            return JsonResponse({'error': 'Price must be a number and stock must be an integer!'}, status=400)

        place = get_object_or_404(Place, id=place_id)
        souvenir = Souvenir(name=name, price=price, stock=stock, image=image, place=place)
        souvenir.save()
        return JsonResponse({
            'id': souvenir.id,
            'name': souvenir.name,
            'price': souvenir.price,
            'stock': souvenir.stock,
            'place_name': place.name,
        }, status=201)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def update_place(request, place_id):
    place = Place.objects.get(id=place_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        place.name = name
        place.description = description

        if image:
            image_path = default_storage.save(os.path.join('places', image.name), image)
            place.image = image_path
        place.save()

        return JsonResponse({
            "id": place.id,
            "name": place.name,
            "description": place.description,
            "image": place.image.url if place.image else None
        })
    return JsonResponse({"error": "Invalid request"}, status=400)

# Delete a place
@csrf_exempt
def delete_place(request, place_id):
    try:
        place = Place.objects.get(id=place_id)
        place.delete()
        return JsonResponse({"success": True})
    except Place.DoesNotExist:
        return JsonResponse({"error": "Place not found"}, status=404)

def assign(request):
    if not request.session.get('is_admin'):
        return redirect('/admin/login/')
    places = Place.objects.all()
    return render(request, 'assign.html', {'places': places})

def login_admin(request):
    if request.method == "POST":
        password = request.POST.get("credential")
        if password == "adminmlaku123":
            request.session['is_admin'] = True
            return redirect('/admin/assign/')
        return HttpResponse("""
            <html>
                <head>
                    <title>Invalid Credentials</title>
                    <script type="text/javascript">
                        alert("Invalid credential.");
                        window.location.href = '/admin/login/';
                    </script>
                </head>
            </html>
        """)
    if request.session.get('is_admin'):
        return redirect('/admin/assign/')
    return render(request, 'portal.html')

def logout_admin(request):
    request.session.flush()
    return redirect('/admin/login/')