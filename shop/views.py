from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError

from .models import News, Order, OrderItem, Product, Cart, CartItem, ShippingAddress, SubCategory, Category, PromoCode
from accounts.models import Membership

from .forms import ShippingAddressForm, PaymentForm, ContactInfoForm, PromoCodeForm
from .utils import create_order, apply_promo_code

from django_ratelimit.decorators import ratelimit

# stripe
# stripe.api_key = settings.STRIPE_SECRET_KEY

@ratelimit(key='user_or_ip', rate='20/m', block=True)
@login_required(login_url='login')
def home(request):
    new_products = Product.objects.all()[:3]
    categories = Category.objects.all()
    news = News.objects.all()[:3]
    return render(request, 'shop/home.html', {'new_products': new_products, 'categories': categories, 'news': news})

@ratelimit(key='user_or_ip', rate='20/m', block=True)
@login_required(login_url='login')
def shop(request):
    products = Product.objects.all()
    
    if request.GET.get('sortby'):
        sort_by = request.GET.get('sortby')
        if sort_by == 'lowest_to_highest':
            products = Product.objects.order_by('price')
        elif sort_by == 'highest_to_lowest':
            products = Product.objects.order_by('-price')
        elif sort_by == 'newest_to_oldest':
            products = Product.objects.order_by('-created_at')
        elif sort_by == 'oldest_to_newest':
            products = Product.objects.order_by('created_at')

    if request.GET.get('show'):
        show = request.GET.get('show')
        products = Product.objects.order_by('-created_at')[:int(show)]

    if request.GET.get('category'):
        category = request.GET.get('category')
        products = Product.objects.filter(category__name__icontains=category)

    if request.GET.get('sub_category'):
        sub_category = request.GET.get('sub_category')
        products = Product.objects.filter(subcategory__name__icontains=sub_category)

    if request.GET.get('s'):
        s = request.GET.get('s')
        products = Product.objects.filter(name__icontains=s)

    if request.GET.get('collection'):
        collection = request.GET.get('collection')
        products = Product.objects.filter(name__icontains=collection)

    sub_categories = SubCategory.objects.all()


    # pagination starts
    paginator = Paginator(products, 9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    pagination_numbers = []
    for i in range(1, paginator.num_pages + 1):
        pagination_numbers.append(i)

    return render(request, 'shop/shop.html', {'products': products, 'sub_categories': sub_categories, 'page_obj': page_obj, 'paginator': paginator, 'pagination_numbers': pagination_numbers})

@ratelimit(key='user_or_ip', rate='20/m', block=True)
@login_required(login_url='login')
def about(request):
    return render(request, 'shop/about.html')

@ratelimit(key='user_or_ip', rate='20/m', block=True)
@login_required(login_url='login')
def service(request):
    return render(request, 'shop/service.html')

@ratelimit(key='user_or_ip', rate='20/m', block=True)
@login_required(login_url='login')
def contact(request):
    if request.method == 'POST':
        form = ContactInfoForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.info(request, 'Thanks for contacting us!')
            return redirect('contact')
        else:
            return render(request, 'shop/contact.html', {'form': form})
    else:
        form = ContactInfoForm()
        return render(request, 'shop/contact.html', {'form': form})

@ratelimit(key='user_or_ip', rate='20/m', block=True)
@login_required(login_url='login')
def single_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    quantity = request.POST.get('quantity')
    if request.method == 'POST':
        user_cart, created = Cart.objects.get_or_create(user=request.user)

        existing_item = CartItem.objects.filter(cart=user_cart, product=product).first()

        if existing_item:
            existing_item.quantity += int(quantity)
            existing_item.save()
            return redirect('cart')
        else:
            CartItem.objects.create(cart=user_cart, product=product, quantity=int(quantity), price=product.price)
            return redirect('cart')
    return render(request, 'shop/single_product.html', {'product': product})

@ratelimit(key='user_or_ip', rate='20/m', block=True)
@login_required(login_url='login')
def news(request):
    news = News.objects.all()

    paginator = Paginator(news, 9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    pagination_numbers = []
    for i in range(1, paginator.count + 1):
        pagination_numbers.append(i)
    
    sub_categories = SubCategory.objects.all()
    return render(request, 'shop/news.html', {'news': news, 'sub_categories': sub_categories, 'page_obj': page_obj, 'paginator': paginator, 'pagination_numbers': pagination_numbers})

@ratelimit(key='user_or_ip', rate='20/m', block=True)
@login_required(login_url='login')
def single_news(request, slug):
    news = News.objects.get(slug=slug)
    return render(request, 'shop/single_news.html', {'news': news})


# checkout functions

@ratelimit(key='user_or_ip', rate='20/m', block=True)
@login_required(login_url='login')
def checkout(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            user_cart = Cart.objects.get(user=request.user)

            cart_items = user_cart.cartitem_set.all()
            total_price = sum(item.quantity * item.price for item in cart_items)

            request.session['shipping_address'] = form.cleaned_data

            return redirect('payment')
        else:
            return render(request, 'shop/checkout.html', {'form': form})
    else:
        form = ShippingAddressForm()
        try:
            Cart.objects.get(user=request.user)

            sub_total_price, discount_price, total_price = apply_promo_code(request)
            return render(request, 'shop/checkout.html', {'form': form, 'sub_total_price': sub_total_price, 'total_price': total_price, 'discount_price': discount_price})
        except:
            messages.info(request, 'Your cart is empty! Please add products to your cart!')
            return redirect('cart')

@ratelimit(key='user_or_ip', rate='20/m', block=True)
@login_required(login_url='login')
def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)

        if form.is_valid():
            try:
                user_cart = Cart.objects.get(user=request.user)

                cart_items = user_cart.cartitem_set.all()

                shipping_address_data = request.session['shipping_address']
                shipping_address = ShippingAddress.objects.create(**shipping_address_data, user=request.user)

                del request.session['shipping_address']

                sub_total_price, discount_price, total_price = apply_promo_code(request)

                payment = form.save(commit=False)
                payment.user = request.user
                payment.paid = True
                payment.amount = total_price
                form.save()

                # create order
                order = create_order(request, total_price, shipping_address)

                # create order item
                for item in cart_items:
                    OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, unit_price=item.price)

                user_cart.delete()

                # set user membership level
                membership = Membership.objects.get(user=request.user)
                orders = Order.objects.filter(user=request.user, status='Paid')
                total_payment = sum(each_order.total_amount for each_order in orders)

                if total_payment >= 1000 and total_payment < 10000:
                    membership.level = 'Silver'
                    membership.save()
                elif total_payment >= 10000 and total_payment < 100000:
                    membership.level = 'Gold'
                    membership.save()
                elif total_payment >= 100000 and total_payment < 1000000:
                    membership.level = 'Platinum'
                    membership.save()
                elif total_payment >= 1000000 and total_payment < 10000000:
                    membership.level = 'Diamond'
                    membership.save()

                messages.success(request, 'Your order is on pending! Happy Shopping!')
                return redirect('shop')
            
            except :
                messages.error(request, "Payment didn't success! Please try again!")
                return redirect('payment')
        else:
            return render(request, 'shop/payment.html', {'form': form})
    else:
        form = PaymentForm()
        try:
            Cart.objects.get(user=request.user)
        except:
            messages.info(request, 'Your cart is empty! Please add products to your cart!')
            return redirect('cart')
        try:
            sub_total_price, discount_price, total_price = apply_promo_code(request)
            
            return render(request, 'shop/payment.html', {'form': form, 'sub_total_price': sub_total_price, 'total_price': total_price, 'discount_price': discount_price})
        except:
            sub_total_price, discount_price, total_price = apply_promo_code(request)
            return render(request, 'shop/payment.html', {'form': form, 'total_price': total_price})

@ratelimit(key='user_or_ip', rate='20/m', block=True)
@login_required(login_url='login')
def order(request):
    return render(request, 'shop/order.html')


# cart functions

@ratelimit(key='user_or_ip', rate='20/m', block=True)
@login_required(login_url='login')
def cart(request):
    if request.method == 'POST':
        try:
            Cart.objects.get(user=request.user)
        except:
            messages.info(request, 'Your cart is empty! Please add products to your cart!')
            return redirect('cart')
        try:
            code_obj = PromoCode.objects.get(code=request.POST['code'])

            request.session['code'] = request.POST['code']
            code_obj.apply_by.add(request.user)
            
            return redirect('cart')
        except:
            messages.info(request, 'Your Promo Code is Invalid!')
        return redirect('cart')
        
    else:
        form = PromoCodeForm()
        try:
            user_cart = Cart.objects.get(user=request.user)

            cart_items = user_cart.cartitem_set.all()

            sub_total_price, discount_price, total_price = apply_promo_code(request)
            
            return render(request, 'shop/cart.html', {'cart': cart_items, 'form': form, 'sub_total_price': sub_total_price, 'total_price': total_price, 'discount_price': discount_price})
        except:
            sub_total_price, discount_price, total_price = apply_promo_code(request)
            return render(request, 'shop/cart.html', {'form': form, 'sub_total_price': sub_total_price, 'total_price': total_price, 'discount_price': discount_price})

@ratelimit(key='user_or_ip', rate='20/m', block=True)
@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    user_cart, created = Cart.objects.get_or_create(user=request.user)

    existing_item = CartItem.objects.filter(cart=user_cart, product=product).first()

    if existing_item:
        existing_item.quantity += 1
        existing_item.save()
    else:
        CartItem.objects.create(cart=user_cart, product=product, quantity=1, price=product.price)

    return redirect('cart')

@ratelimit(key='user_or_ip', rate='20/m', block=True)
@login_required(login_url='login')
def clear_cart(request):
    Cart.objects.get(user=request.user).delete()
    try:
        del request.session['shipping_address']
    except:
        pass
    return redirect('cart')

@ratelimit(key='user_or_ip', rate='20/m', block=True)
@login_required(login_url='login')
def orders(request):
    # orders = Order.objects.filter(user=request.user, status='Paid')
    # total_payment = sum(each_order.total_amount for each_order in orders)
    orders = Order.objects.filter(user=request.user)
    if request.GET.get('status'):
        status = request.GET.get('status')
        orders = Order.objects.filter(user=request.user, status=status)
    return render(request, 'shop/order.html', {'orders': orders})

def get_cartitem_count(user):
    cartitem_count = 0
    try:
        cart = Cart.objects.get(user=user)
        cartitem_count = CartItem.objects.filter(cart=cart).count()
    except:
        pass

    return cartitem_count

def rate_limit_exceeded(request, exception):
    return render(request, 'shop/403.html')

def custom_404_page(request, exception):
    return render(request, 'shop/404.html')
