from django.shortcuts import redirect
from .forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from functools import wraps


def only_for_simple_auth(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.socialaccount_set.exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('account_setting')
    return wrapper
