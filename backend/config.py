"""
Configuration settings for PowerSave Backend
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "PowerSave API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://powersave:powersave@localhost:5432/powersave"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT Authentication
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Energy Pricing (Cyprus EAC rates)
    KWH_TO_EUR_RATE: float = 0.30  # €0.30 per kWh
    CO2_EMISSION_FACTOR: float = 0.7  # kg CO2 per kWh

    # Gamification
    GREEN_POINTS_PER_KWH: int = 10  # 10 points per kWh saved
    BONUS_MULTIPLIER_DOUBLE_DAYS: float = 2.0

    # Session Settings
    SESSION_DURATION_HOURS: int = 3  # Default session duration
    BASELINE_CALCULATION_DAYS: int = 10  # Days for baseline average
    PEAK_HOURS_START: int = 17  # 17:00
    PEAK_HOURS_END: int = 20  # 20:00

    # Municipality Integration
    MUNICIPALITY_API_BASE_URL: str = "http://localhost:8001/api"
    MUNICIPALITY_API_KEY: str = "municipality-api-key"

    # Smart Meter Integration (AHK/EAC)
    AHK_API_BASE_URL: str = "http://localhost:8002/api"
    AHK_API_KEY: str = "ahk-api-key"

    # Notifications
    ENABLE_PUSH_NOTIFICATIONS: bool = True
    FIREBASE_CREDENTIALS_PATH: str = "./firebase-credentials.json"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
