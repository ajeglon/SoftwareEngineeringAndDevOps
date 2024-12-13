from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

# Tests for user login
class UserLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_valid_user_login(self):
        # POST request with valid credentials
        response = self.client.post(reverse('index'), {
            'username': 'testuser',
            'password': 'testpassword',
        }, follow=True)

        # user successfully logged in
        self.assertRedirects(response, reverse('index'))
        self.assertIn('_auth_user_id', self.client.session)  # Check session for login
        self.assertContains(response, "Succesfully logged in", html=False)

    def test_invalid_user_login(self):
        # POST request with invalid credentials
        response = self.client.post(reverse('index'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        }, follow=True)

        # Check that the user is not logged in
        self.assertNotIn('_auth_user_id', self.client.session)  # No login in session
        self.assertContains(response, "There was an error login, please try again")

    def test_get_request(self):
        # GET request
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')