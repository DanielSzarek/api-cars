from django.urls import path

from src.api import views

urlpatterns = [
    path('cars', views.CarView.as_view(), name='cars'),
    path('rate', views.CarRateView.as_view(), name='rate'),
    path('popular', views.CarPopularityView.as_view(), name='popular')
]
