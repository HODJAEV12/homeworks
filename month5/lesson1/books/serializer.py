from rest_framework import serializers
from .models import Books

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__' # автоматически включает все поля модели в сериализатор
        read_only_fields = ('id',) # поле id будет доступно только для чтения
