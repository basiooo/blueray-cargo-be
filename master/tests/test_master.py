from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from master.models import Country, Category

User = get_user_model()


class TestMaster(APITestCase):
    def setUp(self):
        User.objects.create_user(email="test@example.com", password="kuvukiland")
        data = {"email": "test@example.com", "password": "kuvukiland"}

        response = self.client.post(
            reverse("api_token_obtain_pair"), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.token = response.data.get("access")
        self.api_countries_url = reverse("api_countries")
        self.api_categories_url = reverse("api_categories")

    def test_init_country(self):
        assert Country.objects.count() > 1

    def test_init_category(self):
        assert Category.objects.count() > 1

    def test_get_all_coutry(self):
        response = self.client.get(
            self.api_countries_url,
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert len(response.data) > 1

    def test_get_search_coutry_empty(self):
        response = self.client.get(
            self.api_countries_url + "?search=Kuvukiland",
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert len(response.data) == 0

    def test_get_search_coutry_exist(self):
        response = self.client.get(
            self.api_countries_url + "?search=Indonesia",
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert len(response.data) == 1

    def test_get_search_coutry_exist_without_token(self):
        response = self.client.get(
            self.api_countries_url + "?search=Indonesia",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_categories(self):
        response = self.client.get(
            self.api_categories_url,
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert len(response.data) > 1

    def test_get_search_categories_empty(self):
        response = self.client.get(
            self.api_categories_url + "?country_id=1234567890",
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert len(response.data) == 0

    def test_get_search_categories_exist(self):
        coutry = Country.objects.get(name="China")
        response = self.client.get(
            self.api_categories_url + f"?country_id={coutry.pk}&search=Chip",
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert len(response.data) == 1

    def test_get_search_category_exist_without_token(self):
        response = self.client.get(
            self.api_categories_url + "?search=Chip",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
