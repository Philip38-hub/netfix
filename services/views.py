from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from users.models import Company, Customer, User

from .models import Service, ServiceRequest
from .forms import CreateNewService, RequestServiceForm


def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


# def create(request):
#     return render(request, 'services/create.html', {})

def create(request):
    # You can add choices for your field here if needed
    service_choices = [
        ('Air Conditioner', 'Air Conditioner'),
        ('Carpentry', 'Carpentry'),
        ('Electricity', 'Electricity'),
        ('Gardening', 'Gardening'),
        ('Home Machines', 'Home Machines'),
        ('House Keeping', 'House Keeping'),
        ('Interior Design', 'Interior Design'),
        ('Locks', 'Locks'),
        ('Painting', 'Painting'),
        ('Plumbing', 'Plumbing'),
        ('Water Heaters', 'Water Heaters')
    ]
    
    if request.method == 'POST':
        form = CreateNewService(request.POST, choices=service_choices)
        if form.is_valid():
            # Manually save form data to the Service model
            service = Service.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price_hour=form.cleaned_data['price_hour'],
                field=form.cleaned_data['field'],
                company=Company.objects.get(user=request.user)  # Assuming the logged-in user is linked to a company
            )
            service.save()
            return redirect('services_list')  # Redirect after saving the service
    else:
        form = CreateNewService(choices=service_choices)

    return render(request, 'services/create.html', {'form': form})

def service_field(request, field):
    # search for the service present in the url
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(
        field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


def request_service(request, id):
    service = Service.objects.get(id=id)
    customer = Customer.objects.get(user=request.user)  # Assuming the user is logged in as a customer
    
    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            service_hours = form.cleaned_data['service_hours']
            address = form.cleaned_data['address']
            total_price = service.price_hour * service_hours  # Calculate total price

            # Save the service request
            ServiceRequest.objects.create(
                customer=customer,
                service=service,
                service_hours=service_hours,
                address=address,
                total_price=total_price
            )
            return redirect('users:customer-profile', username=request.user.username)
    else:
        form = RequestServiceForm()

    return render(request, 'services/request_service.html', {'form': form, 'service': service})