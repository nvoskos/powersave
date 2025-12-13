"""
Pydantic schemas for User
"""
from pydantic import BaseModel, EmailStr, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional
import uuid


class UserCreateRequest(BaseModel):
    """Request to create a new user"""
    ahk_account_number: str = Field(..., min_length=5, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str
    phone: Optional[str] = None
    property_number: Optional[str] = None
    municipality_name: Optional[str] = None


class UserResponse(BaseModel):
    """Response for user data"""
    user_id: uuid.UUID
    ahk_account_number: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    property_number: Optional[str] = None
    property_address: Optional[str] = None
    green_points_balance: int
    total_kwh_saved: Decimal
    total_eur_saved: Decimal
    total_co2_saved: Decimal
    waste_wallet_balance: Decimal
    annual_waste_fee: Optional[Decimal] = None
    is_vulnerable_household: bool
    created_at: datetime

    class Config:
        from_attributes = True


class PropertyRegistrationRequest(BaseModel):
    """Request to register property for waste fee offset"""
    property_number: str = Field(..., description="Αριθμός Υποστατικού")
    municipality_name: str


class PropertyRegistrationResponse(BaseModel):
    """Response after property registration"""
    success: bool
    property_number: str
    address: Optional[str] = None
    annual_waste_fee: Optional[Decimal] = None
    message: str
