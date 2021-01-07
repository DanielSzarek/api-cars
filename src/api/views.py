from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers import CarSerializer, CarRateSerializer, CarAvgRateSerializer
from api.models import Car, CarRate


class CarView(generics.ListCreateAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        queryset = Car.objects.all()
        print(queryset)
        serializer = CarAvgRateSerializer(queryset, many=True)
        return Response(serializer.data)


class CarRateView(generics.CreateAPIView):
    serializer_class = CarRateSerializer
    queryset = CarRate.objects.all()
    permission_classes = (AllowAny,)
