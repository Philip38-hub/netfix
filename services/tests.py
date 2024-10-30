from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Company
from .models import Service
from .forms import CreateNewService, RequestServiceForm
from django.urls import reverse

User = get_user_model()

class ServiceModelTest(TestCase):
    def setUp(self):
        # Set up user and company
        self.user = User.objects.create_user(username="testcompany", password="password123")
        self.company = Company.objects.create(user=self.user)
        
        # Set up service instance
        self.service = Service.objects.create(
            company=self.company,
            name="Gardening Service",
            description="Professional gardening service",
            price_hour=50.00,
            field="Gardening"
        )

    def test_service_creation(self):
        """Test that the service is created correctly"""
        self.assertEqual(self.service.name, "Gardening Service")
        self.assertEqual(self.service.price_hour, 50.00)
        self.assertEqual(self.service.field, "Gardening")

    def test_service_string_representation(self):
        """Test the string representation of the service"""
        self.assertEqual(str(self.service), "Gardening Service")

class ServiceFormTest(TestCase):
    def test_create_service_form_invalid_data(self):
        """Test that the CreateNewService form rejects invalid data"""
        form = CreateNewService(data={
            "name": "",  # Empty name should trigger an error
            "description": "Interior and exterior painting",
            "price_hour": -10.00,  # Negative price should trigger an error
            "field": "Painting"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("price_hour", form.errors)

class ServiceViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testcompany", password="password123")
        self.company = Company.objects.create(user=self.user)
        self.client.login(username="testcompany", password="password123")

    def test_create_service_view(self):
        """Test service creation view"""
        response = self.client.post(reverse('services_create'), data={
            "name": "New Service",
            "description": "Service description",
            "price_hour": 15.00,
            "field": "Gardening"
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after creation
        self.assertTrue(Service.objects.filter(name="New Service").exists())
