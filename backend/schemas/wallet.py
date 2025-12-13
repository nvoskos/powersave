"""
Pydantic schemas for Waste Wallet
"""
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional
import uuid


class WalletBalanceResponse(BaseModel):
    """Response for wallet balance"""
    user_id: uuid.UUID
    current_balance: Decimal = Field(..., description="Current wallet balance in EUR")
    total_earned: Decimal = Field(..., description="Total earned all time")
    total_spent: Decimal = Field(..., description="Total spent all time")
    sessions_contributed: int = Field(..., description="Number of sessions contributed")
    last_payment_date: Optional[datetime] = None
    last_payment_amount: Decimal = Field(default=Decimal("0"))

    class Config:
        from_attributes = True


class WalletTransactionResponse(BaseModel):
    """Response for a wallet transaction"""
    transaction_id: uuid.UUID
    user_id: uuid.UUID
    type: str = Field(..., description="Transaction type: CREDIT, DEBIT, DONATION, etc.")
    amount: Decimal
    balance_after: Decimal
    description: Optional[str] = None
    session_id: Optional[uuid.UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CreditWalletRequest(BaseModel):
    """Request to credit wallet (from savings session)"""
    user_id: uuid.UUID
    amount: Decimal = Field(..., gt=0, description="Amount to credit in EUR")
    session_id: Optional[uuid.UUID] = None
    description: str = "Savings from session"


class DebitWalletRequest(BaseModel):
    """Request to debit wallet (payment to municipality)"""
    amount: Decimal = Field(..., gt=0, description="Amount to debit in EUR")
    description: str = "Payment to municipality"


class DonationRequest(BaseModel):
    """Request to donate from wallet to solidarity fund"""
    amount: Decimal = Field(..., gt=0, description="Amount to donate in EUR")
    recipient_fund_id: uuid.UUID


class WalletCoverageResponse(BaseModel):
    """Response showing waste fee coverage"""
    current_balance: Decimal
    annual_waste_fee: Decimal
    coverage_percentage: Decimal = Field(..., description="Percentage of annual fee covered")
    months_covered: Decimal = Field(..., description="Number of months covered")
    remaining_to_cover: Decimal = Field(..., description="Remaining amount needed to cover full year")


class MonthlySummaryResponse(BaseModel):
    """Monthly wallet activity summary"""
    year: int
    month: int
    total_credits: Decimal
    total_debits: Decimal
    total_donations: Decimal
    net_change: Decimal
    transaction_count: int
