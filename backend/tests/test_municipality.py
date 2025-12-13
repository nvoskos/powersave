"""
Unit tests for Municipality Integration Service
"""
import pytest

from backend.services.municipality import MunicipalityIntegrationService


class TestMunicipalityIntegrationService:
    """Tests for municipality integration"""

    def test_validate_property_number_valid(self):
        """Test valid property number formats"""
        valid_numbers = [
            "12/345",
            "1/1",
            "999/99999",
            "45/678",
        ]

        for number in valid_numbers:
            assert MunicipalityIntegrationService.validate_property_number(number) is True

    def test_validate_property_number_invalid(self):
        """Test invalid property number formats"""
        invalid_numbers = [
            "",
            "12345",  # No slash
            "12-345",  # Wrong separator
            "12/",  # Missing plot number
            "/345",  # Missing block number
            "1000/1",  # Block too high
            "1/100000",  # Plot too high
            "abc/def",  # Not numeric
        ]

        for number in invalid_numbers:
            assert MunicipalityIntegrationService.validate_property_number(number) is False

    def test_validate_property_number_with_spaces(self):
        """Test property number with spaces"""
        # Should handle spaces by removing them
        assert MunicipalityIntegrationService.validate_property_number("12 / 345") is True

    def test_generate_qr_code(self):
        """Test QR code generation"""
        service = MunicipalityIntegrationService()
        property_number = "12/345"

        qr_data = service.generate_property_qr_code(property_number)

        assert qr_data is not None
        assert "powersave://" in qr_data
        assert property_number in qr_data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
