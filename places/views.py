# places/views.py

import json
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Avg, Count, Q
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from .models import Place, Comment

# Import your models here
from .models import Place, Souvenir, Comment

# Import the Collection models
from placeCollection.models import Collection, CollectionItem  # Added import

def format_price(price):
    """Formats the price with commas (e.g., 10000 -> 10,000)."""
    return "{:,}".format(price)

def place_detail(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    
    # Aggregate average rating
    average_rating = Comment.objects.filter(place=place).aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Fetch all souvenirs for the place
    souvenirs = Souvenir.objects.filter(place=place)
    
    # Calculate total and available souvenirs
    total_souvenirs_count = souvenirs.count()
    available_souvenirs_count = souvenirs.filter(stock__gt=0).count()

    # Format the price for each souvenir
    for souvenir in souvenirs:
        souvenir.formatted_price = format_price(souvenir.price)

    # Fetch the latest 10 comments
    comments = Comment.objects.filter(place=place).order_by('-created_at')[:10]  # Limit to recent 10 reviews

    # Get the user's collections if authenticated
    user_collections = Collection.objects.filter(user=request.user) if request.user.is_authenticated else []

    context = {
        'place': place,
        'average_rating': round(average_rating, 1),
        'souvenirs': souvenirs,
        'comments': comments,
        'user_collections': user_collections,  # Added to context
        'total_souvenirs_count': total_souvenirs_count,  # New context variable
        'available_souvenirs_count': available_souvenirs_count,  # New context variable
    }
    return render(request, 'places/place_detail.html', context)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Path to your custom login template
    redirect_authenticated_user = True  # Redirect users who are already logged in

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse_lazy('home')  # Replace 'home' with your desired default view name

# @login_required
# @csrf_exempt
# def add_comment_ajax(request, place_id):
#     print(f"Request method: {request.method}")
#     print(f"Request headers: {request.headers}")
#     print(f"Request body: {request.body}")

#     if request.method == 'POST':  # Removed x-requested-with for now
#         try:
#             # Parse JSON body
#             data = json.loads(request.body)
#             print(f"Parsed data: {data}")

#             content = data.get('comment')  # Ensure this matches your JSON key
#             rating = data.get('rating')   # Ensure this matches your JSON key

#             if content and rating:
#                 place = get_object_or_404(Place, pk=place_id)
#                 comment = Comment.objects.create(
#                     place=place,
#                     user=request.user,
#                     content=content,
#                     rating=int(rating),
#                     created_at=timezone.now()
#                 )
#                 average_rating = Comment.objects.filter(place=place).aggregate(Avg('rating'))['rating__avg'] or 0
#                 average_rating = round(average_rating, 1)

#                 rendered_comment = render_to_string('places/comment_partial.html', {'comment': comment, 'user': request.user})
#                 return JsonResponse({
#                     'message': 'Your review has been submitted successfully.',
#                     'comment_html': rendered_comment,
#                     'average_rating': average_rating
#                 })

#             return JsonResponse({'error': 'Please provide both a comment and a rating.'}, status=400)

#         except json.JSONDecodeError as e:
#             print(f"JSONDecodeError: {e}")
#             return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
#TRIAL  4 START
#     return JsonResponse({'error': 'Invalid request.'}, status=400)
@csrf_exempt
def add_comment_ajax(request, place_id):
    print("Request method:", request.method)
    print("Request headers:", request.headers)
    print("Is user authenticated?", request.user.is_authenticated)
    print("Session key:", request.session.session_key)
    print("POST data:", request.POST)
    print("Cookies:", request.COOKIES)  # Add this to debug
    print("Session ID:", request.session.session_key)  # Add this to debug
    

    
    # Add CORS headers
    response = JsonResponse({'status': 'error', 'message': 'Authentication required'}, status=401)
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Origin"] = "http://localhost:57880"
    
    if not request.user.is_authenticated:
        session_id = request.COOKIES.get('sessionid')
        if session_id:
            from django.contrib.sessions.backends.db import SessionStore
            from django.contrib.auth.models import User
            session = SessionStore(session_key=session_id)
            if '_auth_user_id' in session:
                user_id = session.get('_auth_user_id')
                request.user = User.objects.get(pk=user_id)
    
    if not request.user.is_authenticated:
        return response

    try:
        place = get_object_or_404(Place, pk=place_id)
        comment_text = request.POST.get('comment')
        rating = request.POST.get('rating')

        comment = Comment.objects.create(
            place=place,
            user=request.user,
            content=comment_text,
            rating=int(rating),
            created_at=timezone.now()
        )

        success_response = JsonResponse({
            'status': 'success',
            'message': 'Comment added successfully',
            'data': {
                'id': comment.id,
                'content': comment.content,
                'rating': comment.rating,
                'username': comment.user.username,
            }
        })
        success_response["Access-Control-Allow-Credentials"] = "true"
        success_response["Access-Control-Allow-Origin"] = "http://localhost:57880"
        return success_response

    except Exception as e:
        error_response = JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
        error_response["Access-Control-Allow-Credentials"] = "true"
        error_response["Access-Control-Allow-Origin"] = "http://localhost:57880"
        return error_response

@csrf_exempt
def add_comment_ajax(request, place_id):
    print("Request method:", request.method)
    print("Request headers:", request.headers)
    print("Is user authenticated?", request.user.is_authenticated)
    print("Session key:", request.session.session_key)
    print("POST data:", request.POST)
    print("Cookies:", request.COOKIES)  # Add this to debug
    print("Session ID:", request.session.session_key)  # Add this to debug
    
    if not request.user.is_authenticated:
        # Try to get the session from the cookie
        session_id = request.COOKIES.get('sessionid')
        if session_id:
            from django.contrib.sessions.backends.db import SessionStore
            session = SessionStore(session_key=session_id)
            if session and '_auth_user_id' in session:
                from django.contrib.auth import get_user
                request.user = get_user(request)

    if not request.user.is_authenticated:
        print("User is not authenticated")
        return JsonResponse({
            'status': 'error',
            'message': 'Authentication required',
        }, status=401)


    if request.method == 'POST':
        try:
            place = get_object_or_404(Place, pk=place_id)
            
            # Get data from POST instead of JSON body
            comment_text = request.POST.get('comment')
            rating = request.POST.get('rating')

            if not comment_text or not rating:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Comment and rating are required'
                }, status=400)

            comment = Comment.objects.create(
                place=place,
                user=request.user,
                content=comment_text,
                rating=int(rating),
                created_at=timezone.now()
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Comment added successfully',
                'data': {
                    'id': comment.id,
                    'content': comment.content,
                    'rating': comment.rating,
                    'username': comment.user.username,
                }
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)
@login_required
@csrf_exempt
def edit_comment_ajax(request, comment_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        if content and rating:
            comment.content = content
            comment.rating = int(rating)
            comment.save()
            # Update average rating
            average_rating = Comment.objects.filter(place=comment.place).aggregate(Avg('rating'))['rating__avg'] or 0
            average_rating = round(average_rating, 1)
            # Return the rendered HTML for the updated comment and updated average rating
            rendered_comment = render_to_string('places/comment_partial.html', {'comment': comment, 'user': request.user})
            return JsonResponse({
                'message': 'Your review has been updated successfully.',
                'comment_html': rendered_comment,
                'comment_id': comment_id,
                'average_rating': average_rating
            })
        else:
            return JsonResponse({'error': 'Please provide both a comment and a rating.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)

@login_required
@csrf_exempt
def delete_comment_ajax(request, comment_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
        place = comment.place
        comment.delete()
        # Update average rating
        average_rating = Comment.objects.filter(place=place).aggregate(Avg('rating'))['rating__avg'] or 0
        average_rating = round(average_rating, 1)
        return JsonResponse({
            'message': 'Your review has been deleted.',
            'comment_id': comment_id,
            'average_rating': average_rating
        })
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)

# New view for adding a place to collections
@csrf_exempt
@login_required
def add_to_collection_ajax(request, place_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Correctly fetch the Place instance using place_id
        place = get_object_or_404(Place, pk=place_id)
        
        # Get list of collection IDs from POST data
        collection_ids = request.POST.getlist('collections')
        
        if collection_ids:
            for collection_id in collection_ids:
                # Fetch the Collection instance ensuring it belongs to the current user
                collection = get_object_or_404(Collection, pk=collection_id, user=request.user)
                
                # Check if the CollectionItem already exists
                existing_item = CollectionItem.objects.filter(collection=collection, place=place).first()
                
                if not existing_item:
                    # Create the CollectionItem if it doesn't exist
                    CollectionItem.objects.create(collection=collection, place=place)
            
            # Return a success response
            return JsonResponse({'success': True})
        else:
            # Return an error if no collections are selected
            return JsonResponse({'error': 'No collections selected.'}, status=400)
    else:
        # Return an error for invalid requests
        return JsonResponse({'error': 'Invalid request.'}, status=400)
# New view for buying a souvenir
@login_required
@csrf_exempt
def buy_souvenir_ajax(request, souvenir_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        souvenir = get_object_or_404(Souvenir, pk=souvenir_id)
        if souvenir.stock > 0:
            souvenir.stock -= 1
            souvenir.save()
            
            # Recalculate available and total souvenirs
            place = souvenir.place
            souvenirs = Souvenir.objects.filter(place=place)
            total_souvenirs_count = souvenirs.count()
            available_souvenirs_count = souvenirs.filter(stock__gt=0).count()
            
            return JsonResponse({
                'success': True,
                'new_stock': souvenir.stock,
                'available_souvenirs_count': available_souvenirs_count,
                'total_souvenirs_count': total_souvenirs_count
            })
        else:
            return JsonResponse({'error': 'Souvenir is out of stock.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)
    


# Add this to places/views.py

def place_detail_json(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    
    # Calculate the average rating
    average_rating = Comment.objects.filter(place=place).aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating, 1)

    # Get all comments for the place
    comments = Comment.objects.filter(place=place).order_by('-created_at')
    comments_data = []
    for c in comments:
        comments_data.append({
            'id': c.id,
            'username': c.user.username,
            'content': c.content,
            'rating': c.rating,
            'created_at': c.created_at.isoformat(),
        })

    # Include souvenirs data if needed (optional)
    souvenirs = Souvenir.objects.filter(place=place)
    souvenir_data = []
    for s in souvenirs:
        souvenir_data.append({
            'id': s.id,
            'name': s.name,
            'price': float(s.price),
            'stock': s.stock,
        })

    # Construct the JSON response
    data = {
        'id': place.id,
        'name': place.name,
        'description': place.description,
        'average_rating': average_rating,
        'comments': comments_data,
        'souvenirs': souvenir_data,
    }
    
    return JsonResponse(data, safe=False)
# TRIAL 4 END