"""
Wallet models for Waste Fee Offset
"""
from sqlalchemy import Column, String, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..database import Base


class WasteWallet(Base):
    """
    Waste Wallet - tracks accumulated savings for waste fee payment
    """
    __tablename__ = "waste_wallet"

    wallet_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, unique=True)

    # Balance
    current_balance = Column(DECIMAL(10, 2), default=0)
    total_earned = Column(DECIMAL(10, 2), default=0)
    total_spent = Column(DECIMAL(10, 2), default=0)

    # Stats
    sessions_contributed = Column(String(50), default=0)
    last_payment_date = Column(TIMESTAMP, nullable=True)
    last_payment_amount = Column(DECIMAL(10, 2), default=0)

    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User")


class WalletTransaction(Base):
    """
    Transaction history for Waste Wallet
    """
    __tablename__ = "wallet_transaction"

    transaction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, index=True)

    # Transaction Type: CREDIT, DEBIT, DONATION, PAYMENT_TO_MUNICIPALITY
    type = Column(String(30), nullable=False)

    # Amount
    amount = Column(DECIMAL(10, 2), nullable=False)
    balance_after = Column(DECIMAL(10, 2), nullable=False)

    # Description
    description = Column(String(500))

    # Reference
    session_id = Column(UUID(as_uuid=True), ForeignKey("saving_session.session_id"), nullable=True)
    donation_recipient_id = Column(UUID(as_uuid=True), nullable=True)

    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="wallet_transactions")
    session = relationship("SavingSession")

    def __repr__(self):
        return f"<WalletTransaction {self.type} - €{self.amount}>"
