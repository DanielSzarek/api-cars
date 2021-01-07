from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny

from api.serializers import CarSerializer
from api.models import Car


class ListCreateCarView(ListCreateAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    permission_classes = (AllowAny,)
