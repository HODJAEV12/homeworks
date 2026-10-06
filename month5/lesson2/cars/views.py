from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CarSerializer
from .models import Car

class CarView(APIView):
    def get(self, request):
        car_data = cache.get('car_data')

        if car_data is not None:
            return Response(car_data)
        

        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        car_data = serializer.data

        cache.set('car_data', car_data, timeout=60)

        return Response(car_data)

    def post(self, request):
        serializer = CarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        cache.delete('car_data')

        return Response(serializer.data, status=status.HTTP_201_CREATED)