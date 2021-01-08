from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from api.models import Car, CarRate


class CarsApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.cars_url = reverse('cars')

        car = Car.objects.create(make="MAZDA", model="RX-6")
        self.cars_amount = Car.objects.all().count()
        CarRate.objects.create(car=car, rate=5)
        CarRate.objects.create(car=car, rate=4)
        CarRate.objects.create(car=car, rate=4)

    def test_add_new_car_that_exists(self):
        data = {
            "make": "AUDI",
            "model": "RS4"
        }

        response = self.client.post(self.cars_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.cars_amount += 1
        self.assertEqual(self.cars_amount, Car.objects.all().count())

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
        self.cars_amount += 1
        self.assertEqual(self.cars_amount, Car.objects.all().count())

        # Should get error (car exists)
        response = self.client.post(self.cars_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.cars_amount, Car.objects.all().count())

    def test_get_cars_with_avg_rate(self):
        response = self.client.get(self.cars_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()[0]
        pk = data['id']
        make = data['make']
        model = data['model']
        avg_rate = data['avg_rate']

        car = Car.objects.get(pk=pk)

        self.assertEqual(make, car.make)
        self.assertEqual(model, car.model)
        # add format, because from api we get string and from model we get float
        self.assertEqual(avg_rate, "{:.1f}".format(car.avg_rate))


class RateApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.rates_url = reverse('rate')
        self.popular_url = reverse('popular')

        self.cars = [
            Car.objects.create(make="MAZDA", model="RX-8"),
            Car.objects.create(make="AUDI", model="RS8"),
            Car.objects.create(make="AUDI", model="RS5")
        ]

        # one of the cars should not get any rates, amount of rates for cars must be descending
        # made for: test_get_popular_cars
        self.rates = [
            CarRate.objects.create(car=self.cars[0], rate=5),
            CarRate.objects.create(car=self.cars[0], rate=4),
            CarRate.objects.create(car=self.cars[0], rate=3),

            CarRate.objects.create(car=self.cars[1], rate=5),
            CarRate.objects.create(car=self.cars[1], rate=4)
        ]
        self.rates_amount = CarRate.objects.all().count()

    def test_add_new_rate(self):
        car_id = self.cars[0].id
        data = {
            'car': car_id,
            'rate': 4
        }

        response = self.client.post(self.rates_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.rates_amount += 1
        self.assertEqual(self.rates_amount, CarRate.objects.all().count())

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
        response = self.client.get(self.popular_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertNotEqual(len(data), len(self.cars))
        self.assertEqual(data[0]['id'], self.cars[0].id)
        self.assertEqual(data[1]['id'], self.cars[1].id)
