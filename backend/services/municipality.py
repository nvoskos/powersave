"""
Municipality Integration Service

Handles integration with municipal systems for:
- Property registration
- Waste fee data
- Payment processing
"""
import httpx
from typing import Optional, Dict
from decimal import Decimal
import logging

from ..config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class MunicipalityIntegrationService:
    """
    Integration with Municipality APIs for waste fee management
    """

    def __init__(self):
        self.base_url = settings.MUNICIPALITY_API_BASE_URL
        self.api_key = settings.MUNICIPALITY_API_KEY

    async def verify_property(
        self,
        property_number: str,
        municipality_name: str
    ) -> Optional[Dict]:
        """
        Verify property number with municipality cadastral system

        Args:
            property_number: Αριθμός Υποστατικού
            municipality_name: Municipality name

        Returns:
            Property details or None if not found
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/properties/{property_number}",
                    headers={"X-API-Key": self.api_key},
                    params={"municipality": municipality_name},
                    timeout=10.0
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "property_number": data.get("property_number"),
                        "address": data.get("address"),
                        "owner_name": data.get("owner_name"),
                        "annual_waste_fee": Decimal(str(data.get("annual_waste_fee", 0))),
                        "is_valid": True
                    }
                elif response.status_code == 404:
                    logger.warning(f"Property {property_number} not found")
                    return None
                else:
                    logger.error(f"Municipality API error: {response.status_code}")
                    return None

        except httpx.RequestError as e:
            logger.error(f"Failed to verify property: {e}")
            return None

    async def get_waste_fee_balance(
        self,
        property_number: str
    ) -> Optional[Dict]:
        """
        Get current waste fee balance from municipality

        Args:
            property_number: Αριθμός Υποστατικού

        Returns:
            Balance information
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/waste-fees/{property_number}/balance",
                    headers={"X-API-Key": self.api_key},
                    timeout=10.0
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "property_number": property_number,
                        "outstanding_balance": Decimal(str(data.get("outstanding_balance", 0))),
                        "last_payment_date": data.get("last_payment_date"),
                        "last_payment_amount": Decimal(str(data.get("last_payment_amount", 0))),
                        "annual_fee": Decimal(str(data.get("annual_fee", 0)))
                    }
                else:
                    logger.error(f"Failed to get balance: {response.status_code}")
                    return None

        except httpx.RequestError as e:
            logger.error(f"Failed to get waste fee balance: {e}")
            return None

    async def submit_payment(
        self,
        property_number: str,
        amount: Decimal,
        payment_source: str = "POWERSAVE_WALLET"
    ) -> bool:
        """
        Submit payment to municipality via PowerSave Waste Wallet

        Args:
            property_number: Αριθμός Υποστατικού
            amount: Payment amount in EUR
            payment_source: Source identifier

        Returns:
            True if successful, False otherwise
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/waste-fees/{property_number}/payments",
                    headers={"X-API-Key": self.api_key},
                    json={
                        "amount": str(amount),
                        "payment_source": payment_source,
                        "payment_method": "DIGITAL_WALLET"
                    },
                    timeout=10.0
                )

                if response.status_code == 200:
                    logger.info(f"Payment successful: €{amount} for {property_number}")
                    return True
                else:
                    logger.error(f"Payment failed: {response.status_code} - {response.text}")
                    return False

        except httpx.RequestError as e:
            logger.error(f"Failed to submit payment: {e}")
            return False

    async def register_powersave_user(
        self,
        property_number: str,
        ahk_account_number: str,
        user_email: str
    ) -> bool:
        """
        Register PowerSave user with municipality for auto-payment

        Args:
            property_number: Αριθμός Υποστατικού
            ahk_account_number: EAC account number
            user_email: User email

        Returns:
            True if successful
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/powersave/registrations",
                    headers={"X-API-Key": self.api_key},
                    json={
                        "property_number": property_number,
                        "ahk_account_number": ahk_account_number,
                        "email": user_email,
                        "auto_payment_enabled": True
                    },
                    timeout=10.0
                )

                return response.status_code == 200

        except httpx.RequestError as e:
            logger.error(f"Failed to register user: {e}")
            return False

    def generate_property_qr_code(
        self,
        property_number: str
    ) -> str:
        """
        Generate QR code data for property registration

        The QR code contains a URL that when scanned opens the PowerSave app
        with property information pre-filled.

        Args:
            property_number: Αριθμός Υποστατικού

        Returns:
            QR code data (URL)
        """
        # In production, this would be a deep link to the mobile app
        return f"powersave://register/property?number={property_number}"

    @staticmethod
    def validate_property_number(property_number: str) -> bool:
        """
        Validate property number format

        Cyprus property numbers typically follow format: XX/YYYY or XXX/YYYY

        Args:
            property_number: Property number to validate

        Returns:
            True if valid format
        """
        if not property_number:
            return False

        # Remove spaces
        property_number = property_number.replace(" ", "")

        # Basic validation: should contain "/"
        if "/" not in property_number:
            return False

        parts = property_number.split("/")
        if len(parts) != 2:
            return False

        # First part should be 2-3 digits, second part 1-5 digits
        try:
            block = int(parts[0])
            plot = int(parts[1])
            return 1 <= block <= 999 and 1 <= plot <= 99999
        except ValueError:
            return False
