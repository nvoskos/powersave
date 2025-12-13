"""
PowerSave FastAPI Application

Main entry point for the PowerSave backend API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .config import get_settings
from .database import init_db
from .routers import waste_wallet, sessions, auth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="PowerSave - National Energy Solidarity Ecosystem API"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(waste_wallet.router, prefix="/api/v1/wallet", tags=["Waste Wallet"])
app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["Saving Sessions"])


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("Starting PowerSave API...")
    init_db()
    logger.info("Database initialized")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected"  # Add actual DB check in production
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
