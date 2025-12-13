"""
Unit Tests for PowerSave Waste Fee Offset System
================================================
Tests for savings calculations, baseline algorithm, and wallet operations
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from waste_fee_api import (
    calculate_savings_value,
    calculate_baseline,
    KWH_TO_EUR_RATE,
    DOUBLE_POINTS_MULTIPLIER,
    MUNICIPALITIES
)


class TestSavingsCalculations:
    """Tests for kWh to EUR conversion logic"""

    def test_basic_conversion(self):
        """Test basic kWh to EUR conversion"""
        kwh_saved = 1.0
        expected = kwh_saved * KWH_TO_EUR_RATE
        # Note: is_double_points_day() is checked internally
        result = calculate_savings_value(kwh_saved)
        assert result >= expected  # Could be doubled on weekends

    def test_zero_savings(self):
        """Test zero kWh saved"""
        result = calculate_savings_value(0)
        assert result == 0.0

    def test_negative_savings(self):
        """Test negative kWh (overconsumption) still calculates"""
        result = calculate_savings_value(-1.0)
        assert result < 0  # Negative savings

    def test_large_savings(self):
        """Test large kWh savings"""
        kwh_saved = 100.0
        result = calculate_savings_value(kwh_saved)
        # Should be at least 100 * 0.34 = 34
        assert result >= 34.0

    def test_decimal_precision(self):
        """Test that results have 2 decimal places"""
        result = calculate_savings_value(1.5)
        assert result == round(result, 2)


class TestBaselineAlgorithm:
    """Tests for 10-day average baseline calculation"""

    def test_basic_baseline(self):
        """Test basic baseline calculation"""
        history = [2.0, 2.5, 2.2, 2.3, 2.1, 2.4, 2.0, 2.6, 2.3, 2.1]
        result = calculate_baseline(history)
        expected = sum(history) / len(history)
        assert result == round(expected, 2)

    def test_empty_history(self):
        """Test empty consumption history"""
        result = calculate_baseline([])
        assert result == 0.0

    def test_single_day_history(self):
        """Test single day history"""
        result = calculate_baseline([2.5])
        assert result == 2.5

    def test_more_than_10_days(self):
        """Test that only last 10 days are used"""
        history = [1.0] * 5 + [3.0] * 10  # First 5 days = 1.0, last 10 days = 3.0
        result = calculate_baseline(history)
        assert result == 3.0  # Should only use last 10 days

    def test_less_than_10_days(self):
        """Test fewer than 10 days uses all available"""
        history = [2.0, 2.0, 2.0]
        result = calculate_baseline(history)
        assert result == 2.0

    def test_varying_consumption(self):
        """Test varying consumption patterns"""
        # Weekday low, weekend high pattern
        history = [1.5, 1.5, 1.5, 1.5, 1.5, 3.0, 3.0, 1.5, 1.5, 1.5]
        result = calculate_baseline(history)
        expected = sum(history) / 10
        assert result == round(expected, 2)


class TestMunicipalities:
    """Tests for municipality data"""

    def test_all_municipalities_have_required_fields(self):
        """Test all municipalities have required fields"""
        required_fields = ['id', 'name', 'name_en', 'annual_fee', 'region']

        for muni_id, muni in MUNICIPALITIES.items():
            for field in required_fields:
                assert field in muni, f"Municipality {muni_id} missing field: {field}"

    def test_annual_fees_are_positive(self):
        """Test all annual fees are positive"""
        for muni_id, muni in MUNICIPALITIES.items():
            assert muni['annual_fee'] > 0, f"Municipality {muni_id} has invalid annual fee"

    def test_nicosia_exists(self):
        """Test that Nicosia municipality exists"""
        assert 'nicosia' in MUNICIPALITIES
        assert MUNICIPALITIES['nicosia']['name'] == 'Δήμος Λευκωσίας'

    def test_municipality_count(self):
        """Test expected number of municipalities"""
        assert len(MUNICIPALITIES) >= 5  # At least 5 municipalities


class TestWalletOperations:
    """Tests for wallet balance calculations"""

    def test_progress_calculation(self):
        """Test progress percentage calculation"""
        total_paid = 46.25
        annual_target = 185.0
        progress = (total_paid / annual_target) * 100
        assert round(progress, 1) == 25.0

    def test_remaining_calculation(self):
        """Test remaining amount calculation"""
        total_paid = 46.25
        annual_target = 185.0
        remaining = max(0, annual_target - total_paid)
        assert remaining == 138.75

    def test_surplus_calculation(self):
        """Test surplus when overpaid"""
        total_paid = 200.0
        annual_target = 185.0
        surplus = total_paid - annual_target
        assert surplus == 15.0

    def test_no_negative_remaining(self):
        """Test remaining is never negative"""
        total_paid = 200.0
        annual_target = 185.0
        remaining = max(0, annual_target - total_paid)
        assert remaining == 0


class TestSessionCalculations:
    """Tests for savings session calculations"""

    def test_savings_calculation(self):
        """Test kWh saved calculation during session"""
        baseline = 2.5  # kWh expected
        actual = 0.5    # kWh used
        saved = max(0, baseline - actual)
        assert saved == 2.0

    def test_no_savings_if_over_baseline(self):
        """Test no savings if consumption exceeds baseline"""
        baseline = 2.5
        actual = 3.0
        saved = max(0, baseline - actual)
        assert saved == 0

    def test_double_points_multiplier(self):
        """Test double points multiplier value"""
        assert DOUBLE_POINTS_MULTIPLIER == 2.0

    def test_kwh_rate_reasonable(self):
        """Test kWh rate is in reasonable range"""
        # Cyprus electricity rates are typically €0.20-0.40 per kWh
        assert 0.20 <= KWH_TO_EUR_RATE <= 0.50


class TestEdgeCases:
    """Tests for edge cases and boundary conditions"""

    def test_very_small_savings(self):
        """Test very small kWh savings"""
        result = calculate_savings_value(0.001)
        assert result >= 0

    def test_very_large_savings(self):
        """Test very large kWh savings (unrealistic but should handle)"""
        result = calculate_savings_value(1000)
        assert result > 0

    def test_baseline_with_zeros(self):
        """Test baseline with zero consumption days"""
        history = [0, 0, 0, 2.0, 2.0, 2.0, 0, 0, 0, 0]
        result = calculate_baseline(history)
        assert result == 0.6  # Average of all values

    def test_baseline_all_same_values(self):
        """Test baseline when all days have same consumption"""
        history = [2.5] * 10
        result = calculate_baseline(history)
        assert result == 2.5


# Integration-style tests (without actual API calls)
class TestIntegrationScenarios:
    """Tests for complete scenarios"""

    def test_complete_session_scenario(self):
        """Test a complete savings session scenario"""
        # User joins session
        baseline = 2.5  # Their usual consumption

        # During session, they reduce to
        actual = 0.5

        # Calculate savings
        kwh_saved = max(0, baseline - actual)
        assert kwh_saved == 2.0

        # Calculate EUR earned
        eur_earned = calculate_savings_value(kwh_saved)
        assert eur_earned >= 0.68  # 2.0 * 0.34 = 0.68 (min)

    def test_annual_goal_achievement(self):
        """Test achieving annual goal through sessions"""
        annual_target = 185.0
        monthly_sessions = 12

        # If user earns €15.42 per month on average
        monthly_earning = annual_target / monthly_sessions
        assert round(monthly_earning, 2) == 15.42

        # That requires approximately X kWh savings per month
        kwh_needed = monthly_earning / KWH_TO_EUR_RATE
        assert round(kwh_needed, 1) == 45.4  # kWh per month

    def test_surplus_rollover(self):
        """Test surplus rollover to next year"""
        year_1_paid = 200.0
        year_1_target = 185.0

        surplus = year_1_paid - year_1_target
        assert surplus == 15.0

        # Rollover to year 2
        year_2_starting_balance = surplus
        year_2_target = 190.0  # New year, possibly new fee

        remaining_year_2 = year_2_target - year_2_starting_balance
        assert remaining_year_2 == 175.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
