from django.db.models import Count
from rest_framework import generics
from rest_framework.response import Response

from api.serializers import CarSerializer, CarRateSerializer, CarAvgRateSerializer
from api.models import Car, CarRate


class CarView(generics.ListCreateAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = Car.objects.all()
        serializer = CarAvgRateSerializer(queryset, many=True)
        return Response(serializer.data)


class CarRateView(generics.CreateAPIView):
    serializer_class = CarRateSerializer
    queryset = CarRate.objects.all()


class CarPopularityView(generics.ListAPIView):
    serializer_class = CarSerializer

    # Queryset:
    # 1. Count an amount of rates in CarRate's table
    # 2. Get cars that gets at least 1 rate
    # 3 Order DESC (From the most popular)
    queryset = Car.objects.annotate(car_rates_amount=Count('carrate'))\
        .filter(car_rates_amount__gt=0)\
        .order_by('-car_rates_amount')  # We can set an amount of given cars by [:5]
