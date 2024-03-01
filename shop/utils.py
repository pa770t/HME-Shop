from django.shortcuts import redirect
from .models import Cart, Order, PromoCode
from django.contrib import messages
from django.utils import timezone


def create_order(request, total_amount, shipping_address):
    order = Order.objects.create(user=request.user, total_amount=total_amount, shipping_address=shipping_address)
    return order
    
def apply_promo_code(request):
    if request.user.promocode_set.exists():
        try:
            # print(request.user.promocode_set)
            code_obj = PromoCode.objects.get(code=request.session['code'])
            if code_obj.time_until > timezone.now():
                user_cart = Cart.objects.get(user=request.user)

                cart_items = user_cart.cartitem_set.all()

                sub_total_price = sum(item.quantity * item.price for item in cart_items)
                total_price = sum(item.quantity * item.price for item in cart_items) - code_obj.discount_price
                
                return [sub_total_price, code_obj.discount_price, total_price]
            else:
                messages.info(request, 'Your Promo Code in Invalid!')
                return [sub_total_price, 0, sub_total_price]
        except:
            return [0, 0, 0]
    else:
        try:
            user_cart = Cart.objects.get(user=request.user)

            cart_items = user_cart.cartitem_set.all()

            total_price = sum(item.quantity * item.price for item in cart_items)
            return [total_price, 0, total_price]
        except:
            return [0, 0, 0]
