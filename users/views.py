from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, TemplateView, DetailView
from django.utils import timezone

from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User, Company, Customer


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
        return redirect('customer-profile') 


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
        return redirect('company-profile') 


def LoginUserView(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # Authenticate the user
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)  # Log the user in
                # Redirect based on user type
                if user.is_customer:
                    return redirect('customer-profile')  # Redirect to customer profile
                elif user.is_company:
                    return redirect('company-profile')  # Redirect to company profile
                else:
                    return redirect('/')  # Fallback to homepage
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})

# Customer Profile View - Only accessible to logged-in users
@login_required
def CustomerProfileView(request):
    customer = Customer.objects.get(user=request.user)
    user_age = timezone.now().year - customer.birth.year

    return render(request, 'users/profile.html', {
        'user': request.user,
        'user_age': user_age,
        'sh': []  # Placeholder for requested services history
    })


# Company Profile View - Only accessible to logged-in users
@login_required
def CompanyProfileView(request):
    company = Company.objects.get(user=request.user)

    return render(request, 'users/profile.html', {
        'user': request.user,
        'services': []  # Placeholder for services provided by the company
    })