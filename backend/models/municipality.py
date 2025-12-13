"""
Municipality model
"""
from sqlalchemy import Column, String, Boolean, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from ..database import Base


class Municipality(Base):
    __tablename__ = "municipality"

    # Primary Key
    municipality_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Basic Info
    name = Column(String(100), nullable=False)
    district = Column(String(50))

    # Waste Fee Configuration
    annual_waste_fee = Column(DECIMAL(10, 2))  # Default annual fee
    monthly_waste_fee = Column(DECIMAL(10, 2))  # Monthly fee

    # Payment Info
    bank_account = Column(String(50))
    api_endpoint = Column(String(500))  # Municipality's API for waste fee data
    api_key = Column(String(255))  # API authentication key

    # Status
    is_active = Column(Boolean, default=True)

    # Relationships
    users = relationship("User", back_populates="municipality")

    def __repr__(self):
        return f"<Municipality {self.name} - {self.district}>"
