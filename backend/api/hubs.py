from fastapi import APIRouter, Query
from typing import List, Optional, Dict, Any
from ..models.india_hubs import INDIA_INDUSTRIAL_HUBS

router = APIRouter(prefix="/api", tags=["Indian Logistics Hubs"])


@router.get("/hubs", response_model=List[Dict[str, Any]])
async def get_indian_industrial_hubs(state: Optional[str] = Query(None, description="Filter by Indian state")):
    """
    Returns verified Indian logistics, warehousing, and industrial parks (KIADB, MIDC, etc.)
    with geo-coordinates and typical rental rates in ₹/sqft.
    """
    if state:
        filtered = [h for h in INDIA_INDUSTRIAL_HUBS if h["state"].lower() == state.lower()]
        return filtered
    return INDIA_INDUSTRIAL_HUBS
