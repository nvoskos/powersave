"""
Savings Calculation Service

Calculates actual savings, monetary value, CO2 impact, and green points.
"""
from decimal import Decimal
from typing import Optional

from ..config import get_settings

settings = get_settings()


class SavingsCalculationService:
    """
    Calculate savings from energy consumption reduction
    """

    @staticmethod
    def calculate_savings(
        baseline_kwh: Decimal,
        actual_kwh: Decimal,
        is_double_points_day: bool = False
    ) -> dict:
        """
        Calculate all savings metrics

        Args:
            baseline_kwh: Expected consumption
            actual_kwh: Actual consumption during session
            is_double_points_day: Whether bonus multiplier applies

        Returns:
            Dictionary with:
            - saved_kwh: Energy saved
            - saved_eur: Monetary value
            - saved_co2_kg: CO2 emissions saved
            - green_points_earned: Gamification points
        """
        # Calculate kWh saved
        saved_kwh = baseline_kwh - actual_kwh

        # No savings if consumption increased
        if saved_kwh <= 0:
            return {
                "saved_kwh": Decimal("0"),
                "saved_eur": Decimal("0"),
                "saved_co2_kg": Decimal("0"),
                "green_points_earned": 0,
                "savings_percentage": Decimal("0")
            }

        # Calculate monetary value (€)
        kwh_rate = Decimal(str(settings.KWH_TO_EUR_RATE))
        saved_eur = saved_kwh * kwh_rate

        # Calculate CO2 savings (kg)
        co2_factor = Decimal(str(settings.CO2_EMISSION_FACTOR))
        saved_co2_kg = saved_kwh * co2_factor

        # Calculate green points
        points_per_kwh = settings.GREEN_POINTS_PER_KWH
        base_points = int(saved_kwh * Decimal(str(points_per_kwh)))

        # Apply bonus multiplier if double points day
        if is_double_points_day:
            multiplier = Decimal(str(settings.BONUS_MULTIPLIER_DOUBLE_DAYS))
            green_points_earned = int(base_points * multiplier)
        else:
            green_points_earned = base_points

        # Calculate savings percentage
        savings_percentage = (saved_kwh / baseline_kwh) * Decimal("100")

        return {
            "saved_kwh": saved_kwh.quantize(Decimal("0.01")),
            "saved_eur": saved_eur.quantize(Decimal("0.01")),
            "saved_co2_kg": saved_co2_kg.quantize(Decimal("0.01")),
            "green_points_earned": green_points_earned,
            "savings_percentage": savings_percentage.quantize(Decimal("0.1"))
        }

    @staticmethod
    def calculate_waste_wallet_credit(
        saved_eur: Decimal,
        allocation_percentage: int = 100
    ) -> Decimal:
        """
        Calculate how much € goes to Waste Wallet

        Args:
            saved_eur: Total monetary savings
            allocation_percentage: % allocated to waste wallet (0-100)

        Returns:
            Amount to credit to waste wallet
        """
        if allocation_percentage < 0 or allocation_percentage > 100:
            raise ValueError("Allocation percentage must be between 0 and 100")

        allocation = Decimal(str(allocation_percentage)) / Decimal("100")
        credit = saved_eur * allocation

        return credit.quantize(Decimal("0.01"))

    @staticmethod
    def estimate_annual_savings(
        avg_session_savings_kwh: Decimal,
        sessions_per_month: int
    ) -> dict:
        """
        Estimate annual savings based on average session performance

        Args:
            avg_session_savings_kwh: Average kWh saved per session
            sessions_per_month: How many sessions per month user participates

        Returns:
            Dictionary with annual projections
        """
        # Monthly calculations
        monthly_kwh = avg_session_savings_kwh * Decimal(str(sessions_per_month))
        monthly_eur = monthly_kwh * Decimal(str(settings.KWH_TO_EUR_RATE))
        monthly_co2 = monthly_kwh * Decimal(str(settings.CO2_EMISSION_FACTOR))

        # Annual calculations
        annual_kwh = monthly_kwh * Decimal("12")
        annual_eur = monthly_eur * Decimal("12")
        annual_co2 = monthly_co2 * Decimal("12")

        return {
            "monthly_kwh": monthly_kwh.quantize(Decimal("0.01")),
            "monthly_eur": monthly_eur.quantize(Decimal("0.01")),
            "monthly_co2_kg": monthly_co2.quantize(Decimal("0.01")),
            "annual_kwh": annual_kwh.quantize(Decimal("0.01")),
            "annual_eur": annual_eur.quantize(Decimal("0.01")),
            "annual_co2_kg": annual_co2.quantize(Decimal("0.01")),
        }

    @staticmethod
    def calculate_waste_fee_coverage(
        waste_wallet_balance: Decimal,
        annual_waste_fee: Decimal
    ) -> dict:
        """
        Calculate how much of waste fee is covered

        Args:
            waste_wallet_balance: Current wallet balance
            annual_waste_fee: Annual waste fee amount

        Returns:
            Dictionary with coverage metrics
        """
        if annual_waste_fee <= 0:
            return {
                "coverage_percentage": Decimal("0"),
                "months_covered": Decimal("0"),
                "remaining_to_cover": Decimal("0")
            }

        # Calculate coverage percentage
        coverage_pct = (waste_wallet_balance / annual_waste_fee) * Decimal("100")
        coverage_pct = min(coverage_pct, Decimal("100"))  # Cap at 100%

        # Calculate months covered
        monthly_fee = annual_waste_fee / Decimal("12")
        months_covered = waste_wallet_balance / monthly_fee if monthly_fee > 0 else Decimal("0")

        # Calculate remaining amount needed
        remaining = annual_waste_fee - waste_wallet_balance
        remaining = max(remaining, Decimal("0"))  # Don't show negative

        return {
            "coverage_percentage": coverage_pct.quantize(Decimal("0.1")),
            "months_covered": months_covered.quantize(Decimal("0.1")),
            "remaining_to_cover": remaining.quantize(Decimal("0.01"))
        }
