from datetime import date

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Assignment, Listing


class ListingList(APITestCase):
    def setUp(self):
        self.listing_1 = Listing.objects.create(first_name="Ross", last_name="Geller")
        self.listing_2 = Listing.objects.create(first_name="Phoebe", last_name="Buffay")
        self.assignment_1 = Assignment.objects.create(
            start_date=date(2023, 2, 7),
            end_date=date(2023, 2, 15),
            listing=self.listing_1,
        )
        self.assignment_2 = Assignment.objects.create(
            start_date=date(2023, 4, 1),
            end_date=date(2023, 4, 4),
            listing=self.listing_2,
        )

    def test_get_200(self):
        response = self.client.get("/listings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_paginated_resp_200(self):
        response = self.client.get("/listings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)

    def test_get_data(self):
        response = self.client.get("/listings/")
        self.assertEqual(
            response.json()["results"],
            [
                {
                    "first_name": self.listing_1.first_name,
                    "last_name": self.listing_1.last_name,
                    "pets": [],
                    "assignments": [self.assignment_1.pk],
                },
                {
                    "first_name": self.listing_2.first_name,
                    "last_name": self.listing_2.last_name,
                    "pets": [],
                    "assignments": [self.assignment_2.pk],
                },
            ],
        )
