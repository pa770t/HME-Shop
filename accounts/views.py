from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegisterForm, ProfileSettingForm, CustomLoginForm, PasswordChangeForm, OTPForm
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash, authenticate
from django.contrib.auth.decorators import login_required
from .models import OTP, User as CustomUser

# custom
from .decorators import only_for_simple_auth
from .send_sms import generate_totp_and_send_sms

# email
from .models import ConfirmationToken, Membership
from .utils import send_confirmation_email

# Create your views here.

# https://www.google.com/search?q=show+allauth+link+direct+to+template&oq=show+allauth+link+direct+to+template&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORigAdIBCTEwNDE5ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8#fpstate=ive&vld=cid:b790088f,vid:dXZim_jgaiI,st:0

User = get_user_model()

def activate_account(request, token):
    try:
        confirmation_token = get_object_or_404(ConfirmationToken, token=token)
        
        user = CustomUser.objects.get(email=confirmation_token.user.email)
        user.is_active = True
        user.save()

        confirmation_token.delete()
        messages.success(request, 'Account activated. Please log in!')
        return redirect('login')
    except:
        messages.error(request, 'Invalid Confirmation Token! Please try again!')
        return redirect('login')

def confirm_email(request):
    return render(request, 'accounts/wait_confirm.html')

def confirm_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            try:
                otp = form.cleaned_data['otp']
                otp = get_object_or_404(OTP, otp=otp)
                otp.user.is_active = True

                otp.user.save()

                otp.delete()

                return redirect('login')
            except:
                messages.error(request, 'Your OTP Code is invalid!')
                return redirect('confirm_otp')
    else:
        form = OTPForm()
        return render(request, 'accounts/verify_otp.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():

            user = form.save()
            user.is_active = False
            user.save()

            # fill
            if user.email:
                send_confirmation_email(request, user.email)
                messages.success(request, 'Your account is registered! Please click the link in your email to activate your account!')
                return redirect('register')
            else:
                generate_totp_and_send_sms(user=user,phone_number=user.phone_number)
                return redirect('confirm_otp')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {
        'form': form
    })

def signin(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid email, phone, or password!')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required(login_url='login')
def logout_request(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def account_setting(request):
    if request.method == 'POST':
        form = ProfileSettingForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated successfully.")
            return redirect('account_setting')
    else:
        form = ProfileSettingForm(instance=request.user)
        is_simple_auth = not request.user.socialaccount_set.exists()

    membership = Membership.objects.get(user=request.user)

    return render(request, 'accounts/account_setting.html', {'form': form, 'user': request.user, 'is_simple_auth': is_simple_auth, 'membership_level': membership.level})

@only_for_simple_auth
@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return redirect('account_setting')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/password_change_form.html', {'form': form})

@login_required(login_url='login')
def delete_user(request):
    request.user.delete()
    return redirect('login')

def custom_404_page(request, exception):
    return render(request, 'accounts/404.html')
