from rest_framework import serializers
import re
from enum import Enum


class CardScheme(Enum):
    VISA = "visa"
    MASTERCARD = "mastercard"
    AMEX = "amex"
    DISCOVER = "discover"
    UNKNOWN = 'unknown'

def sanitize_number(value: str) -> str:
    """Remove spaces and dashes from the input."""
    return re.sub(r"[^\d]", "", value)

def validate_length(number: str) -> None:
    """Ensure the number is between 12 and 19 digits"""
    if not (12 <= len(number) <= 19):
        raise serializers.ValidationError("Number must be between 12 and 19 digits.")

def validate_digits(number: str) -> None:
    """Ensure the number contains only digits."""
    if not number.isdigit():
        raise serializers.ValidationError("Number must contain only digits.")

def luhn_check(number: str):
    """
    Implement Luhn algorithm check:
    - Starting from rightmost digit, double every second digit
    - If doubling >= 10, subtract 9
    - Add up all digits
    - If total % 10 == 0 → valid
    """
    total = 0
    reverse_digits = number[::-1]
    
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1: # Every second digit from right
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0

def detect_scheme(number: str) -> str:
    """
    Detect credit card scheme based on number prefix (optional feature).
    Returns scheme name for API response.
    """
    
    if number.startswith('4'):
        return CardScheme.VISA.value
    elif number.startswith(('51', '52', '53', '54', '55')):
        return CardScheme.MASTERCARD.value
    elif number.startswith(('34', '37')):
        return CardScheme.AMEX.value
    elif number.startswith('6'):
        return CardScheme.DISCOVER.value
    else:
        return CardScheme.UNKNOWN.value

def mask_number_for_logging(number: str) -> str:
    """
    Mask card number for logging - show only last 4 digit.
    """
    if len(number) < 4:
        return "****"
    return f"****{number[-4:]}"
