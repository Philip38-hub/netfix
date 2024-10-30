from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Company, Customer
from django.contrib.auth.models import User

User = get_user_model()

class UserTests(TestCase):
    
    def setUp(self):
        # Create customer user
        self.customer_user = User.objects.create_user(
            username="customer1", password="testpass123", email="customer1@example.com", is_customer=True
        )
        Customer.objects.create(user=self.customer_user, birth="1990-01-01")

        # Create company user
        self.company_user = User.objects.create_user(
            username="company1", password="testpass123", email="company1@example.com", is_company=True
        )
        Company.objects.create(user=self.company_user, field="Gardening")

    def test_company_registration(self):
        response = self.client.post(reverse("users:register_company"), {
            "username": "newcompany",
            "password1": "companypass123",
            "password2": "companypass123",
            "email": "newcompany@example.com",
            "field": "Gardening"
        })
        self.assertEqual(response.status_code, 302)  # Successful registration should redirect
        self.assertTrue(User.objects.filter(username="newcompany").exists())

    def test_customer_login(self):
        login = self.client.login(username="customer1", password="testpass123")
        self.assertTrue(login)
        response = self.client.get(reverse("users:customer-profile", kwargs={"username": "customer1"}))
        self.assertEqual(response.status_code, 200)

    def test_company_login(self):
        login = self.client.login(username="company1", password="testpass123")
        self.assertTrue(login)
        response = self.client.get(reverse("users:company-profile", kwargs={"username": "company1"}))
        self.assertEqual(response.status_code, 200)

    def test_customer_profile_access(self):
        self.client.login(username="customer1", password="testpass123")
        response = self.client.get(reverse("users:customer-profile", kwargs={"username": "customer1"}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "customer1")  # Check if profile displays correct username

    def test_company_profile_access(self):
        self.client.login(username="company1", password="testpass123")
        response = self.client.get(reverse("users:company-profile", kwargs={"username": "company1"}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "company1")  # Check if profile displays correct username
