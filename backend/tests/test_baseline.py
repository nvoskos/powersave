"""
Unit tests for Baseline Calculation Service
"""
import pytest
from datetime import datetime, timedelta
from decimal import Decimal

from backend.services.baseline import BaselineService


class TestBaselineService:
    """Tests for baseline calculation"""

    def test_10_day_average_normal(self):
        """Test normal 10-day average calculation"""
        # Create mock historical data
        base_date = datetime(2025, 1, 1, 17, 0)  # 5 PM
        historical_data = []

        for day in range(1, 11):  # 10 days back
            session_start = base_date - timedelta(days=day)
            # 3-hour session: 17:00-20:00
            for hour_offset in range(3):
                timestamp = session_start + timedelta(hours=hour_offset)
                historical_data.append({
                    "timestamp": timestamp,
                    "consumption_kwh": 0.5  # 0.5 kWh per hour
                })

        # Calculate baseline
        baseline = BaselineService.calculate_10_day_average(
            historical_data=historical_data,
            session_start=base_date,
            session_duration_hours=3
        )

        # Should be approximately 1.5 kWh (0.5 × 3 hours)
        assert baseline is not None
        assert 1.4 <= baseline <= 1.6

    def test_10_day_average_with_outliers(self):
        """Test baseline calculation with outlier removal"""
        base_date = datetime(2025, 1, 1, 17, 0)
        historical_data = []

        for day in range(1, 11):
            session_start = base_date - timedelta(days=day)
            for hour_offset in range(3):
                timestamp = session_start + timedelta(hours=hour_offset)
                # Normal consumption except one outlier
                consumption = 10.0 if day == 5 else 0.5
                historical_data.append({
                    "timestamp": timestamp,
                    "consumption_kwh": consumption
                })

        baseline = BaselineService.calculate_10_day_average(
            historical_data=historical_data,
            session_start=base_date,
            session_duration_hours=3
        )

        # Outlier should be removed, baseline should be around 1.5 kWh
        assert baseline is not None
        assert 1.0 <= baseline <= 2.0

    def test_10_day_average_insufficient_data(self):
        """Test with insufficient historical data"""
        base_date = datetime(2025, 1, 1, 17, 0)
        historical_data = [
            {
                "timestamp": base_date - timedelta(days=1),
                "consumption_kwh": 0.5
            }
        ]

        baseline = BaselineService.calculate_10_day_average(
            historical_data=historical_data,
            session_start=base_date,
            session_duration_hours=3
        )

        # Should return None due to insufficient data
        assert baseline is None

    def test_same_weekday_average(self):
        """Test same weekday average calculation"""
        # Monday
        base_date = datetime(2025, 1, 6, 17, 0)  # Monday
        historical_data = []

        # Create data for 4 previous Mondays
        for week in range(1, 5):
            monday = base_date - timedelta(weeks=week)
            for hour_offset in range(3):
                timestamp = monday + timedelta(hours=hour_offset)
                historical_data.append({
                    "timestamp": timestamp,
                    "consumption_kwh": 0.6
                })

        baseline = BaselineService.calculate_same_weekday_average(
            historical_data=historical_data,
            session_start=base_date,
            session_duration_hours=3,
            weeks_back=4
        )

        # Should be approximately 1.8 kWh (0.6 × 3 hours)
        assert baseline is not None
        assert 1.6 <= baseline <= 2.0

    def test_seasonal_adjustment_summer(self):
        """Test seasonal adjustment for summer months"""
        baseline = Decimal("2.0")

        # July (peak AC season)
        adjusted = BaselineService.apply_seasonal_adjustment(baseline, 7)

        # Should be higher in summer
        assert adjusted > baseline
        assert adjusted == baseline * Decimal("1.30")

    def test_seasonal_adjustment_spring(self):
        """Test seasonal adjustment for spring"""
        baseline = Decimal("2.0")

        # April (mild weather)
        adjusted = BaselineService.apply_seasonal_adjustment(baseline, 4)

        # Should be lower in spring
        assert adjusted < baseline
        assert adjusted == baseline * Decimal("0.95")

    def test_validate_baseline_valid(self):
        """Test baseline validation with valid value"""
        baseline = Decimal("2.5")
        assert BaselineService.validate_baseline(baseline) is True

    def test_validate_baseline_invalid_negative(self):
        """Test baseline validation with negative value"""
        baseline = Decimal("-1.0")
        assert BaselineService.validate_baseline(baseline) is False

    def test_validate_baseline_invalid_too_high(self):
        """Test baseline validation with unreasonably high value"""
        baseline = Decimal("15.0")
        assert BaselineService.validate_baseline(baseline) is False

    def test_validate_baseline_none(self):
        """Test baseline validation with None"""
        assert BaselineService.validate_baseline(None) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
