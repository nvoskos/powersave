"""
Pydantic schemas for Saving Sessions
"""
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional
import uuid


class SessionCreateRequest(BaseModel):
    """Request to create a new saving session"""
    scheduled_start: datetime = Field(..., description="When session should start")
    duration_hours: int = Field(default=3, ge=1, le=6, description="Session duration in hours")
    allocation_type: str = Field(
        default="WASTE_WALLET",
        description="Where to allocate savings: WASTE_WALLET, SOLIDARITY_FUND, GREEN_COINS, MIXED"
    )


class SessionResponse(BaseModel):
    """Response for a saving session"""
    session_id: uuid.UUID
    user_id: uuid.UUID
    status: str
    scheduled_start: datetime
    scheduled_end: datetime
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    baseline_kwh: Optional[Decimal] = None
    actual_kwh: Optional[Decimal] = None
    saved_kwh: Optional[Decimal] = None
    saved_eur: Optional[Decimal] = None
    saved_co2_kg: Optional[Decimal] = None
    green_points_earned: int = 0
    is_double_points_day: str = "N"
    allocation_type: str
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SessionResultsResponse(BaseModel):
    """Detailed results after session completion"""
    session_id: uuid.UUID
    status: str
    savings: dict = Field(..., description="Savings details (kWh, EUR, CO2)")
    gamification: dict = Field(..., description="Points earned, badges unlocked")
    wallet_credit: Decimal = Field(..., description="Amount credited to waste wallet")
    message: str = Field(..., description="Congratulatory or feedback message")


class SessionStatsResponse(BaseModel):
    """User's overall session statistics"""
    total_sessions: int
    completed_sessions: int
    total_kwh_saved: Decimal
    total_eur_saved: Decimal
    total_co2_saved: Decimal
    total_green_points: int
    average_savings_per_session: Decimal
    current_streak_days: int = Field(..., description="Consecutive days with sessions")
