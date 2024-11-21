from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.http import JsonResponse
from allauth.socialaccount.models import SocialAccount
from django.views.decorators.csrf import csrf_exempt
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings

def social_login_callback(request):
    if request.user.is_authenticated:
        # Retrieve social account details
        try:
            social_account = SocialAccount.objects.get(user=request.user, provider='google')
            return JsonResponse({
                'email': request.user.email,
                'name': request.user.first_name,
                'social_id': social_account.uid,
            })
        except SocialAccount.DoesNotExist:
            return JsonResponse({'error': 'No social account found'}, status=400)
    return JsonResponse({'error': 'Not authenticated'}, status=401)



# # Create your views here.
# def home(request):
#     return render(request,"home.html")

def logout_view(request):
    logout(request)
    return redirect("/login")


@csrf_exempt
def api_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({
            'status': 'success', 
            'message': 'Logged out successfully'
        })
    return JsonResponse({
        'status': 'error', 
        'message': 'No user logged in'
    }, status=400)

class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = settings.GITHUB_REDIRECT_URI
    client_class = OAuth2Client