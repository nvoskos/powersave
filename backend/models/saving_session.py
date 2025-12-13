"""
Saving Session model
"""
from sqlalchemy import Column, String, Integer, DECIMAL, TIMESTAMP, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..database import Base


class SavingSession(Base):
    __tablename__ = "saving_session"

    # Primary Key
    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, index=True)

    # Status: SCHEDULED, IN_PROGRESS, COMPLETED, FAILED, CANCELLED
    status = Column(String(20), nullable=False, default="SCHEDULED", index=True)

    # Timing
    scheduled_start = Column(TIMESTAMP, nullable=False, index=True)
    scheduled_end = Column(TIMESTAMP, nullable=False)
    actual_start = Column(TIMESTAMP, nullable=True)
    actual_end = Column(TIMESTAMP, nullable=True)

    # Baseline Calculation
    baseline_kwh = Column(DECIMAL(10, 4), nullable=True)
    baseline_calculation_method = Column(String(50), default="10_DAY_AVERAGE")

    # Actual Consumption
    actual_kwh = Column(DECIMAL(10, 4), nullable=True)

    # Results (Savings)
    saved_kwh = Column(DECIMAL(10, 4), nullable=True)
    saved_eur = Column(DECIMAL(10, 4), nullable=True)
    saved_co2_kg = Column(DECIMAL(10, 4), nullable=True)

    # Gamification
    green_points_earned = Column(Integer, default=0)
    is_double_points_day = Column(String(1), default="N")  # Y/N

    # Target Allocation (where savings go)
    allocation_type = Column(String(20), default="WASTE_WALLET")
    # WASTE_WALLET, SOLIDARITY_FUND, GREEN_COINS, MIXED

    # Metadata
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    completed_at = Column(TIMESTAMP, nullable=True)
    error_message = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="saving_sessions")

    def __repr__(self):
        return f"<SavingSession {self.session_id} - {self.status} - Saved: {self.saved_kwh} kWh>"
