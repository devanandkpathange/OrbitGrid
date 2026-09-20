"""
Configuration & Environment Settings for GridPoint.
Supports optional API keys (Google Maps, Mapbox, OpenRouteService)
with automatic fallback to ₹0 free open-source engines.
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "GridPoint — Warehouse Location Optimization Engine"
    ENVIRONMENT: str = "production"
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Optional Paid / Third-Party Map & Routing API Keys (Default: None = ₹0 Free Mode)
    GOOGLE_MAPS_API_KEY: Optional[str] = os.getenv("GOOGLE_MAPS_API_KEY", None)
    MAPBOX_ACCESS_TOKEN: Optional[str] = os.getenv("MAPBOX_ACCESS_TOKEN", None)
    OPENROUTESERVICE_API_KEY: Optional[str] = os.getenv("OPENROUTESERVICE_API_KEY", None)
    CUSTOM_LLM_URL: Optional[str] = os.getenv("CUSTOM_LLM_URL", None)

    # India Logistics Calibration Defaults
    DEFAULT_FIXED_WH_COST_INR: float = 150000.0
    DEFAULT_FREIGHT_PER_UNIT_KM_INR: float = 0.05
    INDIAN_ROAD_CIRCUITY_FACTOR: float = 1.28

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
