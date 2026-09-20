"""
Indian Logistics Cost & Carbon Footprint Engine.
Calibrated for Indian freight market rates (INR / ₹), warehouse rental tariffs,
and BS-VI commercial truck emission standards.
"""

from typing import Dict, Any

# Indian Logistics Economics Constants
DEFAULT_FIXED_WH_COST_INR = 150000.0   # Monthly baseline rent + warehouse overhead
DEFAULT_UNIT_HANDLING_INR = 2.50        # Per-unit pick/pack & sorting in INR
DEFAULT_FREIGHT_PER_UNIT_KM_INR = 0.05  # Transport freight rate per unit per km in INR
MIN_SHIPMENT_DISPATCH_INR = 150.0       # Base consignment dispatch fee

# Green Logistics Constants (India BS-VI Heavy & Medium Commercial Vehicles)
DIESEL_CONSUMPTION_LITRE_PER_KM = 0.24  # ~4.16 km per litre of diesel for commercial trucks
CO2_KG_PER_LITRE_DIESEL = 2.68          # BEE / GHG protocol emission factor for diesel


def calculate_delivery_cost_inr(
    demand_volume: float, 
    distance_km: float, 
    freight_rate_per_unit_km: float = DEFAULT_FREIGHT_PER_UNIT_KM_INR
) -> float:
    """
    Computes delivery transport cost for a demand assignment in Indian Rupees (₹).
    Cost = Fixed Dispatch Base + (Demand Volume * Distance * Freight Rate) + Handling.
    """
    if demand_volume <= 0:
        return 0.0

    transport_cost = demand_volume * distance_km * freight_rate_per_unit_km
    dispatch_cost = MIN_SHIPMENT_DISPATCH_INR
    handling_cost = demand_volume * DEFAULT_UNIT_HANDLING_INR

    total = transport_cost + dispatch_cost + handling_cost
    return round(total, 2)


def calculate_green_logistics_metrics(total_distance_weighted_km: float) -> Dict[str, float]:
    """
    Computes environmental ESG metrics for freight transport.
    Estimates diesel consumption in litres and CO2 emissions in kg.
    """
    # Equivalent commercial truck-km based on volume consolidation (approx 500 units per truckload)
    truck_km = total_distance_weighted_km / 500.0 if total_distance_weighted_km > 0 else 0.0
    diesel_litres = truck_km * DIESEL_CONSUMPTION_LITRE_PER_KM
    co2_kg = diesel_litres * CO2_KG_PER_LITRE_DIESEL

    return {
        "diesel_litres": round(diesel_litres, 2),
        "co2_emissions_kg": round(co2_kg, 2)
    }
