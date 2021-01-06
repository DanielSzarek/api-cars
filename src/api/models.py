from django.db import models


class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        db_table = "car"
        unique_together = ("make", "model",)

    def __str__(self):
        return f"{self.make} {self.model}"


class CarRate(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField()  # Values: 1-5

    class Meta:
        db_table = "car_rate"

    def __str__(self):
        return f"{self.car}: {self.rate}"
