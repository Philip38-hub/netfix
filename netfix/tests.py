from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

User = get_user_model()


class NetfixAppTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        
        # URL reversals for core pages
        self.home_url = reverse('main:home')
        self.admin_url = reverse('admin:index')

    def test_home_url_resolves(self):
        """Test that the homepage URL resolves to the correct view"""
        resolver = resolve(self.home_url)
        self.assertEqual(resolver.view_name, 'main:home')
        
    def test_homepage_access(self):
        """Test that the homepage loads successfully with status 200"""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_admin_access_for_superuser(self):
        """Test that a superuser can access the admin page"""
        superuser = User.objects.create_superuser(
            username='admin_test', password='testpass123', email='admin@example.com'
        )
        self.client.login(username='admin_test', password='testpass123')
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 200)

    def test_admin_access_for_non_superuser(self):
        """Test that a non-superuser cannot access the admin page"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_included_urls(self):
        """Test that URLs from users and services apps are included and accessible"""
        users_urls = [
            reverse('users:register'),
            reverse('users:login'),
        ]
        services_urls = [
            reverse('services_list'),
            reverse('services_create')
        ]

        for url in users_urls + services_urls:
            response = self.client.get(url)
            self.assertIn(response.status_code, [200, 302])  # Either accessible or redirects to login
        
    def test_context_processors(self):
        """Confirm important context processors are loaded"""
        response = self.client.get(self.home_url)
        self.assertIn('user', response.context)  # User context processor
        self.assertIn('request', response.context)  # Request context processor
