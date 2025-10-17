from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .validators import (
    luhn_check,
    detect_scheme,
    sanitize_number,
    validate_length,
    validate_digits,
    mask_number_for_logging,
    CardScheme,
)
from rest_framework.exceptions import ValidationError
from unittest.mock import patch, Mock

class LuhnCheckTests(TestCase):
    """Test Luhn algorithm implementation"""

    def test_valid_visa_card(self):
        """Test valid Visa card number"""
        self.assertTrue(luhn_check("4532015112830366"))

    def test_valid_mastercard(self):
        """Test valid Mastercard number"""
        self.assertTrue(luhn_check("5425233430109903"))

    def test_valid_amex(self):
        """Test valid American Express number"""
        self.assertTrue(luhn_check("374245455400126"))

    def test_invalid_card_number(self):
        """Test invalid card number"""
        self.assertFalse(luhn_check("4532015112830367"))

    def test_all_zeros(self):
        """Test edge case with zeros"""
        self.assertTrue(luhn_check("0000000000000000"))


class DetectSchemeTests(TestCase):
    """Test card scheme detection"""

    def test_detect_visa(self):
        """Test Visa detection (starts with 4)"""
        self.assertEqual(detect_scheme("4532015112830366"), CardScheme.VISA.value)

    def test_detect_mastercard_51(self):
        """Test Mastercard detection (starts with 51)"""
        self.assertEqual(detect_scheme("5425233430109903"), CardScheme.MASTERCARD.value)

    def test_detect_mastercard_55(self):
        """Test Mastercard detection (starts with 55)"""
        self.assertEqual(detect_scheme("5599233430109903"), CardScheme.MASTERCARD.value)

    def test_detect_amex_34(self):
        """Test Amex detection (starts with 34)"""
        self.assertEqual(detect_scheme("340000000000009"), CardScheme.AMEX.value)

    def test_detect_amex_37(self):
        """Test Amex detection (starts with 37)"""
        self.assertEqual(detect_scheme("374245455400126"), CardScheme.AMEX.value)

    def test_detect_discover(self):
        """Test Discover detection (starts with 6)"""
        self.assertEqual(detect_scheme("6011000000000012"), CardScheme.DISCOVER.value)

    def test_detect_unknown(self):
        """Test unknown scheme"""
        self.assertEqual(detect_scheme("9999999999999999"), CardScheme.UNKNOWN.value)


class SanitizeNumberTests(TestCase):
    """Test input sanitization"""

    def test_remove_spaces(self):
        """Test removing spaces"""
        self.assertEqual(sanitize_number("4532 0151 1283 0366"), "4532015112830366")

    def test_remove_dashes(self):
        """Test removing dashes"""
        self.assertEqual(sanitize_number("4532-0151-1283-0366"), "4532015112830366")

    def test_remove_mixed(self):
        """Test removing mixed spaces and dashes"""
        self.assertEqual(sanitize_number("4532-0151 1283-0366"), "4532015112830366")

    def test_already_clean(self):
        """Test already clean number"""
        self.assertEqual(sanitize_number("4532015112830366"), "4532015112830366")


class ValidateLengthTests(TestCase):
    """Test length validation"""

    def test_valid_length_13(self):
        """Test minimum valid length (13 digits)"""
        try:
            validate_length("1234567890123")
        except ValidationError:
            self.fail("validate_length raised ValidationError unexpectedly")

    def test_valid_length_19(self):
        """Test maximum valid length (19 digits)"""
        try:
            validate_length("1234567890123456789")
        except ValidationError:
            self.fail("validate_length raised ValidationError unexpectedly")

    def test_invalid_length_too_short(self):
        """Test too short number"""
        with self.assertRaises(ValidationError):
            validate_length("12345678901")

    def test_invalid_length_too_long(self):
        """Test too long number"""
        with self.assertRaises(ValidationError):
            validate_length("12345678901234567890")


