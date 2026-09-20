from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from ..models.schemas import DemandPoint, ElbowCurveResponse
from ..optimization.optimizer import compute_elbow_curve

router = APIRouter(prefix="/api", tags=["Pareto & What-If"])


class ElbowRequest(BaseModel):
    demand_points: List[DemandPoint]
    max_k: Optional[int] = 5
    region: Optional[str] = "Karnataka"


@router.post("/elbow", response_model=ElbowCurveResponse)
async def get_elbow_curve(request: ElbowRequest):
    """
    Evaluates total cost and SLA across k=1 to max_k warehouses.
    Identifies the mathematical Pareto elbow point / commercial sweet spot.
    """
    try:
        demand_dict_list = [d.model_dump() for d in request.demand_points]
        result = compute_elbow_curve(
            demand_points=demand_dict_list,
            max_k=request.max_k or 5,
            region=request.region or "Karnataka"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Elbow curve computation failed: {str(e)}")
