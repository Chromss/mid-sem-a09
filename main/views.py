import base64
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .models import Journal, Souvenir, Itinerary
from .jurnalform import JournalForm
from django.http import JsonResponse
import json
from django.core import serializers
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt



@login_required
def landing_page(request):
    return render(request, 'main/landing_page.html', {'user': request.user})


@login_required(login_url='/login')
def journal_home(request):
    journals = Journal.objects.all().order_by('-created_at')

    # Membaca data dari file JSON
    with open('main/DATASET.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Memasukkan data ke dalam model Souvenir
    for item in data:
        Souvenir.objects.get_or_create(
            name=item['Product Name'],
            defaults={
                'price': item['Price'],
                'description': item['Description Product'],
                'place_name': item['Place Name']
            }
        )

    # Ambil semua souvenir dari database
    souvenirs = Souvenir.objects.all()

    # Filter berdasarkan nama tempat
    place_name_filter = request.GET.get('place_name')
    if place_name_filter:
        souvenirs = souvenirs.filter(place_name=place_name_filter)

    # Filter berdasarkan harga
    price_filter = request.GET.get('price')
    if price_filter == 'low_to_high':
        souvenirs = souvenirs.order_by('price')
    elif price_filter == 'high_to_low':
        souvenirs = souvenirs.order_by('-price')

    # Ambil semua nama tempat untuk dropdown
    places = Souvenir.objects.values_list('place_name', flat=True).distinct()

    return render(request, 'main/journal_home.html', {
        'journals': journals,
        'souvenirs': souvenirs,
        'places': places,
    })
   
@login_required
@csrf_exempt
def create_journal(request):
    if request.method == 'POST':
        try:
            # Ambil data dari form
            title = request.POST.get('title')
            content = request.POST.get('content')
            place_name = request.POST.get('place_name')
            souvenir_id = request.POST.get('souvenir')
            
            # Buat journal baru
            journal = Journal(
                author=request.user,
                title=title,
                content=content,
                place_name=place_name
            )
            
            # Handle souvenir jika ada
            if souvenir_id:
                try:
                    souvenir = Souvenir.objects.get(id=souvenir_id)
                    journal.souvenir = souvenir
                except Souvenir.DoesNotExist:
                    pass
            
            # Handle image jika ada
            if 'image' in request.FILES:
                journal.image = request.FILES['image']
            
            journal.save()
            
            return JsonResponse({
                'success': True, 
                'journal_id': journal.id,
                'message': 'Journal created successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
            
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@login_required(login_url='/login')
def like_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    if request.user.is_authenticated:
        if request.user in journal.likes.all():
            journal.likes.remove(request.user)  # Hapus like jika sudah ada
            liked = False
        else:
            journal.likes.add(request.user)  # Tambah like jika belum ada
            liked = True
        return JsonResponse({'liked': liked, 'likes_count': journal.likes.count()})
    return JsonResponse({'error': 'User not authenticated'}, status=401)

def souvenir_list(request):
    souvenirs = Souvenir.objects.all()

    # Filter berdasarkan harga
    price_filter = request.GET.get('price')
    if price_filter == 'low_to_high':
        souvenirs = souvenirs.order_by('price')
    elif price_filter == 'high_to_low':
        souvenirs = souvenirs.order_by('-price')

    # # Filter berdasarkan rating
    # rating_filter = request.GET.get('rating')
    # if rating_filter == 'high_to_low':
    #     souvenirs = souvenirs.order_by('-rating')
    # elif rating_filter == 'low_to_high':
    #     souvenirs = souvenirs.order_by('rating')

    return render(request, 'main/souvenir_list.html', {'souvenirs': souvenirs})


@login_required(login_url='/login')
def journal_history(request):
    journals = Journal.objects.filter(author=request.user)
    return render(request, 'main/journal_history.html', {'journals': journals})

def specific_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    return render(request, 'main/specific_journal.html', {'journal': journal})

@login_required(login_url='/login')
def edit_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    
    if request.method == 'POST':
        try:
            # Update basic fields
            journal.title = request.POST.get('title')
            journal.content = request.POST.get('content')
            journal.place_name = request.POST.get('place_name')
            
            # Update souvenir if provided
            souvenir_id = request.POST.get('souvenir')
            if souvenir_id:
                try:
                    souvenir = Souvenir.objects.get(id=souvenir_id)
                    journal.souvenir = souvenir
                except Souvenir.DoesNotExist:
                    journal.souvenir = None
            else:
                journal.souvenir = None
            
            # Handle image update
            if 'image' in request.FILES:
                journal.image = request.FILES['image']
            
            journal.save()
            
            # Prepare response data
            response_data = {
                'success': True,
                'title': journal.title,
                'content': journal.content,
                'place_name': journal.place_name,
                'image_url': journal.image.url if journal.image else None,
            }
            
            if journal.souvenir:
                response_data['souvenir'] = {
                    'id': journal.souvenir.id,
                    'name': journal.souvenir.name,
                    'price': str(journal.souvenir.price)
                }
            
            return JsonResponse(response_data)
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
            
    elif request.method == 'GET':
        # Return journal data for editing
        data = {
            'title': journal.title,
            'content': journal.content,
            'place_name': journal.place_name,
            'image_url': journal.image.url if journal.image else None,
            'souvenir_id': journal.souvenir.id if journal.souvenir else None
        }
        return JsonResponse(data)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required(login_url='/login')
def delete_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id, author=request.user)
    journal.delete()
    return redirect('main:journal_home')

@login_required
def save_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    SavedJournal.objects.get_or_create(journal=journal, user=request.user)
    return redirect('journal_home')

def journal_detail(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    return render(request, 'main/spesific_journal.html', {'journal': journal})


def register(request):
    form = UserCreationForm()
    last_login = request.COOKIES.get('last_login', 'Never')

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form': form, 'last_login': last_login}
    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:journal_home')  # Arahkan ke journal_home setelah login
            else:
                form.add_error(None, "Invalid username or password.")  # Tambahkan error jika autentikasi gagal
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response


def show_xml(request):
    # Get all journals for the current user
    data = Journal.objects.filter(author=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    # Get all journals for the current user
    data = Journal.objects.filter(author=request.user)
    print(data)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    # Get a specific journal by ID
    data = Journal.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    # Get a specific journal by ID
    data = Journal.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_itin(request):
    # Get all journals for the current user
    data = Itinerary.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_itin(request):
    # Get all journals for the current user
    itineraries = Itinerary.objects.all()
    return HttpResponse(serializers.serialize("json", itineraries), content_type="application/json")

def show_xml_by_id_itin(request, id):
    # Get a specific journal by ID
    data = Itinerary.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id_itin(request, id):
    # Get a specific journal by ID
    data = Itinerary.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

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

@login_required
def get_places(request):
    places = Souvenir.objects.values_list('place_name', flat=True).distinct()
    return JsonResponse({'places': list(places)})

@login_required
def get_souvenirs(request):
    place_name = request.GET.get('place_name')
    souvenirs = Souvenir.objects.filter(place_name=place_name).values('id', 'name')
    return JsonResponse({'souvenirs': list(souvenirs)})
# @login_required
# def get_places(request):
#     places = Souvenir.objects.values_list('place_name', flat=True).distinct()
#     return JsonResponse({'places': list(places)})

# @login_required
# def get_souvenirs(request):
#     place_name = request.GET.get('place_name')
#     souvenirs = Souvenir.objects.filter(place_name=place_name).values('id', 'name')
#     return JsonResponse({'souvenirs': list(souvenirs)})


# @csrf_exempt
# def create_journal_flutter(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
        
#         # Adjusted to match the Fields structure in your journal entry
#         new_entry = Journal.objects.create(
#             model="JournalEntry",  # Assuming you want to set a model name
#             pk=None,  # Auto-incremented primary key
#             author=request.user,
#             title=data["title"],
#             content=data["content"],
#             created_at=datetime.datetime.now(),
#             updated_at=datetime.datetime.now(),
#             image=data.get("image", ""),
#             souvenir_id=data.get("souvenir"),
#             place_name=data.get("place_name"),
#         )

#         new_entry.save()

#         return JsonResponse({"status": "success"}, status=200)
#     else:
#         return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def create_journal_flutter(request):
    if request.method == 'POST':
        try:
            # Decode JSON data
            data = json.loads(request.body)
            
            # Extract data
            title = data.get('title')
            content = data.get('content')
            place_name = data.get('place_name')
            souvenir_id = data.get('souvenir')
            image_base64 = data.get('image')

            # Create journal
            journal = Journal.objects.create(
                author=request.user,
                title=title,
                content=content,
                place_name=place_name
            )

            # Handle souvenir if provided
            if souvenir_id:
                try:
                    souvenir = Souvenir.objects.get(id=int(souvenir_id))
                    journal.souvenir = souvenir
                except Souvenir.DoesNotExist:
                    pass

            # Handle image if provided
            if image_base64:
                try:
                    # Decode base64 image
                    image_data = base64.b64decode(image_base64)
                    journal.image.save(f'journal_image_{journal.id}.jpg', ContentFile(image_data), save=True)
                except Exception as e:
                    print(f"Error saving image: {e}")

            journal.save()

            return JsonResponse({"status": "success"})

        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


# views.py
def get_journals_json(request):
    journals = Journal.objects.all().order_by('-created_at')
    return JsonResponse([{
        'model': 'main.journal',
        'pk': journal.id,
        'fields': {
            'author': journal.author.id,
            'author_username': journal.author.username,
            'title': journal.title,
            'content': journal.content,
            'created_at': journal.created_at.isoformat(),
            'updated_at': journal.updated_at.isoformat(),
            'image': journal.image.url if journal.image else '',
            'place_name': journal.place_name,
            'souvenir': journal.souvenir.id if journal.souvenir else None,
            'likes': list(journal.likes.values_list('id', flat=True)),
        }
    } for journal in journals], safe=False)
# @csrf_exempt
# def create_journal_flutter(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
            
#             # Create journal entry directly
#             new_entry = JournalEntry.objects.create(
#                 author=request.user,
#                 title=data["title"],
#                 content=data["content"],
#                 place_name=data.get("place_name", ""),
#                 souvenir_id=data.get("souvenir"),  # Assuming this is the souvenir ID
#                 image=data.get("image", "")
#             )

#             return JsonResponse({
#                 'status': 'success',
#                 'message': 'Journal created successfully',
#                 'data': {
#                     'id': new_entry.id,
#                     'title': new_entry.title
#                 }
#             })
#         except Exception as e:
#             print(f"Error: {str(e)}")  # For debugging
#             return JsonResponse({
#                 'status': 'error',
#                 'message': str(e)
#             }, status=400)
    
#     return JsonResponse({
#         'status': 'error',
#         'message': 'Invalid request method'
#     }, status=405)

# def get_journals_json(request):
#     journals = Journal.objects.all()
#     return JsonResponse([{
#         'model': 'main.journal',
#         'pk': journal.id,
#         'fields': {
#             'author': journal.author.id,
#             'username': journal.author.username,  # Add this line to include username
#             'title': journal.title,
#             'content': journal.content,
#             'created_at': journal.created_at.isoformat(),
#             'updated_at': journal.updated_at.isoformat(),
#             'image': journal.image.url if journal.image else '',
#             'souvenir': journal.souvenir.id if journal.souvenir else None,
#             'place_name': journal.place_name,
#             'likes': list(journal.likes.values_list('id', flat=True)),
#         }
#     } for journal in journals], safe=False)