"""
Authentication API Router

Basic authentication endpoints (placeholder for full implementation).
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..schemas.user import UserCreateRequest, UserResponse, PropertyRegistrationRequest, PropertyRegistrationResponse
from ..models.user import User
from ..models.municipality import Municipality
from ..services.municipality import MunicipalityIntegrationService

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    request: UserCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user

    Creates a new user account with AHK account number and email.
    """
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.ahk_account_number == request.ahk_account_number) |
        (User.email == request.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this AHK account or email already exists"
        )

    # Get municipality
    municipality = None
    if request.municipality_name:
        municipality = db.query(Municipality).filter(
            Municipality.name == request.municipality_name
        ).first()

    # Create user (password should be hashed in production)
    new_user = User(
        ahk_account_number=request.ahk_account_number,
        email=request.email,
        password_hash=request.password,  # TODO: Hash password properly
        first_name=request.first_name,
        last_name=request.last_name,
        phone=request.phone,
        property_number=request.property_number,
        municipality_id=municipality.municipality_id if municipality else None
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/register-property", response_model=PropertyRegistrationResponse)
async def register_property(
    request: PropertyRegistrationRequest,
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Register property for Waste Fee Offset

    Verifies property with municipality and sets annual waste fee.
    """
    # Validate property number format
    if not MunicipalityIntegrationService.validate_property_number(request.property_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid property number format"
        )

    # Get user
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Verify property with municipality
    municipality_service = MunicipalityIntegrationService()
    property_info = await municipality_service.verify_property(
        property_number=request.property_number,
        municipality_name=request.municipality_name
    )

    if not property_info or not property_info.get("is_valid"):
        return PropertyRegistrationResponse(
            success=False,
            property_number=request.property_number,
            message="Property not found or invalid"
        )

    # Update user with property info
    user.property_number = request.property_number
    user.property_address = property_info.get("address")
    user.annual_waste_fee = property_info.get("annual_waste_fee")

    # Register with municipality for auto-payment
    await municipality_service.register_powersave_user(
        property_number=request.property_number,
        ahk_account_number=user.ahk_account_number,
        user_email=user.email
    )

    db.commit()
    db.refresh(user)

    return PropertyRegistrationResponse(
        success=True,
        property_number=request.property_number,
        address=property_info.get("address"),
        annual_waste_fee=property_info.get("annual_waste_fee"),
        message="Property successfully registered for Waste Fee Offset"
    )


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get user details
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user
