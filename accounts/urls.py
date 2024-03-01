from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    # account urls
    path('account/register/', views.register, name='register'),
    path('account/confirm/email/', views.confirm_email, name='confirm_email'),
    path('account/activate/<str:token>/', views.activate_account, name='activate_account'),
    path('account/login/', views.signin, name='login'),
    path('account/logout/', views.logout_request, name='logout'),
    path('account/password/change/', views.change_password, name='change_password'),
    path('account/setting/', views.account_setting, name='account_setting'),
    path('account/delete/', views.delete_user, name='delete_user'),
    path('account/verify/otp/', views.confirm_otp, name='confirm_otp'),
]
