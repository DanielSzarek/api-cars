from os.path import join

import requests
from rest_framework import serializers
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from api.models import Car


def _validate_make(make):
    vpic_url = getattr(settings, "VPIC_API_URL")
    url = join(vpic_url, "GetMakesForVehicleType", "car?format=json")

    response = requests.get(url)
    results = response.json().get('Results')

    for result in results:
        # Looking for make in response
        if result.get('MakeName').upper() == make.upper():
            return make

    message = _(f"There is no such a make: '{make}'")
    raise ValidationError(message)


def _validate_model(make, model):
    vpic_url = getattr(settings, "VPIC_API_URL")
    url = join(vpic_url, "GetModelsForMake", f"{make}?format=json")

    response = requests.get(url)
    results = response.json().get('Results')

    for result in results:
        if result.get('Model_Name').lower() == model.lower():
            # Looking for a model in response
            return model

    message = _(f"There is no such a model: '{model}'")
    raise ValidationError(message)


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
