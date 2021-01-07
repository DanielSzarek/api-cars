from os.path import join

import requests
from rest_framework import serializers
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from api.models import Car, CarRate


def _validate_make(make):
    vpic_url = getattr(settings, "VPIC_API_URL")
    url = join(vpic_url, "GetMakesForVehicleType", "car?format=json")

    response = requests.get(url)
    results = response.json().get('Results')

    for result in results:
        # Looking for a make in response
        if result.get('MakeName').upper() == make.upper():
            return make

    raise ValidationError(_(f"there is no such a make: '{make}'"))


def _validate_model(make, model):
    vpic_url = getattr(settings, "VPIC_API_URL")
    url = join(vpic_url, "GetModelsForMake", f"{make}?format=json")

    response = requests.get(url)
    results = response.json().get('Results')

    for result in results:
        if result.get('Model_Name').lower() == model.lower():
            # Looking for a model in response
            return model

    raise ValidationError(_(f"there is no such a model: '{model}'"))


class CarSerializer(serializers.ModelSerializer):
    def validate(self, data):
        make = data['make']
        model = data['model']
        _validate_make(make)
        _validate_model(make, model)
        return data

    class Meta:
        model = Car
        fields = "__all__"


class RateSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        rate = attrs['rate']
        if rate < 1 or rate > 5:
            raise ValidationError(_("rate value should be in range from 1 to 5"))

    class Meta:
        model = CarRate
        fields = "__all__"
