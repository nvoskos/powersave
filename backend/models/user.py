"""
User model
"""
from sqlalchemy import Column, String, Integer, Boolean, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..database import Base


class User(Base):
    __tablename__ = "user"

    # Primary Key
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Authentication
    ahk_account_number = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)

    # Personal Info
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))

    # Property Info (for Waste Fee Offset)
    property_number = Column(String(50), nullable=True)  # Αριθμός Υποστατικού
    property_address = Column(String(500))

    # Gamification Stats
    green_points_balance = Column(Integer, default=0)
    total_kwh_saved = Column(DECIMAL(10, 2), default=0)
    total_eur_saved = Column(DECIMAL(10, 2), default=0)
    total_co2_saved = Column(DECIMAL(10, 2), default=0)

    # Waste Wallet
    waste_wallet_balance = Column(DECIMAL(10, 2), default=0)
    annual_waste_fee = Column(DECIMAL(10, 2), nullable=True)

    # Municipality
    municipality_id = Column(UUID(as_uuid=True), ForeignKey("municipality.municipality_id"))

    # Status
    is_active = Column(Boolean, default=True)
    is_vulnerable_household = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    last_login_at = Column(TIMESTAMP, nullable=True)

    # Relationships
    municipality = relationship("Municipality", back_populates="users")
    saving_sessions = relationship("SavingSession", back_populates="user")
    wallet_transactions = relationship("WalletTransaction", back_populates="user")
    planted_items = relationship("UserPlantedItem", back_populates="user")
    challenge_progress = relationship("UserChallengeProgress", back_populates="user")
    badges = relationship("UserBadge", back_populates="user")

    def __repr__(self):
        return f"<User {self.ahk_account_number} - {self.first_name} {self.last_name}>"
