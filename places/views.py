# places/views.py

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

@login_required
@csrf_exempt
def add_comment_ajax(request, place_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        place = get_object_or_404(Place, pk=place_id)
        content = request.POST.get('comment')
        rating = request.POST.get('rating')
        if content and rating:
            comment = Comment.objects.create(
                place=place,
                user=request.user,
                content=content,
                rating=int(rating),
                created_at=timezone.now()
            )
            # Update average rating
            average_rating = Comment.objects.filter(place=place).aggregate(Avg('rating'))['rating__avg'] or 0
            average_rating = round(average_rating, 1)
            # Return the rendered HTML for the new comment and updated average rating
            rendered_comment = render_to_string('places/comment_partial.html', {'comment': comment, 'user': request.user})
            return JsonResponse({
                'message': 'Your review has been submitted successfully.',
                'comment_html': rendered_comment,
                'average_rating': average_rating
            })
        else:
            return JsonResponse({'error': 'Please provide both a comment and a rating.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)

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

