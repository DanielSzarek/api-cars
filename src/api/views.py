from rest_framework import generics
from rest_framework.permissions import AllowAny

from api.serializers import CarSerializer, CarRateSerializer
from api.models import Car, CarRate


class CarView(generics.ListCreateAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    permission_classes = (AllowAny,)


class CarRateView(generics.CreateAPIView):
    serializer_class = CarRateSerializer
    queryset = CarRate.objects.all()
    permission_classes = (AllowAny,)