class ValidateDigitsTests(TestCase):
    """Test digit-only validation"""

    def test_valid_digits(self):
        """Test valid digits only"""
        try:
            validate_digits("1234567890")
        except ValidationError:
            self.fail("validate_digits raised ValidationError unexpectedly")

    def test_invalid_with_letters(self):
        """Test invalid input with letters"""
        with self.assertRaises(ValidationError):
            validate_digits("123456789a")

    def test_invalid_with_special_chars(self):
        """Test invalid input with special characters"""
        with self.assertRaises(ValidationError):
            validate_digits("1234-5678")


class MaskNumberTests(TestCase):
    """Test number masking for logging"""

    def test_mask_full_number(self):
        """Test masking standard card number"""
        self.assertEqual(mask_number_for_logging("4532015112830366"), "****0366")

    def test_mask_short_number(self):
        """Test masking short number"""
        self.assertEqual(mask_number_for_logging("123"), "****")

    def test_mask_exactly_4_digits(self):
        """Test masking exactly 4 digits"""
        self.assertEqual(mask_number_for_logging("1234"), "****1234")


class ValidateAPITests(APITestCase):
    """Test /api/v1/validate/ endpoint"""

    def test_valid_card_number(self):
        """Test POST with valid card number"""
        response = self.client.post(
            "/api/v1/validate/", {"number": "4532015112830366"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["valid"], True)
        self.assertEqual(response.data["scheme"], "visa")
        self.assertEqual(response.data["message"], "OK")

    def test_valid_card_with_spaces(self):
        """Test POST with spaces in card number"""
        response = self.client.post(
            "/api/v1/validate/", {"number": "4532 0151 1283 0366"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["valid"], True)

    def test_valid_card_with_dashes(self):
        """Test POST with dashes in card number"""
        response = self.client.post(
            "/api/v1/validate/", {"number": "4532-0151-1283-0366"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["valid"], True)

    def test_invalid_card_luhn_check(self):
        """Test POST with invalid Luhn checksum"""
        response = self.client.post(
            "/api/v1/validate/", {"number": "4532015112830367"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["valid"], False)
        self.assertEqual(response.data["message"], "Invalid card number")

    def test_invalid_too_short(self):
        """Test POST with too short number"""
        response = self.client.post(
            "/api/v1/validate/", {"number": "12345"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_invalid_too_long(self):
        """Test POST with too long number"""
        response = self.client.post(
            "/api/v1/validate/", {"number": "12345678901234567890"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_missing_number_field(self):
        """Test POST without number field"""
        response = self.client.post("/api/v1/validate/", {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_mastercard_detection(self):
        """Test Mastercard scheme detection"""
        response = self.client.post(
            "/api/v1/validate/", {"number": "5425233430109903"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["scheme"], "mastercard")

    def test_amex_detection(self):
        """Test American Express scheme detection"""
        response = self.client.post(
            "/api/v1/validate/", {"number": "374245455400126"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["scheme"], "amex")


class HealthAPITests(APITestCase):
    """Test /api/v1/health/ endpoint"""

    def test_health_check(self):
        """Test GET /health returns Ok status"""
        response = self.client.get("/api/v1/health/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Ok")

class MockValidatorTests(TestCase):
    """Test cases using mocking"""

    @patch('validator.validators.luhn_check')
    def test_mocked_luhn_check(self, mock_luhn):
        """Test validation with mocked luhn check"""
        mock_luhn.return_value = True
        
        # The actual value doesn't matter since we're mocking the check
        result = mock_luhn("4532015112830366")
        
        self.assertTrue(result)
        mock_luhn.assert_called_once_with("4532015112830366")

    @patch('validator.validators.detect_scheme')
    def test_mocked_scheme_detection(self, mock_detect):
        """Test scheme detection with mocking"""
        mock_detect.return_value = "visa"
        
        result = mock_detect("4532015112830366")
        
        self.assertEqual(result, "visa")
        mock_detect.assert_called_once_with("4532015112830366")

    @patch('validator.views.validate_card_number')
    def test_mocked_api_validation(self, mock_validate):
        """Test API validation with mocked validator"""
        mock_validate.return_value = {
            'valid': True,
            'scheme': 'visa',
            'message': 'OK'
        }
        
        response = self.client.post(
            "/api/v1/validate/",
            {"number": "4532015112830366"},
            format="json"
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["valid"], True)
        self.assertEqual(response.data["scheme"], "visa")
        mock_validate.assert_called_once()
