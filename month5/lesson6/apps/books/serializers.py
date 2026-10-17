from rest_framework import serializers

from .models import Books


class BooksSerializers(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ("id", "title", "author", "price")
        read_only_fields = ("id",)
