from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, TemplateView, DetailView
from django.utils import timezone

from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User, Company, Customer
from services.models import ServiceRequest


def register(request):
    return render(request, 'users/register.html')


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'users/register_customer.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user) #login user automatically
        return redirect('users:customer-profile') 


class CompanySignUpView(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = 'users/register_company.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('users:company-profile') 


def LoginUserView(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # Authenticate the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  # Log the user in
                # Redirect based on user type
                if user.is_customer:
                    return redirect('users:customer-profile', username=user.username)  # Redirect to customer profile
                elif user.is_company:
                    return redirect('users:company-profile', username=user.username)  # Redirect to company profile
                else:
                    return redirect('home')  # Fallback to homepage
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})

# Customer Profile View - Only accessible to logged-in users
@login_required
def CustomerProfileView(request, username):
    customer = Customer.objects.get(user=request.user)
    user_age = timezone.now().year - customer.birth.year
    requested_services = ServiceRequest.objects.filter(customer=customer).order_by('-request_date')

    return render(request, 'users/profile.html', {
        'user': request.user,
        'user_age': user_age,
        'sh': requested_services  # Placeholder for requested services history
    })


# Company Profile View - Only accessible to logged-in users
@login_required
def CompanyProfileView(request, username):
    company = Company.objects.get(user=request.user)

    return render(request, 'users/profile.html', {
        'user': request.user,
        'services': []  # Placeholder for services provided by the company
    })