from django.urls import path
from .views import CarDetailApi, CarListApi

urlpatterns = [
    path("", CarListApi.as_view(), name="car_list"),
    path("<int:pk>/", CarDetailApi.as_view(), name="car_detail")
]