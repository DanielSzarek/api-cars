from django.urls import path

from api import views

urlpatterns = [
    path('cars', views.CarView.as_view()),
    path('rate', views.CarRateView.as_view()),
]
