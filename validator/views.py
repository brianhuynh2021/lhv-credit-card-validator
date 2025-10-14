from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import ValidateSerializer, ValidateResponseSerializer, ErrorResponseSerializer, HealthResponseSerializer
from .validators import luhn_check, detect_scheme, mask_number_for_logging
import logging

logger = logging.getLogger('validator')

class ValidateView(APIView):
    """
    POST /validate
    Validates credit card number using Luhn algorithm
    """
    @extend_schema(
        request=ValidateSerializer,
        responses={
            200: ValidateResponseSerializer,
            400: ErrorResponseSerializer,
        }
    )
    def post(self, request):
        serializer = ValidateSerializer(data=request.data)
        
        if not serializer.is_valid():
            # Return 400 with error message as per PDF requirement
            field_errors = list(serializer.errors.values())
            error_message = field_errors[0][0] if field_errors else 'Invalid input'
            return Response(
                {"error": str(error_message)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get sanitized number from serializer
        number = serializer.validated_data['number']
        
        # Run Luhn check and detect scheme
        is_valid = luhn_check(number)
        scheme = detect_scheme(number)
        
        logger.info(
            "Card validation completed",
            extra={
                'scheme': scheme,
                'valid': is_valid,
                'masked_number': mask_number_for_logging(number),
                'request_id': getattr(request, 'request_id', '-'),
            }
        )
        
        return Response({
            "valid": is_valid,
            "scheme": scheme,
            "message": "OK" if is_valid else "Invalid card number"
        })
class HealthView(APIView):
    """
    GET /health
    Returns health status
    """
    @extend_schema(responses={200: HealthResponseSerializer})
    def get(self, request):
        return Response({"status": "Ok"})