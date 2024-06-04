from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class TestAuth(APITestCase):
    def setUp(self):
        self.email = "testuser@example.com"
        self.password = "testpassword"
        self.user = User.objects.create_user(email=self.email, password=self.password)
        self.req_token_url = reverse("api_token_obtain_pair")
        self.req_refresh_token_url = reverse("api_token_refresh")
        self.req_register_url = reverse("api_register")

    def test_jwt_authentication(self):
        url = self.req_token_url
        data = {"email": self.email, "password": self.password}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

    def test_jwt_authentication_invalid_credentials(self):
        url = self.req_token_url
        data = {"email": self.email, "password": "wrongpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_jwt_refresh(self):
        url = self.req_token_url
        data = {"email": self.email, "password": self.password}
        response = self.client.post(url, data, format="json")
        refresh_token = response.data["refresh"]

        url = self.req_refresh_token_url
        data = {"refresh": refresh_token}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)

    def test_user_registration(self):
        data = {"email": "newuser@example.com", "password": "kuvukiland"}
        response = self.client.post(self.req_register_url, data, format="json")
        self.assertEqual(response.status_code, 201)

        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

        self.assertEqual(response.data["email"], "newuser@example.com")
        self.assertNotIn("password", response.data)

    def test_short_password(self):
        data = {"email": "shortpassword@example.com", "password": "short"}
        response = self.client.post(self.req_register_url, data, format="json")

        self.assertEqual(response.status_code, 400)

        self.assertFalse(
            User.objects.filter(email="shortpassword@example.com").exists()
        )

        self.assertIn("password", response.data)

    def test_email_already_exist(self):
        data = {"email": "testuser", "password": ""}
        response = self.client.post(self.req_register_url, data, format="json")

        self.assertEqual(response.status_code, 400)

        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())

        self.assertIn("password", response.data)
