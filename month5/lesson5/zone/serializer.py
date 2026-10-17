from .models import Zone, Visitors
from rest_framework import serializers

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class VisitorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitors
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')