"""
Baseline Calculation Service

Calculates the baseline consumption for a user based on historical data.
The baseline is used to determine savings during a session.
"""
from datetime import datetime, timedelta
from typing import List, Optional
from decimal import Decimal
import statistics

from ..config import get_settings

settings = get_settings()


class BaselineService:
    """
    Baseline calculation for energy consumption

    Methods:
    - 10-day average (default)
    - Same-day-of-week average
    - Seasonal adjustment
    """

    @staticmethod
    def calculate_10_day_average(
        historical_data: List[dict],
        session_start: datetime,
        session_duration_hours: int = 3
    ) -> Optional[Decimal]:
        """
        Calculate 10-day average baseline consumption

        Args:
            historical_data: List of dicts with 'timestamp' and 'consumption_kwh'
            session_start: When the session starts
            session_duration_hours: Duration of session in hours

        Returns:
            Baseline consumption in kWh for the session duration
        """
        if not historical_data or len(historical_data) < 5:
            return None

        # Get the same time window for the past 10 days
        session_hour = session_start.hour
        session_end_hour = (session_start + timedelta(hours=session_duration_hours)).hour

        # Filter historical data for the same time window
        relevant_consumptions = []

        for i in range(1, 11):  # Last 10 days
            day_start = session_start - timedelta(days=i)
            day_end = day_start + timedelta(hours=session_duration_hours)

            # Sum consumption for this time window
            day_consumption = sum(
                Decimal(str(entry['consumption_kwh']))
                for entry in historical_data
                if day_start <= entry['timestamp'] < day_end
            )

            if day_consumption > 0:
                relevant_consumptions.append(day_consumption)

        if len(relevant_consumptions) < 5:
            return None

        # Calculate average, removing outliers
        baseline = BaselineService._calculate_average_with_outlier_removal(
            relevant_consumptions
        )

        return baseline

    @staticmethod
    def calculate_same_weekday_average(
        historical_data: List[dict],
        session_start: datetime,
        session_duration_hours: int = 3,
        weeks_back: int = 4
    ) -> Optional[Decimal]:
        """
        Calculate baseline using same weekday average
        (e.g., average of last 4 Mondays)

        Args:
            historical_data: List of dicts with 'timestamp' and 'consumption_kwh'
            session_start: When the session starts
            session_duration_hours: Duration of session
            weeks_back: Number of weeks to look back

        Returns:
            Baseline consumption in kWh
        """
        target_weekday = session_start.weekday()
        session_hour = session_start.hour

        relevant_consumptions = []

        for i in range(1, weeks_back + 1):
            # Go back i weeks
            historical_date = session_start - timedelta(weeks=i)

            # Ensure it's the same weekday
            if historical_date.weekday() == target_weekday:
                day_start = historical_date.replace(
                    hour=session_start.hour,
                    minute=0,
                    second=0,
                    microsecond=0
                )
                day_end = day_start + timedelta(hours=session_duration_hours)

                day_consumption = sum(
                    Decimal(str(entry['consumption_kwh']))
                    for entry in historical_data
                    if day_start <= entry['timestamp'] < day_end
                )

                if day_consumption > 0:
                    relevant_consumptions.append(day_consumption)

        if len(relevant_consumptions) < 2:
            return None

        return BaselineService._calculate_average_with_outlier_removal(
            relevant_consumptions
        )

    @staticmethod
    def _calculate_average_with_outlier_removal(
        values: List[Decimal]
    ) -> Decimal:
        """
        Calculate average while removing outliers (values > 2 std dev from mean)

        Args:
            values: List of consumption values

        Returns:
            Average after outlier removal
        """
        if len(values) < 3:
            return Decimal(str(statistics.mean(values)))

        # Convert to float for statistics calculations
        float_values = [float(v) for v in values]

        mean = statistics.mean(float_values)
        std_dev = statistics.stdev(float_values)

        # Filter outliers (values within 2 standard deviations)
        filtered = [
            v for v in float_values
            if abs(v - mean) <= 2 * std_dev
        ]

        if not filtered:
            filtered = float_values  # Keep all if all are outliers

        return Decimal(str(statistics.mean(filtered)))

    @staticmethod
    def apply_seasonal_adjustment(
        baseline: Decimal,
        month: int
    ) -> Decimal:
        """
        Apply seasonal adjustment factor to baseline

        Cyprus has higher consumption in summer (AC) and winter (heating)

        Args:
            baseline: Calculated baseline
            month: Month (1-12)

        Returns:
            Adjusted baseline
        """
        # Seasonal factors for Cyprus
        seasonal_factors = {
            1: 1.15,   # January (heating)
            2: 1.10,   # February
            3: 1.00,   # March
            4: 0.95,   # April
            5: 1.05,   # May
            6: 1.20,   # June (AC starts)
            7: 1.30,   # July (peak AC)
            8: 1.30,   # August (peak AC)
            9: 1.20,   # September
            10: 1.00,  # October
            11: 1.05,  # November
            12: 1.15,  # December (heating)
        }

        factor = Decimal(str(seasonal_factors.get(month, 1.0)))
        return baseline * factor

    @staticmethod
    def validate_baseline(baseline: Optional[Decimal]) -> bool:
        """
        Validate that baseline is reasonable

        Args:
            baseline: Calculated baseline

        Returns:
            True if valid, False otherwise
        """
        if baseline is None:
            return False

        # Baseline should be positive and less than 10 kWh for a 3-hour session
        # (typical household max consumption)
        if baseline <= 0 or baseline > 10:
            return False

        return True
