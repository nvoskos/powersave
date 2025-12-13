"""
Gamification models (Green Garden, Challenges, Badges)
"""
from sqlalchemy import Column, String, Integer, Boolean, DECIMAL, Date, TIMESTAMP, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..database import Base


class PlantCatalog(Base):
    """Plant catalog for Green Garden"""
    __tablename__ = "plant_catalog"

    plant_id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    cost_in_green_points = Column(Integer, nullable=False)
    growth_stages = Column(Integer, default=5)
    image_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    planted_items = relationship("UserPlantedItem", back_populates="plant")


class UserPlantedItem(Base):
    """User's planted items in Green Garden"""
    __tablename__ = "user_planted_item"

    planted_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, index=True)
    plant_id = Column(String(50), ForeignKey("plant_catalog.plant_id"), nullable=False)

    # Position in garden grid
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)

    # Growth
    current_growth_stage = Column(Integer, default=1)
    last_watered_at = Column(TIMESTAMP)

    # Timestamps
    planted_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="planted_items")
    plant = relationship("PlantCatalog", back_populates="planted_items")


class Challenge(Base):
    """Challenge definitions"""
    __tablename__ = "challenge"

    challenge_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    description = Column(Text)

    # Goal: TOTAL_KWH_SAVED, SESSION_COUNT, CONSECUTIVE_DAYS, COMMUNITY_GOAL
    goal_type = Column(String(50), nullable=False)
    goal_value = Column(DECIMAL(10, 2), nullable=False)

    # Duration
    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False, index=True)

    # Rewards
    reward_green_points = Column(Integer, default=0)
    reward_badge_id = Column(String(50), ForeignKey("badge.badge_id"), nullable=True)

    # Scope: INDIVIDUAL, COMMUNITY, SCHOOL, CORPORATE
    scope = Column(String(20), default="INDIVIDUAL")
    community_id = Column(UUID(as_uuid=True), nullable=True)

    # Status
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    progress = relationship("UserChallengeProgress", back_populates="challenge")
    reward_badge = relationship("Badge")


class UserChallengeProgress(Base):
    """User progress in challenges"""
    __tablename__ = "user_challenge_progress"

    progress_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, index=True)
    challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenge.challenge_id"), nullable=False, index=True)

    # Progress
    current_value = Column(DECIMAL(10, 2), default=0)
    status = Column(String(20), default="IN_PROGRESS")  # IN_PROGRESS, COMPLETED, EXPIRED

    # Timestamps
    joined_at = Column(TIMESTAMP, server_default=func.now())
    completed_at = Column(TIMESTAMP, nullable=True)

    # Relationships
    user = relationship("User", back_populates="challenge_progress")
    challenge = relationship("Challenge", back_populates="progress")


class Badge(Base):
    """Badge definitions"""
    __tablename__ = "badge"

    badge_id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    image_url = Column(String(500))

    # Category: BEGINNER, ACHIEVEMENT, STREAK, COMMUNITY, SPECIAL
    category = Column(String(50))

    # Rarity: COMMON, RARE, EPIC, LEGENDARY
    rarity = Column(String(20), default="COMMON")

    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge")


class UserBadge(Base):
    """User earned badges"""
    __tablename__ = "user_badge"

    user_badge_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, index=True)
    badge_id = Column(String(50), ForeignKey("badge.badge_id"), nullable=False)

    # Metadata
    earned_at = Column(TIMESTAMP, server_default=func.now())
    earning_session_id = Column(UUID(as_uuid=True), ForeignKey("saving_session.session_id"), nullable=True)
    earning_challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenge.challenge_id"), nullable=True)

    # Relationships
    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="user_badges")
    earning_session = relationship("SavingSession")
    earning_challenge = relationship("Challenge")
