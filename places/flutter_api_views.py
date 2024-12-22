from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Avg
from .models import Place, Comment, Souvenir

@csrf_exempt
def add_comment_flutter(request, place_id):
    """API endpoint for adding comments from Flutter app"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'Authentication required'
        }, status=401)

    if request.method == 'POST':
        try:
            place = get_object_or_404(Place, pk=place_id)
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

            # Recalculate average rating
            avg_rating = Comment.objects.filter(place=place).aggregate(Avg('rating'))['rating__avg'] or 0
            
            return JsonResponse({
                'status': 'success',
                'message': 'Comment added successfully',
                'data': {
                    'id': comment.id,
                    'content': comment.content,
                    'rating': comment.rating,
                    'username': comment.user.username,
                    'average_rating': round(avg_rating, 1)
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

@csrf_exempt
@csrf_exempt
def edit_comment_flutter(request, comment_id):
    print("Debug - Initial User auth status:", request.user.is_authenticated)
    print("Debug - Initial Session:", request.session.session_key)
    print("Debug - Request POST:", request.POST)
    print("Debug - Request COOKIES:", request.COOKIES)

    # Try to get session ID from either cookies or POST data
    session_id = request.COOKIES.get('sessionid') or request.POST.get('sessionid')
    print("Debug - Session ID found:", session_id)

    if not request.user.is_authenticated and session_id:
        try:
            session = SessionStore(session_key=session_id)
            if '_auth_user_id' in session:
                user_id = session.get('_auth_user_id')
                request.user = User.objects.get(pk=user_id)
                print("Debug - User authenticated:", request.user.username)
        except Exception as e:
            print("Debug - Session authentication failed:", str(e))

    print("Debug - Final User auth status:", request.user.is_authenticated)

    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'Authentication required'
        }, status=401)

    if request.method == 'POST':
        try:
            comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
            content = request.POST.get('content')
            rating = request.POST.get('rating')

            if not content or not rating:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Content and rating are required'
                }, status=400)

            comment.content = content
            comment.rating = int(rating)
            comment.save()

            # Recalculate average rating
            avg_rating = Comment.objects.filter(place=comment.place).aggregate(Avg('rating'))['rating__avg'] or 0

            return JsonResponse({
                'status': 'success',
                'message': 'Comment updated successfully',
                'data': {
                    'id': comment.id,
                    'content': comment.content,
                    'rating': comment.rating,
                    'username': comment.user.username,
                    'average_rating': round(avg_rating, 1)
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

@csrf_exempt
def delete_comment_flutter(request, comment_id):
    """API endpoint for deleting comments from Flutter app"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'Authentication required'
        }, status=401)

    if request.method == 'POST':
        try:
            comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
            place = comment.place
            comment.delete()

            # Recalculate average rating
            avg_rating = Comment.objects.filter(place=place).aggregate(Avg('rating'))['rating__avg'] or 0

            return JsonResponse({
                'status': 'success',
                'message': 'Comment deleted successfully',
                'data': {
                    'average_rating': round(avg_rating, 1)
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

@csrf_exempt
def buy_souvenir_flutter(request, souvenir_id):
    """API endpoint for purchasing souvenirs from Flutter app"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'Authentication required'
        }, status=401)

    if request.method == 'POST':
        try:
            souvenir = get_object_or_404(Souvenir, pk=souvenir_id)
            
            if souvenir.stock <= 0:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Souvenir is out of stock'
                }, status=400)

            souvenir.stock -= 1
            souvenir.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Souvenir purchased successfully',
                'data': {
                    'id': souvenir.id,
                    'name': souvenir.name,
                    'new_stock': souvenir.stock
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