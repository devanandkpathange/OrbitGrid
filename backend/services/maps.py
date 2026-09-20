"""
Zero-Cost Indian Logistics Maps & Routing Service.
Computes realistic road distances, travel times, and route geometries
without requiring paid Google Maps or Mapbox API keys (₹0 cost).
"""

import math
from typing import List, Tuple, Dict, Any, Optional
import httpx

# Empirical Indian highway circuity multiplier (NH/SH average vs straight line)
INDIAN_ROAD_CIRCUITY_FACTOR = 1.28

# Commercial freight truck average operating speed in India (km/h)
INDIAN_FREIGHT_AVG_SPEED_KMH = 42.0


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes great-circle distance between two geographic coordinates in kilometers.
    """
    R = 6371.0  # Earth's mean radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c


def indian_road_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates estimated actual road distance across the Indian highway network
    by applying the empirically calibrated Indian road circuity factor.
    """
    haversine = haversine_distance_km(lat1, lon1, lat2, lon2)
    return round(haversine * INDIAN_ROAD_CIRCUITY_FACTOR, 2)


def estimate_transit_time_hours(distance_km: float) -> float:
    """
    Estimates commercial freight vehicle transit time in hours across Indian corridors.
    """
    # 42 km/h highway speed + 0.5 hr terminal dispatch/checkpoint allowance
    if distance_km <= 0.1:
        return 0.1
    transit_hours = (distance_km / INDIAN_FREIGHT_AVG_SPEED_KMH) + 0.5
    return round(transit_hours, 2)


def generate_curved_corridor_polyline(
    lat1: float, 
    lon1: float, 
    lat2: float, 
    lon2: float, 
    num_intermediate_points: int = 5
) -> List[List[float]]:
    """
    Generates realistic road-like waypoint geometry between warehouse and demand point
    with subtle corridor curve, suitable for Leaflet polyline rendering.
    """
    points = [[lat1, lon1]]
    if lat1 == lat2 and lon1 == lon2:
        return points

    # Perpendicular displacement vector to simulate natural highway curve
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    dist = math.sqrt(dlat**2 + dlon**2)
    if dist > 0:
        perp_lat = -dlon / dist
        perp_lon = dlat / dist
    else:
        perp_lat, perp_lon = 0, 0

    curve_amplitude = min(0.04, dist * 0.08)

    for i in range(1, num_intermediate_points):
        t = i / float(num_intermediate_points)
        # Parabolic deflection
        deflection = math.sin(t * math.pi) * curve_amplitude
        mid_lat = lat1 + t * dlat + deflection * perp_lat
        mid_lon = lon1 + t * dlon + deflection * perp_lon
        points.append([round(mid_lat, 5), round(mid_lon, 5)])

    points.append([lat2, lon2])
    return points


async def fetch_osrm_route(
    lat1: float, 
    lon1: float, 
    lat2: float, 
    lon2: float, 
    timeout_secs: float = 1.0
) -> Tuple[float, List[List[float]]]:
    """
    Attempts to query OpenStreetMap's free OSRM routing server.
    If server is slow, unreachable, or offline, seamlessly falls back
    to the calibrated Indian road distance model.
    """
    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=simplified&geometries=geojson"
    try:
        async with httpx.AsyncClient(timeout=timeout_secs) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                if "routes" in data and len(data["routes"]) > 0:
                    route = data["routes"][0]
                    dist_km = round(route["distance"] / 1000.0, 2)
                    # OSRM geojson coordinates are [lon, lat], convert to [lat, lon] for Leaflet
                    raw_coords = route["geometry"]["coordinates"]
                    leaflet_coords = [[pt[1], pt[0]] for pt in raw_coords]
                    return dist_km, leaflet_coords
    except Exception:
        pass

    # Seamless zero-latency fallback
    fallback_dist = indian_road_distance_km(lat1, lon1, lat2, lon2)
    fallback_geom = generate_curved_corridor_polyline(lat1, lon1, lat2, lon2)
    return fallback_dist, fallback_geom


def compute_distance_matrix(
    origin_coords: List[Tuple[float, float]], 
    dest_coords: List[Tuple[float, float]]
) -> List[List[float]]:
    """
    Computes an N x M distance matrix (in km) using Indian road circuity.
    Fast, vectorized-friendly, pure Python with no external dependencies.
    """
    matrix = []
    for o_lat, o_lng in origin_coords:
        row = []
        for d_lat, d_lng in dest_coords:
            dist = indian_road_distance_km(o_lat, o_lng, d_lat, d_lng)
            row.append(dist)
        matrix.append(row)
    return matrix
