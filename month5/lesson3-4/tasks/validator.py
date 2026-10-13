from rest_framework import serializers
from django.utils import timezone

def validate_title(value):
    if len(value) < 5:
        raise serializers.ValidationError("Поле title не может содержать меньше 5 символов")
    elif value.isdigit():
        raise serializers.ValidationError("Поле title не может содержать только цифры")
    return value

def validate_priority(value):
    if not (1 <= value <= 5):
        raise serializers.ValidationError("Поле priority должно быть в диапазоне от 1 до 5")
    return value

# def validate(self, attrs):
#     due_date = attrs.get('due_date')
#     if due_date and due_date < timezone.now():
#         raise serializers.ValidationError(
#             {'due_date': 'Дата дедлайна не может быть в прошлом.'}
#         )
#     return attrs