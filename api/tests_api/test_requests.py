from rest_framework.test import APITestCase
from rest_framework import status
from api.models import VerificationRequest

from unittest.mock import patch

class VerificationRequestAPITest(APITestCase):

    def setUp(self):
        self.url = "/api/requests/"
        self.data = {
            "title": "Test",
            "address": "Kyiv",
            "phone": "123456",
            "source": "olx"
        }

    def test_create_request(self):
        response = self.client.post(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VerificationRequest.objects.count(), 1)

    def test_get_requests_list(self):
        VerificationRequest.objects.create(**self.data)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_request_detail(self):
        obj = VerificationRequest.objects.create(**self.data)

        response = self.client.get(f"/api/requests/{obj.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], obj.id)

    def test_filter_by_status(self):
        VerificationRequest.objects.create(**self.data, status="new")
        VerificationRequest.objects.create(**self.data, status="verified")

        response = self.client.get(self.url + "?status=verified")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_status(self):
        obj = VerificationRequest.objects.create(**self.data)

        response = self.client.patch(
            f"/api/requests/{obj.id}/status/",
            {"status": "verified"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        obj.refresh_from_db()
        self.assertEqual(obj.status, "verified")
    
    def test_duplicate_request_blocked(self):
        response1 = self.client.post(self.url, self.data, format="json")

        self.assertEqual(response1.status_code, 409)