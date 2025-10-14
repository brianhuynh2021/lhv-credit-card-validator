from rest_framework import serializers
from .validators import sanitize_number, validate_digits, validate_length

   
class ValidateSerializer(serializers.Serializer):
    number = serializers.CharField()
    
    def validate_number(self, value: str) -> str:
        sanitized = sanitize_number(value)
        validate_length(sanitized)
        validate_digits(sanitized)
        return sanitized
    
class ValidateResponseSerializer(serializers.Serializer):
    valid = serializers.BooleanField()
    scheme = serializers.CharField()
    message = serializers.CharField()

class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()

class HealthResponseSerializer(serializers.Serializer):
    status = serializers.CharField()