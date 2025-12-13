"""
Waste Wallet Service

Manages Waste Wallet balance, transactions, and payments
"""
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime
from typing import Optional, List
import uuid

from ..models.wallet import WasteWallet, WalletTransaction
from ..models.user import User


class WasteWalletService:
    """
    Service for managing Waste Wallet operations
    """

    @staticmethod
    def get_or_create_wallet(db: Session, user_id: uuid.UUID) -> WasteWallet:
        """
        Get existing wallet or create new one for user

        Args:
            db: Database session
            user_id: User UUID

        Returns:
            WasteWallet instance
        """
        wallet = db.query(WasteWallet).filter(WasteWallet.user_id == user_id).first()

        if not wallet:
            wallet = WasteWallet(
                user_id=user_id,
                current_balance=Decimal("0"),
                total_earned=Decimal("0"),
                total_spent=Decimal("0"),
                sessions_contributed=0
            )
            db.add(wallet)
            db.commit()
            db.refresh(wallet)

        return wallet

    @staticmethod
    def credit_wallet(
        db: Session,
        user_id: uuid.UUID,
        amount: Decimal,
        session_id: Optional[uuid.UUID] = None,
        description: str = "Savings from session"
    ) -> WalletTransaction:
        """
        Credit amount to waste wallet

        Args:
            db: Database session
            user_id: User UUID
            amount: Amount to credit
            session_id: Reference to saving session
            description: Transaction description

        Returns:
            Created transaction
        """
        if amount <= 0:
            raise ValueError("Credit amount must be positive")

        # Get wallet
        wallet = WasteWalletService.get_or_create_wallet(db, user_id)

        # Update balance
        wallet.current_balance += amount
        wallet.total_earned += amount
        if session_id:
            wallet.sessions_contributed += 1

        # Create transaction
        transaction = WalletTransaction(
            user_id=user_id,
            type="CREDIT",
            amount=amount,
            balance_after=wallet.current_balance,
            description=description,
            session_id=session_id
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction

    @staticmethod
    def debit_wallet(
        db: Session,
        user_id: uuid.UUID,
        amount: Decimal,
        description: str = "Payment to municipality"
    ) -> WalletTransaction:
        """
        Debit amount from waste wallet

        Args:
            db: Database session
            user_id: User UUID
            amount: Amount to debit
            description: Transaction description

        Returns:
            Created transaction

        Raises:
            ValueError: If insufficient balance
        """
        if amount <= 0:
            raise ValueError("Debit amount must be positive")

        # Get wallet
        wallet = WasteWalletService.get_or_create_wallet(db, user_id)

        # Check balance
        if wallet.current_balance < amount:
            raise ValueError(
                f"Insufficient balance. Available: €{wallet.current_balance}, Required: €{amount}"
            )

        # Update balance
        wallet.current_balance -= amount
        wallet.total_spent += amount
        wallet.last_payment_date = datetime.utcnow()
        wallet.last_payment_amount = amount

        # Create transaction
        transaction = WalletTransaction(
            user_id=user_id,
            type="PAYMENT_TO_MUNICIPALITY",
            amount=amount,
            balance_after=wallet.current_balance,
            description=description
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction

    @staticmethod
    def donate_to_solidarity_fund(
        db: Session,
        user_id: uuid.UUID,
        amount: Decimal,
        recipient_fund_id: uuid.UUID
    ) -> WalletTransaction:
        """
        Donate amount from wallet to Social Energy Fund

        Args:
            db: Database session
            user_id: User UUID
            amount: Amount to donate
            recipient_fund_id: Social Energy Fund UUID

        Returns:
            Created transaction

        Raises:
            ValueError: If insufficient balance
        """
        if amount <= 0:
            raise ValueError("Donation amount must be positive")

        # Get wallet
        wallet = WasteWalletService.get_or_create_wallet(db, user_id)

        # Check balance
        if wallet.current_balance < amount:
            raise ValueError(f"Insufficient balance for donation")

        # Update balance
        wallet.current_balance -= amount
        wallet.total_spent += amount

        # Create transaction
        transaction = WalletTransaction(
            user_id=user_id,
            type="DONATION",
            amount=amount,
            balance_after=wallet.current_balance,
            description=f"Donation to Energy Solidarity Fund",
            donation_recipient_id=recipient_fund_id
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction

    @staticmethod
    def get_balance(db: Session, user_id: uuid.UUID) -> Decimal:
        """
        Get current wallet balance

        Args:
            db: Database session
            user_id: User UUID

        Returns:
            Current balance
        """
        wallet = WasteWalletService.get_or_create_wallet(db, user_id)
        return wallet.current_balance

    @staticmethod
    def get_transaction_history(
        db: Session,
        user_id: uuid.UUID,
        limit: int = 50,
        offset: int = 0
    ) -> List[WalletTransaction]:
        """
        Get transaction history for user

        Args:
            db: Database session
            user_id: User UUID
            limit: Max number of transactions
            offset: Pagination offset

        Returns:
            List of transactions
        """
        transactions = (
            db.query(WalletTransaction)
            .filter(WalletTransaction.user_id == user_id)
            .order_by(WalletTransaction.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        return transactions

    @staticmethod
    def get_monthly_summary(
        db: Session,
        user_id: uuid.UUID,
        year: int,
        month: int
    ) -> dict:
        """
        Get monthly summary of wallet activity

        Args:
            db: Database session
            user_id: User UUID
            year: Year
            month: Month (1-12)

        Returns:
            Dictionary with monthly stats
        """
        from sqlalchemy import extract, func

        # Get transactions for the month
        transactions = (
            db.query(WalletTransaction)
            .filter(
                WalletTransaction.user_id == user_id,
                extract('year', WalletTransaction.created_at) == year,
                extract('month', WalletTransaction.created_at) == month
            )
            .all()
        )

        # Calculate totals
        total_credits = sum(
            t.amount for t in transactions if t.type == "CREDIT"
        )
        total_debits = sum(
            t.amount for t in transactions if t.type in ["PAYMENT_TO_MUNICIPALITY", "DEBIT"]
        )
        total_donations = sum(
            t.amount for t in transactions if t.type == "DONATION"
        )

        return {
            "year": year,
            "month": month,
            "total_credits": total_credits,
            "total_debits": total_debits,
            "total_donations": total_donations,
            "net_change": total_credits - total_debits - total_donations,
            "transaction_count": len(transactions)
        }
