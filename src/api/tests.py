from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from api.models import Car, CarRate


class CarsApiTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.cars_url = '/cars'

    def test_add_new_car_that_exists(self):
        data = {
            "make": "AUDI",
            "model": "RS4"
        }

        response = self.client.post(self.cars_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_new_car_that_not_exists(self):
        data = {
            "make": "AUDII",
            "model": "SR4"
        }

        response = self.client.post(self.cars_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_dont_add_car_twice(self):
        data = {
            "make": "AUDI",
            "model": "RS5"
        }

        # Should add this one
        response = self.client.post(self.cars_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Should get error (car exists)
        response = self.client.post(self.cars_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_cars_with_avg_rate(self):
        response = self.client.get(self.cars_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RateApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.rates_url = '/rate'
        self.popular_url = '/popular'

        cars = [
            Car.objects.create(make="MAZDA", model="RX-8"),
            Car.objects.create(make="AUDI", model="RS8")
        ]

        CarRate.objects.create(car=cars[0], rate=4)
        CarRate.objects.create(car=cars[0], rate=3)
        CarRate.objects.create(car=cars[1], rate=5)

    def test_add_new_rate(self):
        data = {
            'car': 1,
            'rate': 5
        }

        response = self.client.post(self.rates_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_dont_add_too_high_rate(self):
        data = {
            'car': 1,
            'rate': 6
        }

        response = self.client.post(self.rates_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_dont_add_too_low_rate(self):
        data = {
            'car': 1,
            'rate': 0
        }

        response = self.client.post(self.rates_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_popular_cars(self):
        # TODO Finish this test case (check data)
        response = self.client.get(self.popular_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
