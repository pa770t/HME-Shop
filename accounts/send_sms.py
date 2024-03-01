import vonage
import string, random
from .models import OTP
from django.conf import settings

def generate_totp_and_send_sms(user, phone_number):

    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(6))

    # save to database
    OTP.objects.create(user=user, otp=otp)

    # Send TOTP code via sms
    client = vonage.Client(key="44a8ce83", secret=settings.SECRET_KEY)
    sms = vonage.Sms(client)

    responseData = sms.send_message(
        {
            "from": "HME Shop",
            "to": phone_number,
            "text": f"Your OTP CODE: {otp}",
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
