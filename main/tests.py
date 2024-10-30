from django.test import TestCase, Client
from django.urls import reverse
from users.models import User, Company, Customer
from services.models import Service, ServiceRequest

class MainAppTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('main:home')
        
        # Create a customer and a company user for testing
        self.customer_user = User.objects.create_user(
            username="customer_test", password="testpass123", is_customer=True, email="customer@example.com"
        )
        self.company_user = User.objects.create_user(
            username="company_test", password="testpass123", is_company=True, email="company@example.com"
        )
        self.customer = Customer.objects.create(user=self.customer_user, birth="1990-01-01")
        self.company = Company.objects.create(user=self.company_user, field="Gardening")

        # Create a few services
        self.service1 = Service.objects.create(
            company=self.company, name="Gardening Service", description="Lawn care and maintenance",
            price_hour=20.00, field="Gardening"
        )
        self.service2 = Service.objects.create(
            company=self.company, name="Tree Trimming", description="Tree care and trimming",
            price_hour=30.00, field="Gardening"
        )

        # Create service requests
        self.service_request1 = ServiceRequest.objects.create(
            service=self.service1, customer=self.customer, service_hours=2, total_price=40.00
        )
        self.service_request2 = ServiceRequest.objects.create(
            service=self.service2, customer=self.customer, service_hours=3, total_price=90.00
        )

    def test_homepage_access(self):
        """Test that the homepage loads successfully with status 200"""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')
        
    def test_homepage_content_for_unauthenticated_user(self):
        """Check content available to unauthenticated users on homepage"""
        response = self.client.get(self.home_url)
        self.assertContains(response, "Login")
        self.assertContains(response, "Register")
        
    def test_homepage_content_for_authenticated_customer(self):
        """Check content available to authenticated customer on homepage"""
        self.client.login(username="customer_test", password="testpass123")
        response = self.client.get(self.home_url)
        self.assertContains(response, "Logout")
        self.assertContains(response, "customer_test")

    def test_top_services_display(self):
        """Test that the top requested services are displayed on the homepage"""
        response = self.client.get(self.home_url)
        self.assertContains(response, self.service1.name)
        self.assertContains(response, self.service2.name)

    def test_navigation_links(self):
        """Ensure primary navigation links are present"""
        response = self.client.get(self.home_url)
        self.assertContains(response, reverse('main:home'))
        self.assertContains(response, reverse('services_list'))
