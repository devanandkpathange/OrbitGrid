from fastapi import APIRouter, HTTPException
from ..models.schemas import OptimizationRequest, BenchmarkResponse
from ..optimization.optimizer import optimize_warehouse_network, compute_baseline_benchmark

router = APIRouter(prefix="/api", tags=["Benchmark"])


@router.post("/benchmark", response_model=BenchmarkResponse)
async def get_benchmark_comparison(request: OptimizationRequest):
    """
    Computes Before vs After comparison between a single central legacy hub
    and the optimized distributed warehouse network.
    """
    try:
        demand_dict_list = [d.model_dump() for d in request.demand_points]
        constraints = request.constraints

        opt_result = optimize_warehouse_network(
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

        benchmark = compute_baseline_benchmark(
            demand_points=demand_dict_list,
            optimized_result=opt_result,
            region=request.region or "Karnataka"
        )
        return benchmark
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Benchmark calculation failed: {str(e)}")
