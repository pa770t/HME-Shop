# allauth
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.models import SocialApp
from django.shortcuts import redirect
from django.urls import reverse

def custom_google_login(request):
    adapter = get_adapter(request)
    login_url = reverse('socialaccount_login')
    app = SocialApp.objects.get(provider='google')
    callback_url = request.build_absolute_uri(f'{login_url}google/')
    authorize_url = adapter.get_authorize_url(request, GoogleOAuth2Adapter, callback_url)

    return redirect(authorize_url)