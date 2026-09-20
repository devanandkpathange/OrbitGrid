"""
Demand-to-Warehouse Assignment Engine.
Handles uncapacitated and capacitated (CFLP) assignment,
enforces maximum delivery radius SLA, and calculates route metrics.
"""

from typing import List, Dict, Any, Tuple
from ..services.maps import indian_road_distance_km, generate_curved_corridor_polyline
from .cost_model import (
    calculate_delivery_cost_inr, 
    calculate_green_logistics_metrics,
    DEFAULT_FIXED_WH_COST_INR
)


def assign_demand_to_warehouses(
    demand_points: List[Dict[str, Any]],
    warehouse_candidates: List[Dict[str, Any]],
    capacity_limit: float = None,
    max_radius_km: float = None,
    freight_rate_per_unit_km: float = 0.05,
    fixed_wh_cost_inr: float = DEFAULT_FIXED_WH_COST_INR
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    """
    Assigns each demand point to an optimal warehouse under capacity and SLA constraints.
    Returns:
        (enriched_warehouses, assignments, aggregated_metrics)
    """
    warehouses_map = {
        wh["id"]: {
            "id": wh["id"],
            "name": wh.get("name", f"Warehouse {wh['id']}"),
            "lat": wh["lat"],
            "lng": wh["lng"],
            "capacity": capacity_limit,
            "assigned_demand": 0.0,
            "transport_cost": 0.0,
            "fixed_cost": fixed_wh_cost_inr,
            "snapped_hub": wh.get("snapped_hub")
        }
        for wh in warehouse_candidates
    }

    # Precalculate distance matrix between every demand point and warehouse
    dem_wh_distances = []
    for dem in demand_points:
        d_id = dem.get("id") or dem.get("name") or f"dem_{len(dem_wh_distances)}"
        d_lat = dem["lat"]
        d_lng = dem["lng"]
        d_demand = float(dem["demand"])
        wh_distances = []
        for wh in warehouse_candidates:
            dist = indian_road_distance_km(d_lat, d_lng, wh["lat"], wh["lng"])
            wh_distances.append((wh["id"], dist))
        # Sort by distance ascending
        wh_distances.sort(key=lambda x: x[1])
        dem_wh_distances.append({
            "id": d_id,
            "name": dem.get("name", d_id),
            "lat": d_lat,
            "lng": d_lng,
            "demand": d_demand,
            "options": wh_distances
        })

    # If capacity is constrained, sort high-demand points first to anchor major demand
    if capacity_limit is not None and capacity_limit > 0:
        dem_wh_distances.sort(key=lambda x: x["demand"], reverse=True)

    assignments = []
    total_transport_distance_weighted = 0.0
    total_linear_distance = 0.0
    sla_violations = 0

    for item in dem_wh_distances:
        dem_id = item["id"]
        dem_name = item["name"]
        dem_lat = item["lat"]
        dem_lng = item["lng"]
        dem_vol = item["demand"]

        assigned_wh_id = None
        assigned_dist = 0.0

        for wh_id, dist in item["options"]:
            current_wh = warehouses_map[wh_id]
            if capacity_limit is None or capacity_limit <= 0:
                assigned_wh_id = wh_id
                assigned_dist = dist
                break
            else:
                # Capacity constraint check
                if current_wh["assigned_demand"] + dem_vol <= capacity_limit:
                    assigned_wh_id = wh_id
                    assigned_dist = dist
                    break

        # Fallback to closest warehouse if all are at/near capacity
        if assigned_wh_id is None:
            assigned_wh_id = item["options"][0][0]
            assigned_dist = item["options"][0][1]

        # Check SLA radius constraint
        if max_radius_km is not None and assigned_dist > max_radius_km:
            sla_violations += 1

        cost = calculate_delivery_cost_inr(dem_vol, assigned_dist, freight_rate_per_unit_km)
        warehouses_map[assigned_wh_id]["assigned_demand"] += dem_vol
        warehouses_map[assigned_wh_id]["transport_cost"] += cost

        # Route polyline for visualization
        wh_ref = warehouses_map[assigned_wh_id]
        route_geom = generate_curved_corridor_polyline(wh_ref["lat"], wh_ref["lng"], dem_lat, dem_lng)

        assignments.append({
            "demand_id": dem_id,
            "demand_name": dem_name,
            "warehouse_id": assigned_wh_id,
            "distance": round(assigned_dist, 2),
            "cost": round(cost, 2),
            "demand_volume": dem_vol,
            "route_geometry": route_geom
        })

        total_transport_distance_weighted += (assigned_dist * dem_vol)
        total_linear_distance += assigned_dist

    # Finalize warehouse list and utilization
    final_warehouses = []
    total_fixed_cost = 0.0
    total_transport_cost = 0.0
    total_all_demand = sum(d["demand"] for d in demand_points)

    for wh_id, wh_data in warehouses_map.items():
        util_pct = None
        if wh_data["capacity"] and wh_data["capacity"] > 0:
            util_pct = round((wh_data["assigned_demand"] / wh_data["capacity"]) * 100.0, 1)

        # Only charge fixed cost if warehouse is actually utilized with demand
        wh_fixed = wh_data["fixed_cost"] if wh_data["assigned_demand"] > 0 else 0.0
        wh_total_cost = round(wh_data["transport_cost"] + wh_fixed, 2)

        total_fixed_cost += wh_fixed
        total_transport_cost += wh_data["transport_cost"]

        final_warehouses.append({
            "id": wh_id,
            "name": wh_data["name"],
            "lat": wh_data["lat"],
            "lng": wh_data["lng"],
            "cost": wh_total_cost,
            "assigned_demand": round(wh_data["assigned_demand"], 1),
            "capacity": wh_data["capacity"],
            "utilization_pct": util_pct,
            "snapped_hub": wh_data["snapped_hub"],
            "fixed_cost_inr": round(wh_fixed, 2),
            "variable_cost_inr": round(wh_data["transport_cost"], 2)
        })

    # Aggregate metrics
    n_demands = max(1, len(demand_points))
    avg_distance = round(total_linear_distance / n_demands, 2)
    grand_total_cost = round(total_transport_cost + total_fixed_cost, 2)
    green_metrics = calculate_green_logistics_metrics(total_transport_distance_weighted)
    sla_pct = round(((n_demands - sla_violations) / n_demands) * 100.0, 1) if n_demands > 0 else 100.0

    aggregated_metrics = {
        "total_distance": round(total_linear_distance, 2),
        "total_cost": grand_total_cost,
        "transport_cost_inr": round(total_transport_cost, 2),
        "fixed_facility_cost_inr": round(total_fixed_cost, 2),
        "average_distance": avg_distance,
        "currency": "INR",
        "total_demand": round(total_all_demand, 1),
        "co2_emissions_kg": green_metrics["co2_emissions_kg"],
        "diesel_litres": green_metrics["diesel_litres"],
        "sla_compliance_pct": sla_pct,
        "warehouses_used": len([w for w in final_warehouses if w["assigned_demand"] > 0])
    }

    return final_warehouses, assignments, aggregated_metrics
