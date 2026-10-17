from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Books
from .serializers import BooksSerializers

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class BookListApi(APIView):
    @method_decorator(cache_page(60 * 5)) # с помощью втроенного декоратора
    def get(self, request, *args, **kwargs):
        books = Books.objects.all()
        serializer = BooksSerializers(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BooksSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
