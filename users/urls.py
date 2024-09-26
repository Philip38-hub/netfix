from django.urls import path
from django.contrib.auth import views

from .forms import UserLoginForm
from . import views as v

app_name = 'users'

urlpatterns = [
    path('', v.register, name='register'),
    path('company/', v.CompanySignUpView.as_view(), name='register_company'),
    path('customer/', v.CustomerSignUpView.as_view(), name='register_customer'),
    path('login/', v.LoginUserView, name='login'),
    path('profile/company/', v.CompanyProfileView, name='company-profile'), 
    path('profile/customer/', v.CustomerProfileView, name='customer-profile')
]
