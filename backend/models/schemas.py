from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DemandPoint(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    lat: float = Field(..., description="Latitude coordinate", ge=-90, le=90)
    lng: float = Field(..., description="Longitude coordinate", ge=-180, le=180)
    demand: float = Field(..., description="Demand volume or order count", ge=0)


class Constraints(BaseModel):
    capacity: Optional[float] = Field(None, description="Maximum capacity per warehouse (units/orders)")
    max_radius: Optional[float] = Field(None, description="Maximum delivery radius in km")
    snap_to_industrial_hubs: Optional[bool] = Field(
        False, 
        description="Snap continuous centroids to real Indian industrial & logistics warehousing parks"
    )
    fixed_warehouse_cost_inr: Optional[float] = Field(
        150000.0, 
        description="Estimated monthly fixed operational & rental cost per warehouse in ₹ (INR)"
    )
    freight_rate_per_km_unit_inr: Optional[float] = Field(
        0.05, 
        description="Transportation freight cost per unit-km in ₹ (INR)"
    )


class OptimizationRequest(BaseModel):
    demand_points: List[DemandPoint] = Field(..., min_length=1)
    warehouse_count: int = Field(2, ge=1, description="Number of warehouses to optimize")
    objective: Optional[str] = Field("minimize_delivery_cost", description="Optimization objective")
    region: Optional[str] = Field("Karnataka", description="Operating geographic region in India")
    business_type: Optional[str] = Field("retail", description="Industry or product sector")
    constraints: Optional[Constraints] = Field(default_factory=Constraints)


class Warehouse(BaseModel):
    id: str
    name: Optional[str] = None
    lat: float
    lng: float
    cost: float = Field(..., description="Total cost associated with this warehouse in ₹ (INR)")
    assigned_demand: float = 0.0
    capacity: Optional[float] = None
    utilization_pct: Optional[float] = None
    snapped_hub: Optional[Dict[str, Any]] = None
    fixed_cost_inr: Optional[float] = None
    variable_cost_inr: Optional[float] = None
    reasoning: Optional[str] = Field(None, description="Detailed supply chain & geographical siting reasoning")
    served_cities: Optional[List[str]] = Field(default_factory=list, description="Names of cities served by this facility")
    average_dispatch_distance_km: Optional[float] = Field(None, description="Average dispatch distance to assigned customers")


class Assignment(BaseModel):
    demand_id: str
    demand_name: Optional[str] = None
    warehouse_id: str
    distance: float = Field(..., description="Distance in km (accounting for Indian road circuity)")
    cost: float = Field(..., description="Delivery cost in ₹ (INR)")
    demand_volume: float = 0.0
    route_geometry: Optional[List[List[float]]] = Field(
        None, 
        description="List of [lat, lng] polyline points for map visualization"
    )


class OptimizationMetrics(BaseModel):
    total_distance: float
    total_cost: float
    average_distance: float
    currency: str = "INR"
    total_demand: float
    co2_emissions_kg: float
    diesel_litres: float
    sla_compliance_pct: float
    warehouses_used: int


class OptimizationResponse(BaseModel):
    warehouses: List[Warehouse]
    assignments: List[Assignment]
    metrics: OptimizationMetrics
    total_cost: float
    geojson_catchment: Optional[Dict[str, Any]] = Field(
        None, 
        description="GeoJSON FeatureCollection representing warehouse service zones"
    )


class BenchmarkComparison(BaseModel):
    baseline_type: str = "Single Central Legacy Hub (Bengaluru / Central)"
    metric: str
    before_value: float
    after_value: float
    unit: str
    percentage_change: float
    interpretation: str


class BenchmarkResponse(BaseModel):
    before: Dict[str, Any]
    after: Dict[str, Any]
    comparisons: List[BenchmarkComparison]
    summary: str


class ElbowCurvePoint(BaseModel):
    warehouse_count: int
    total_cost_inr: float
    transport_cost_inr: float
    fixed_facility_cost_inr: float
    average_distance_km: float
    co2_emissions_kg: float
    is_recommended: bool = False
    recommendation_reason: Optional[str] = None


class ElbowCurveResponse(BaseModel):
    region: str
    recommended_k: int
    points: List[ElbowCurvePoint]
    executive_summary: str
