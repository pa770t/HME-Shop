from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('contact/', views.contact, name='contact'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('news/<slug:slug>/', views.single_news, name='single_news'),
    path('news/', views.news, name='news'),
    path('products/<slug:slug>/', views.single_product, name='single_product'),
    path('orders/', views.orders, name='orders'),

    # cart functions
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<uuid:product_id>', views.add_to_cart, name='add_to_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
]
