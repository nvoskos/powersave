"""
Waste Wallet API Router

Endpoints for managing Waste Wallet operations.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from ..database import get_db
from ..schemas.wallet import (
    WalletBalanceResponse,
    WalletTransactionResponse,
    CreditWalletRequest,
    DebitWalletRequest,
    DonationRequest,
    WalletCoverageResponse,
    MonthlySummaryResponse
)
from ..services.wallet import WasteWalletService
from ..services.savings import SavingsCalculationService
from ..models.user import User

router = APIRouter()


@router.get("/{user_id}/balance", response_model=WalletBalanceResponse)
async def get_wallet_balance(
    user_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Get current wallet balance for user

    Returns current balance, total earned, total spent, and stats.
    """
    wallet = WasteWalletService.get_or_create_wallet(db, user_id)
    return wallet


@router.get("/{user_id}/transactions", response_model=List[WalletTransactionResponse])
async def get_transaction_history(
    user_id: uuid.UUID,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get transaction history for user

    Paginated list of all wallet transactions.
    """
    transactions = WasteWalletService.get_transaction_history(
        db, user_id, limit=limit, offset=offset
    )
    return transactions


@router.post("/{user_id}/credit", response_model=WalletTransactionResponse)
async def credit_wallet(
    user_id: uuid.UUID,
    request: CreditWalletRequest,
    db: Session = Depends(get_db)
):
    """
    Credit wallet with savings from session

    This endpoint is typically called automatically after a successful
    saving session completes.
    """
    try:
        transaction = WasteWalletService.credit_wallet(
            db=db,
            user_id=user_id,
            amount=request.amount,
            session_id=request.session_id,
            description=request.description
        )
        return transaction
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{user_id}/debit", response_model=WalletTransactionResponse)
async def debit_wallet(
    user_id: uuid.UUID,
    request: DebitWalletRequest,
    db: Session = Depends(get_db)
):
    """
    Debit wallet (payment to municipality)

    Deducts specified amount from wallet balance.
    """
    try:
        transaction = WasteWalletService.debit_wallet(
            db=db,
            user_id=user_id,
            amount=request.amount,
            description=request.description
        )
        return transaction
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{user_id}/donate", response_model=WalletTransactionResponse)
async def donate_to_solidarity_fund(
    user_id: uuid.UUID,
    request: DonationRequest,
    db: Session = Depends(get_db)
):
    """
    Donate from wallet to Energy Solidarity Fund

    Transfer funds from personal wallet to help vulnerable households.
    """
    try:
        transaction = WasteWalletService.donate_to_solidarity_fund(
            db=db,
            user_id=user_id,
            amount=request.amount,
            recipient_fund_id=request.recipient_fund_id
        )
        return transaction
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{user_id}/coverage", response_model=WalletCoverageResponse)
async def get_waste_fee_coverage(
    user_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Calculate how much of annual waste fee is covered

    Returns coverage percentage, months covered, and remaining amount.
    """
    # Get user
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.annual_waste_fee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Annual waste fee not set for user"
        )

    # Get wallet balance
    balance = WasteWalletService.get_balance(db, user_id)

    # Calculate coverage
    coverage = SavingsCalculationService.calculate_waste_fee_coverage(
        waste_wallet_balance=balance,
        annual_waste_fee=user.annual_waste_fee
    )

    return WalletCoverageResponse(
        current_balance=balance,
        annual_waste_fee=user.annual_waste_fee,
        **coverage
    )


@router.get("/{user_id}/summary/{year}/{month}", response_model=MonthlySummaryResponse)
async def get_monthly_summary(
    user_id: uuid.UUID,
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    """
    Get monthly summary of wallet activity

    Returns credits, debits, donations, and net change for specified month.
    """
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Month must be between 1 and 12"
        )

    summary = WasteWalletService.get_monthly_summary(db, user_id, year, month)
    return summary
