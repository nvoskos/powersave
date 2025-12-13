"""
Saving Sessions API Router

Endpoints for managing energy saving sessions.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from decimal import Decimal
import uuid

from ..database import get_db
from ..schemas.session import (
    SessionCreateRequest,
    SessionResponse,
    SessionResultsResponse,
    SessionStatsResponse
)
from ..models.saving_session import SavingSession
from ..models.user import User
from ..services.baseline import BaselineService
from ..services.savings import SavingsCalculationService
from ..services.wallet import WasteWalletService
from ..config import get_settings

settings = get_settings()
router = APIRouter()


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    request: SessionCreateRequest,
    user_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Create a new saving session

    Schedules a new energy saving session for the user.
    """
    # Verify user exists
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Calculate scheduled_end
    scheduled_end = request.scheduled_start + timedelta(hours=request.duration_hours)

    # Create session
    session = SavingSession(
        user_id=user_id,
        status="SCHEDULED",
        scheduled_start=request.scheduled_start,
        scheduled_end=scheduled_end,
        allocation_type=request.allocation_type
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Get details of a specific session
    """
    session = db.query(SavingSession).filter(
        SavingSession.session_id == session_id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    return session


@router.get("/user/{user_id}", response_model=List[SessionResponse])
async def get_user_sessions(
    user_id: uuid.UUID,
    status_filter: str = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get all sessions for a user

    Can be filtered by status (SCHEDULED, IN_PROGRESS, COMPLETED, etc.)
    """
    query = db.query(SavingSession).filter(SavingSession.user_id == user_id)

    if status_filter:
        query = query.filter(SavingSession.status == status_filter.upper())

    sessions = (
        query
        .order_by(SavingSession.scheduled_start.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )

    return sessions


@router.post("/{session_id}/start", response_model=SessionResponse)
async def start_session(
    session_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Start a scheduled session

    Calculates baseline and marks session as IN_PROGRESS.
    """
    session = db.query(SavingSession).filter(
        SavingSession.session_id == session_id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    if session.status != "SCHEDULED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot start session with status {session.status}"
        )

    # Calculate baseline (In production, fetch from AHK API)
    # For now, using placeholder data
    historical_data = _get_mock_historical_data(session.user_id)
    duration_hours = int((session.scheduled_end - session.scheduled_start).seconds / 3600)

    baseline = BaselineService.calculate_10_day_average(
        historical_data=historical_data,
        session_start=session.scheduled_start,
        session_duration_hours=duration_hours
    )

    if not baseline or not BaselineService.validate_baseline(baseline):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate valid baseline"
        )

    # Update session
    session.status = "IN_PROGRESS"
    session.actual_start = datetime.utcnow()
    session.baseline_kwh = baseline
    session.baseline_calculation_method = "10_DAY_AVERAGE"

    db.commit()
    db.refresh(session)

    return session


@router.post("/{session_id}/complete", response_model=SessionResultsResponse)
async def complete_session(
    session_id: uuid.UUID,
    actual_consumption_kwh: Decimal,
    db: Session = Depends(get_db)
):
    """
    Complete a session and calculate results

    Calculates savings, credits wallet, awards points.
    """
    session = db.query(SavingSession).filter(
        SavingSession.session_id == session_id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    if session.status != "IN_PROGRESS":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot complete session with status {session.status}"
        )

    # Calculate savings
    is_double_points = session.is_double_points_day == "Y"
    savings = SavingsCalculationService.calculate_savings(
        baseline_kwh=session.baseline_kwh,
        actual_kwh=actual_consumption_kwh,
        is_double_points_day=is_double_points
    )

    # Update session
    session.status = "COMPLETED"
    session.actual_end = datetime.utcnow()
    session.actual_kwh = actual_consumption_kwh
    session.saved_kwh = savings["saved_kwh"]
    session.saved_eur = savings["saved_eur"]
    session.saved_co2_kg = savings["saved_co2_kg"]
    session.green_points_earned = savings["green_points_earned"]
    session.completed_at = datetime.utcnow()

    # Credit waste wallet
    wallet_credit = Decimal("0")
    if session.allocation_type == "WASTE_WALLET" and savings["saved_eur"] > 0:
        wallet_credit = savings["saved_eur"]
        WasteWalletService.credit_wallet(
            db=db,
            user_id=session.user_id,
            amount=wallet_credit,
            session_id=session_id,
            description=f"Savings from session {session_id}"
        )

    # Update user stats
    user = db.query(User).filter(User.user_id == session.user_id).first()
    user.green_points_balance += savings["green_points_earned"]
    user.total_kwh_saved += savings["saved_kwh"]
    user.total_eur_saved += savings["saved_eur"]
    user.total_co2_saved += savings["saved_co2_kg"]

    db.commit()
    db.refresh(session)

    # Generate congratulatory message
    if savings["saved_kwh"] > 0:
        message = f"🎉 Συγχαρητήρια! Εξοικονόμησες {savings['saved_kwh']} kWh και κέρδισες {savings['green_points_earned']} points!"
    else:
        message = "Δεν καταγράφηκε εξοικονόμηση αυτή τη φορά. Προσπάθησε ξανά!"

    return SessionResultsResponse(
        session_id=session_id,
        status="COMPLETED",
        savings=savings,
        gamification={
            "green_points": savings["green_points_earned"],
            "badges_unlocked": []  # TODO: Implement badge logic
        },
        wallet_credit=wallet_credit,
        message=message
    )


@router.get("/user/{user_id}/stats", response_model=SessionStatsResponse)
async def get_user_stats(
    user_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Get overall session statistics for user
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Count sessions
    total_sessions = db.query(SavingSession).filter(
        SavingSession.user_id == user_id
    ).count()

    completed_sessions = db.query(SavingSession).filter(
        SavingSession.user_id == user_id,
        SavingSession.status == "COMPLETED"
    ).count()

    # Calculate average
    avg_savings = Decimal("0")
    if completed_sessions > 0:
        avg_savings = user.total_kwh_saved / Decimal(str(completed_sessions))

    # TODO: Calculate current streak
    current_streak = 0

    return SessionStatsResponse(
        total_sessions=total_sessions,
        completed_sessions=completed_sessions,
        total_kwh_saved=user.total_kwh_saved,
        total_eur_saved=user.total_eur_saved,
        total_co2_saved=user.total_co2_saved,
        total_green_points=user.green_points_balance,
        average_savings_per_session=avg_savings,
        current_streak_days=current_streak
    )


def _get_mock_historical_data(user_id: uuid.UUID) -> List[dict]:
    """
    Mock historical consumption data
    In production, this would fetch from AHK API
    """
    from datetime import datetime, timedelta
    import random

    data = []
    base_date = datetime.utcnow() - timedelta(days=10)

    for day in range(10):
        for hour in range(24):
            timestamp = base_date + timedelta(days=day, hours=hour)
            # Mock consumption: higher during peak hours (17-20)
            if 17 <= hour <= 20:
                consumption = random.uniform(0.6, 1.0)  # Peak hours
            else:
                consumption = random.uniform(0.2, 0.5)  # Off-peak

            data.append({
                "timestamp": timestamp,
                "consumption_kwh": consumption
            })

    return data
