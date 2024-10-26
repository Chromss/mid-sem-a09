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

def place_detail(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    average_rating = Comment.objects.filter(place=place).aggregate(Avg('rating'))['rating__avg'] or 0
    souvenirs = Souvenir.objects.filter(place=place)
    comments = Comment.objects.filter(place=place).order_by('-created_at')[:10]  # Limit to recent 10 reviews

    # Check if there's review data stored in session
    review_data = request.session.pop('review_data', None)

    context = {
        'place': place,
        'average_rating': round(average_rating, 1),
        'souvenirs': souvenirs,
        'comments': comments,
        'review_data': review_data,  # Pass any existing review data to the template
    }
    return render(request, 'places/place_detail.html', context)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Path to your custom login template
    redirect_authenticated_user = True  # Redirect users who are already logged in

    def get_success_url(self):
        """
        Override this method to redirect users after successful login.
        If a 'next' parameter exists, redirect there; otherwise, use a default URL.
        """
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
            # Check if the user already has a comment on this place
            existing_comment = Comment.objects.filter(place=place, user=request.user).first()
            if existing_comment:
                return JsonResponse({'error': 'You have already reviewed this place.'}, status=400)
            else:
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
