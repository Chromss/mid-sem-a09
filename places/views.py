from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Place, Souvenir, Comment
from django.db.models import Avg
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.utils import timezone

def place_detail(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    average_rating = Comment.objects.filter(place=place).aggregate(Avg('rating'))['rating__avg'] or 0
    souvenirs = Souvenir.objects.filter(place=place)
    comments = Comment.objects.filter(place=place).order_by('-created_at')[:10]  # Limit to recent 10 reviews

    # Check if there's review data stored in session
    review_data = request.session.pop('review_data', None)

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_content = request.POST.get('comment')
            rating_value = request.POST.get('rating')

            if comment_content and rating_value:
                # Save the comment with rating
                Comment.objects.create(
                    place=place,
                    user=request.user,
                    content=comment_content,
                    rating=int(rating_value),
                    created_at=timezone.now()
                )
                messages.success(request, "Your review has been submitted successfully.")
                return redirect('place_detail', place_id=place.id)
            else:
                messages.error(request, "Please provide both a comment and a rating.")
        else:
            # Store the submitted review data in session
            comment_content = request.POST.get('comment')
            rating_value = request.POST.get('rating')
            request.session['review_data'] = {
                'comment': comment_content,
                'rating': rating_value,
                'place_id': place.id
            }
            messages.error(request, "You must be logged in to submit a review.")
            return redirect(f"{reverse('login')}?next={request.path}")

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
