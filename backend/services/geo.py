"""
Geographic catchment and spatial polygon service.
Generates GeoJSON FeatureCollection containing warehouse service polygons
and convex boundaries for Leaflet interactive rendering.
"""

from typing import List, Dict, Any, Tuple
import math


def compute_convex_hull(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    Computes 2D convex hull of coordinates using Monotone Chain algorithm.
    Points are (lat, lng).
    """
    pts = sorted(list(set(points)))
    if len(pts) <= 2:
        return pts

    def cross_product(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]


def expand_polygon_buffer(coords: List[Tuple[float, float]], buffer_deg: float = 0.15) -> List[List[float]]:
    """
    Adds a subtle buffer padding around points and closes the polygon loop for GeoJSON.
    GeoJSON coordinates format: [lng, lat].
    """
    if not coords:
        return []

    if len(coords) == 1:
        # Generate small circular polygon around single point
        lat, lng = coords[0]
        circle = []
        for step in range(16):
            angle = 2 * math.pi * (step / 16)
            p_lat = lat + buffer_deg * math.sin(angle)
            p_lng = lng + buffer_deg * math.cos(angle) * 1.1
            circle.append([round(p_lng, 5), round(p_lat, 5)])
        circle.append(circle[0])
        return circle

    if len(coords) == 2:
        # Expand 2 points into an oriented pill polygon
        p1, p2 = coords[0], coords[1]
        lat_diff = p2[0] - p1[0]
        lng_diff = p2[1] - p1[1]
        length = math.sqrt(lat_diff**2 + lng_diff**2) or 1.0
        n_lat = -lng_diff / length * buffer_deg
        n_lng = lat_diff / length * buffer_deg

        poly = [
            [p1[1] - n_lng, p1[0] - n_lat],
            [p2[1] - n_lng, p2[0] - n_lat],
            [p2[1] + n_lng, p2[0] + n_lat],
            [p1[1] + n_lng, p1[0] + n_lat],
            [p1[1] - n_lng, p1[0] - n_lat]
        ]
        return [[round(pt[0], 5), round(pt[1], 5)] for pt in poly]

    # Standard hull
    hull = compute_convex_hull(coords)
    # GeoJSON expects [lng, lat] and closed polygon (first == last)
    poly = [[round(pt[1], 5), round(pt[0], 5)] for pt in hull]
    if poly and poly[0] != poly[-1]:
        poly.append(poly[0])
    return poly


def generate_catchment_geojson(
    warehouses: List[Dict[str, Any]], 
    assignments: List[Dict[str, Any]],
    demand_coords: Dict[str, Tuple[float, float]]
) -> Dict[str, Any]:
    """
    Generates standard GeoJSON FeatureCollection of service polygons for each warehouse.
    """
    features = []
    
    # Palette of distinctive supply-chain zone colors
    palette = ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899", "#14B8A6"]

    # Group demand points by assigned warehouse
    wh_points: Dict[str, List[Tuple[float, float]]] = {wh["id"]: [(wh["lat"], wh["lng"])] for wh in warehouses}
    for asgn in assignments:
        wh_id = asgn["warehouse_id"]
        dem_id = asgn["demand_id"]
        if dem_id in demand_coords and wh_id in wh_points:
            wh_points[wh_id].append(demand_coords[dem_id])

    for idx, wh in enumerate(warehouses):
        wh_id = wh["id"]
        pts = wh_points.get(wh_id, [])
        polygon_coords = expand_polygon_buffer(pts, buffer_deg=0.18)
        color = palette[idx % len(palette)]

        if polygon_coords:
            feature = {
                "type": "Feature",
                "properties": {
                    "warehouse_id": wh_id,
                    "warehouse_name": wh.get("name", wh_id),
                    "fill_color": color,
                    "stroke_color": color,
                    "assigned_points_count": len(pts) - 1,
                    "total_assigned_demand": wh.get("assigned_demand", 0)
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [polygon_coords]
                }
            }
            features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features
    }
