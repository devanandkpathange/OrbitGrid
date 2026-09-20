from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from ..optimization.feasibility import generate_location_feasibility_report
from ..models.industry_knowledge import INDUSTRY_PROFILES, get_industry_recommendations
from ..services.nlp_classifier import analyze_user_business

router = APIRouter(prefix="/api", tags=["Feasibility & Intelligence"])


class BusinessAnalysisRequest(BaseModel):
    business_description: str


@router.post("/analyze-business")
async def analyze_business(request: BusinessAnalysisRequest):
    """
    NLP & Semantic Business Profiler.
    Accepts ANY free-text business description and returns
    tailored supply chain siting criteria and recommended Indian corridors.
    """
    return analyze_user_business(request.business_description)


class FeasibilityRequest(BaseModel):
    candidate_city: str
    candidate_lat: float
    candidate_lng: float
    demand_points: List[Dict[str, Any]]
    industry: Optional[str] = "sugar_agro"
    existing_warehouses: Optional[List[Dict[str, Any]]] = None


@router.post("/feasibility")
async def get_feasibility_report(request: FeasibilityRequest):
    """
    Generates an in-depth viability & ROI report for placing a warehouse
    at a specific candidate location (e.g. Mandya, Belagavi, Nelamangala).
    """
    try:
        report = generate_location_feasibility_report(
            candidate_city=request.candidate_city,
            candidate_lat=request.candidate_lat,
            candidate_lng=request.candidate_lng,
            demand_points=request.demand_points,
            industry=request.industry or "sugar_agro",
            existing_warehouses=request.existing_warehouses
        )
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feasibility analysis failed: {str(e)}")


@router.get("/industry-suggestions")
async def get_industry_suggestions(industry: str = Query("sugar_agro", description="e.g. sugar_agro, ecommerce_retail, cold_chain_pharma")):
    """
    Returns curated raw-material belts and sourcing zones for an industry in India.
    """
    return get_industry_recommendations(industry)


@router.get("/industries")
async def list_available_industries():
    """
    Lists all supported industry supply-chain profiles.
    """
    return [
        {"key": k, "name": v["name"], "description": v["description"]}
        for k, v in INDUSTRY_PROFILES.items()
    ]
