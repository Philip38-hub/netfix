# from django.test import TestCase, override_settings
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from .models import Customer, Company


# User = get_user_model()
# @override_settings(CSRF_COOKIE_HTTPONLY=False)
# class UserTests(TestCase):

#     def setUp(self):
#         # Setup test data for customer and company registration
#         self.customer_data = {
#             'username': 'customer1',
#             'email': 'customer1@example.com',
#             'password1': 'Testpassword123',
#             'password2': 'Testpassword123',
#             'date_of_birth': '1990-01-01'
#         }

#         self.company_data = {
#             'username': 'company1',
#             'email': 'company1@example.com',
#             'password1': 'Testpassword123',
#             'password2': 'Testpassword123',
#             'field': 'Carpentry'
#         }

#     def test_customer_registration(self):
#         response = self.client.post(reverse('register_customer'), self.customer_data)
#         self.assertEqual(response.status_code, 302)  # Successful registration should redirect to profile
#         customer = User.objects.get(username='customer1')
#         self.assertTrue(customer.is_customer)

#     def test_company_registration(self):
#         response = self.client.post(reverse('register_company'), self.company_data)
#         self.assertEqual(response.status_code, 302)  # Successful registration should redirect to profile
#         company = User.objects.get(username='company1')
#         self.assertTrue(company.is_company)

#     def test_customer_login(self):
#         self.client.post(reverse('register_customer'), self.customer_data)
#         login_data = {'email': 'customer1@example.com', 'password': 'Testpassword123'}
#         response = self.client.post(reverse('login'), login_data)
#         self.assertEqual(response.status_code, 302)  # Successful login should redirect to customer profile

#     def test_company_login(self):
#         self.client.post(reverse('register_company'), self.company_data)
#         login_data = {'email': 'company1@example.com', 'password': 'Testpassword123'}
#         response = self.client.post(reverse('login'), login_data)
#         self.assertEqual(response.status_code, 302)  # Successful login should redirect to company profile

#     def test_customer_profile_access(self):
#         self.client.post(reverse('register_customer'), self.customer_data)
#         self.client.login(email='customer1@example.com', password='Testpassword123')
#         response = self.client.get(reverse('customer-profile'))
#         self.assertEqual(response.status_code, 200)

#     def test_profile_access_without_login(self):
#         response = self.client.get(reverse('customer-profile'))
#         self.assertRedirects(response, '/login/?next=/profile/customer/')
