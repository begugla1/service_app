from collections import OrderedDict
from decimal import Decimal

from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse_lazy, NoReverseMatch
from rest_framework import status
from rest_framework.test import APITestCase

from services.tests.test_mixins import MainApiTestMixin


class MainApiTestCase(MainApiTestMixin, APITestCase):
    def test_get(self):

        response = self.client.get(self.url)
        expected_data = {
            "result": [
                OrderedDict({
                    "id": 1,
                    "plan":
                        OrderedDict({
                            "id": 1,
                            "plan_type": "student",
                            "discount_percent": 65
                        }),
                    "client_username": "test_username1",
                    "client_company_name": "Amazon",
                    "client_email": "yokimokiadmin@gmail.com",
                    "service_name": "YouTube Premium",
                    "full_price": 1000,
                    "full_price_with_discount": '0.00'
                })
            ],
            "total_amount": Decimal('0.00')
        }
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_query(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(self.url)
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertEqual(5, len(queries))

    def test_wrong_url(self):
        self.url = reverse_lazy('subscriptions-list')
        try:
            self.client.get(self.url)
        except NoReverseMatch:
            return

    def test_get_detail(self):
        self.url = reverse_lazy('subscription-detail', args=(self.subscription1.id,))
        response = self.client.get(self.url)
        expected_data = {
            "id": self.subscription1.id,
            "plan":
                OrderedDict({
                    "id": self.subscription1.plan.id,
                    "plan_type": "student",
                    "discount_percent": 65
                }),
            "client_username": "test_username1",
            "client_company_name": "Amazon",
            "client_email": "yokimokiadmin@gmail.com",
            "service_name": "YouTube Premium",
            "full_price": 1000,
            "full_price_with_discount": '0.00'
        }
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)
