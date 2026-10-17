from rest_framework import serializers
from .models import Shop

class ShopSer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Shop
        fields = ('id', 'name', 'color', 'logo', 'user')
        read_only_fields = ('id', 'user')
