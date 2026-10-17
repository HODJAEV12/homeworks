from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "description")
        read_only_fields = ("id",)

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Минимум 3 символа в названии!")
        return value.strip()
