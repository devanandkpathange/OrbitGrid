from fastapi import APIRouter, HTTPException
from ..models.schemas import OptimizationRequest, OptimizationResponse
from ..optimization.optimizer import optimize_warehouse_network

router = APIRouter(prefix="/api", tags=["Optimization"])


@router.post("/optimize", response_model=OptimizationResponse)
async def optimize_warehouses(request: OptimizationRequest):
    """
    Core Optimization Endpoint.
    Solves warehouse placement, demand assignments, freight costs,
    and returns GeoJSON catchment zones.
    """
    try:
        demand_dict_list = [d.model_dump() for d in request.demand_points]
        constraints = request.constraints

        result = optimize_warehouse_network(
            demand_points=demand_dict_list,
            warehouse_count=request.warehouse_count,
            objective=request.objective or "minimize_delivery_cost",
            region=request.region or "Karnataka",
            capacity_limit=constraints.capacity if constraints else None,
            max_radius_km=constraints.max_radius if constraints else None,
            snap_to_industrial_hubs=constraints.snap_to_industrial_hubs if constraints else False,
            fixed_warehouse_cost_inr=constraints.fixed_warehouse_cost_inr if constraints and constraints.fixed_warehouse_cost_inr is not None else 150000.0,
            freight_rate_per_unit_km=constraints.freight_rate_per_km_unit_inr if constraints and constraints.freight_rate_per_km_unit_inr is not None else 0.05
        )
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")
