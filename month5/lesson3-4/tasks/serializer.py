from rest_framework import serializers
from .models import Task
from .validator import validate_title, validate_priority

class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100, required=True, validators=[validate_title])
    priority = serializers.IntegerField(required=True, validators=[validate_priority])
    # due_date = serializers.DateTimeField(required=True, validators=[validate])

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')