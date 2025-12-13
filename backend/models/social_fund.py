"""
Social Energy Fund model (Energy Solidarity)
"""
from sqlalchemy import Column, Integer, DECIMAL, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from ..database import Base


class SocialEnergyFund(Base):
    """
    Social Energy Fund for Energy Solidarity program
    Accumulates donations from citizens to help vulnerable households
    """
    __tablename__ = "social_energy_fund"

    fund_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    municipality_id = Column(UUID(as_uuid=True), ForeignKey("municipality.municipality_id"), nullable=True)

    # Balance tracking
    balance = Column(DECIMAL(12, 2), default=0)
    total_donations = Column(DECIMAL(12, 2), default=0)
    total_disbursements = Column(DECIMAL(12, 2), default=0)

    # Impact metrics
    households_helped = Column(Integer, default=0)
    total_kwh_donated = Column(DECIMAL(12, 2), default=0)

    # Relationships
    municipality = relationship("Municipality")

    def __repr__(self):
        return f"<SocialEnergyFund Balance: €{self.balance} - Helped: {self.households_helped}>"
