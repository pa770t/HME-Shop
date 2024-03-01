from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from .models import ConfirmationToken
from django.shortcuts import redirect
from .models import User

def send_confirmation_email(request, email):
    user = User.objects.get(email=email)
    # send confirm email
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    confirmation_key = f"{uid}-{token}"

    confirmation_url = f"{request.scheme}://{request.get_host()}/account/activate/{confirmation_key}/"

    ConfirmationToken.objects.create(user=user, token=confirmation_key)

    subject = 'HME Shop - Confirm Your Email'
    message = f'Thank you for signing up. Please click the link below to confirm your email.\n{confirmation_url}'
    from_email = 'yarzarmin476@gmail.com'

    send_mail(subject, message, from_email, [user.email], fail_silently=False)
