# places/views.py

from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Avg
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

# Import your models here
from .models import Place, Souvenir, Comment

# Import the Collection models
from placeCollection.models import Collection, CollectionItem  # Added import

def format_price(price):
    """Formats the price with commas (e.g., 10000 -> 10,000)."""
    return "{:,}".format(price)

def place_detail(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    average_rating = Comment.objects.filter(place=place).aggregate(Avg('rating'))['rating__avg'] or 0
    souvenirs = Souvenir.objects.filter(place=place)

    # Format the price for each souvenir
    for souvenir in souvenirs:
        souvenir.formatted_price = format_price(souvenir.price)

    comments = Comment.objects.filter(place=place).order_by('-created_at')[:10]  # Limit to recent 10 reviews

    # Get the user's collections if authenticated
    user_collections = Collection.objects.filter(user=request.user) if request.user.is_authenticated else []

    context = {
        'place': place,
        'average_rating': round(average_rating, 1),
        'souvenirs': souvenirs,
        'comments': comments,
        'user_collections': user_collections,  # Added to context
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
            # Format the new comment's price if needed (assuming comments don't have prices)
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
        place = get_object_or_404(Place, pk=place_id)
        collection_ids = request.POST.getlist('collections')
        if collection_ids:
            for collection_id in collection_ids:
                collection = get_object_or_404(Collection, pk=collection_id, user=request.user)
                # Check if the place is already in the collection
                existing_item = CollectionItem.objects.filter(collection=collection, place=place).first()
                if not existing_item:
                    CollectionItem.objects.create(collection=collection, place=place)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'No collections selected.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)
