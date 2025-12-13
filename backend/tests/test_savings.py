"""
Unit tests for Savings Calculation Service
"""
import pytest
from decimal import Decimal

from backend.services.savings import SavingsCalculationService


class TestSavingsCalculationService:
    """Tests for savings calculations"""

    def test_calculate_savings_positive(self):
        """Test savings calculation with positive savings"""
        baseline = Decimal("2.0")
        actual = Decimal("1.5")

        result = SavingsCalculationService.calculate_savings(
            baseline_kwh=baseline,
            actual_kwh=actual,
            is_double_points_day=False
        )

        assert result["saved_kwh"] == Decimal("0.50")
        assert result["saved_eur"] == Decimal("0.15")  # 0.5 × €0.30
        assert result["saved_co2_kg"] == Decimal("0.35")  # 0.5 × 0.7
        assert result["green_points_earned"] == 5  # 0.5 × 10
        assert result["savings_percentage"] == Decimal("25.0")

    def test_calculate_savings_zero(self):
        """Test when consumption equals baseline (no savings)"""
        baseline = Decimal("2.0")
        actual = Decimal("2.0")

        result = SavingsCalculationService.calculate_savings(
            baseline_kwh=baseline,
            actual_kwh=actual,
            is_double_points_day=False
        )

        assert result["saved_kwh"] == Decimal("0")
        assert result["saved_eur"] == Decimal("0")
        assert result["saved_co2_kg"] == Decimal("0")
        assert result["green_points_earned"] == 0
        assert result["savings_percentage"] == Decimal("0")

    def test_calculate_savings_negative(self):
        """Test when consumption increases (negative savings)"""
        baseline = Decimal("2.0")
        actual = Decimal("2.5")

        result = SavingsCalculationService.calculate_savings(
            baseline_kwh=baseline,
            actual_kwh=actual,
            is_double_points_day=False
        )

        # Should return zeros when consumption increased
        assert result["saved_kwh"] == Decimal("0")
        assert result["saved_eur"] == Decimal("0")
        assert result["green_points_earned"] == 0

    def test_calculate_savings_double_points(self):
        """Test savings calculation with double points day"""
        baseline = Decimal("2.0")
        actual = Decimal("1.5")

        result = SavingsCalculationService.calculate_savings(
            baseline_kwh=baseline,
            actual_kwh=actual,
            is_double_points_day=True
        )

        # Points should be doubled
        assert result["green_points_earned"] == 10  # 5 × 2

    def test_waste_wallet_credit_full(self):
        """Test waste wallet credit calculation at 100%"""
        saved_eur = Decimal("10.00")

        credit = SavingsCalculationService.calculate_waste_wallet_credit(
            saved_eur=saved_eur,
            allocation_percentage=100
        )

        assert credit == Decimal("10.00")

    def test_waste_wallet_credit_partial(self):
        """Test waste wallet credit calculation at 50%"""
        saved_eur = Decimal("10.00")

        credit = SavingsCalculationService.calculate_waste_wallet_credit(
            saved_eur=saved_eur,
            allocation_percentage=50
        )

        assert credit == Decimal("5.00")

    def test_waste_wallet_credit_invalid_percentage(self):
        """Test waste wallet credit with invalid percentage"""
        saved_eur = Decimal("10.00")

        with pytest.raises(ValueError):
            SavingsCalculationService.calculate_waste_wallet_credit(
                saved_eur=saved_eur,
                allocation_percentage=150
            )

    def test_estimate_annual_savings(self):
        """Test annual savings estimation"""
        avg_session_savings = Decimal("0.5")  # 0.5 kWh per session
        sessions_per_month = 20

        result = SavingsCalculationService.estimate_annual_savings(
            avg_session_savings_kwh=avg_session_savings,
            sessions_per_month=sessions_per_month
        )

        # Monthly: 0.5 × 20 = 10 kWh
        assert result["monthly_kwh"] == Decimal("10.00")
        assert result["monthly_eur"] == Decimal("3.00")  # 10 × €0.30

        # Annual: 10 × 12 = 120 kWh
        assert result["annual_kwh"] == Decimal("120.00")
        assert result["annual_eur"] == Decimal("36.00")  # 120 × €0.30

    def test_waste_fee_coverage_full(self):
        """Test waste fee coverage at 100%"""
        wallet_balance = Decimal("120.00")
        annual_fee = Decimal("120.00")

        result = SavingsCalculationService.calculate_waste_fee_coverage(
            waste_wallet_balance=wallet_balance,
            annual_waste_fee=annual_fee
        )

        assert result["coverage_percentage"] == Decimal("100.0")
        assert result["months_covered"] == Decimal("12.0")
        assert result["remaining_to_cover"] == Decimal("0.00")

    def test_waste_fee_coverage_partial(self):
        """Test waste fee coverage at 50%"""
        wallet_balance = Decimal("60.00")
        annual_fee = Decimal("120.00")

        result = SavingsCalculationService.calculate_waste_fee_coverage(
            waste_wallet_balance=wallet_balance,
            annual_waste_fee=annual_fee
        )

        assert result["coverage_percentage"] == Decimal("50.0")
        assert result["months_covered"] == Decimal("6.0")
        assert result["remaining_to_cover"] == Decimal("60.00")

    def test_waste_fee_coverage_over_100(self):
        """Test waste fee coverage exceeding 100%"""
        wallet_balance = Decimal("150.00")
        annual_fee = Decimal("120.00")

        result = SavingsCalculationService.calculate_waste_fee_coverage(
            waste_wallet_balance=wallet_balance,
            annual_waste_fee=annual_fee
        )

        # Should cap at 100%
        assert result["coverage_percentage"] == Decimal("100.0")
        assert result["remaining_to_cover"] == Decimal("0.00")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
