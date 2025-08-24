from datetime import date, timedelta

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Assignment, Listing


class ListingList(APITestCase):
    def setUp(self):
        self.listings_url = "/listings/"
        self.assignments_url = "/assignments/create/"

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
        response = self.client.get(self.listings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_data(self):
        response = self.client.get(self.listings_url)
        self.assertEqual(
            response.data,
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

    def test_create_assignment_200(self):
        """
        test that an assignment can be created against an existing listing
        """

        start_date = date.today() + timedelta(days=1)  # tomorrow
        end_date = start_date + timedelta(days=2)

        data = {
            "start_date": start_date,
            "end_date": end_date,
            "listing": self.listing_1.id,
        }

        response = self.client.post(self.assignments_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assignment.objects.count(), 3)
        assignment = Assignment.objects.first()
        self.assertEqual(assignment.listing, self.listing_1)

    def test_create_assignment_start_date_today_fails_400(self):
        """
        test should fail if start date of assignment is the same as current date
        """
        start_date = date.today()
        end_date = start_date + timedelta(days=2)
        data = {
            "listing": self.listing_1.id,
            "start_date": start_date,
            "end_date": end_date,
        }
        response = self.client.post(self.assignments_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("start_date", response.data)

    def test_create_assignment_overlap_fails_400(self):
        """
        test should fail if an overlapping assignment is found
        """
        # assignment
        start_date1 = date.today() + timedelta(days=1)
        end_date1 = start_date1 + timedelta(days=3)
        Assignment.objects.create(
            listing=self.listing_1, start_date=start_date1, end_date=end_date1
        )

        # Overlapping assignment
        start_date2 = date.today() + timedelta(days=2)
        end_date2 = start_date2 + timedelta(days=2)
        data = {
            "listing": self.listing_1.id,
            "start_date": start_date2,
            "end_date": end_date2,
        }
        response = self.client.post(self.assignments_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
