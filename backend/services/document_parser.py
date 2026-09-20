"""
Document & Invoice Parsing Service for GridPoint.
Extracts business profiles, city orders, and demand quantities from uploaded
CSVs, text delivery sheets, JSON invoices, and free-form dispatch logs.
"""

import re
import csv
import io
import json
from typing import Dict, List, Any, Tuple
from ..api.search import OFFLINE_INDIAN_LOCATIONS
from .nlp_classifier import analyze_user_business


def geocode_city_fuzzy(city_name: str) -> Tuple[float, float, str]:
    """
    Fuzzy matches city name against our verified Indian location database.
    """
    clean = (city_name or "").strip().lower()
    for loc in OFFLINE_INDIAN_LOCATIONS:
        loc_name = loc["name"].lower()
        if clean == loc_name or clean in loc_name or loc_name in clean:
            return loc["lat"], loc["lng"], loc["name"]
    # Fallback to central coordinates
    return 14.5000, 76.0000, city_name.strip().title()


def parse_csv_document(content: str) -> List[Dict[str, Any]]:
    """
    Parses CSV content with various column naming conventions.
    """
    reader = csv.DictReader(io.StringIO(content))
    points = []
    
    for idx, row in enumerate(reader):
        norm_row = {k.strip().lower().replace("_", "").replace(" ", ""): v for k, v in row.items() if k}
        
        # Detect city/location
        city = (
            norm_row.get("city") or norm_row.get("location") or norm_row.get("name") or 
            norm_row.get("destination") or norm_row.get("district") or norm_row.get("town") or 
            f"Point_{idx+1}"
        )
        
        # Detect demand/quantity
        demand_val = 5000.0
        for key in ["demand", "quantity", "orders", "units", "sales", "volume", "tonnes", "tons", "weight"]:
            if key in norm_row and norm_row[key]:
                try:
                    cleaned_val = str(norm_row[key]).replace(",", "").replace("₹", "").strip()
                    demand_val = float(cleaned_val)
                    break
                except ValueError:
                    pass

        # Detect lat/lng if provided, else geocode
        lat = None
        lng = None
        for k in ["lat", "latitude"]:
            if k in norm_row and norm_row[k]:
                try:
                    lat = float(norm_row[k])
                except ValueError:
                    pass
        for k in ["lng", "lon", "longitude"]:
            if k in norm_row and norm_row[k]:
                try:
                    lng = float(norm_row[k])
                except ValueError:
                    pass

        if lat is None or lng is None:
            lat, lng, canonical_name = geocode_city_fuzzy(city)
        else:
            canonical_name = str(city).strip().title()

        points.append({
            "id": f"dem_{idx+1}",
            "name": canonical_name,
            "lat": round(lat, 4),
            "lng": round(lng, 4),
            "demand": round(demand_val, 1)
        })

    return points


def parse_freeform_text(content: str) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Extracts demand data and business profile from text reports, delivery run-sheets, and unstructured logs.
    """
    lower_content = content.lower()
    nlp_result = analyze_user_business(content[:1000])

    # Look for Indian cities mentioned in text
    points = []
    seen_cities = set()

    for loc in OFFLINE_INDIAN_LOCATIONS:
        c_name = loc["name"].lower()
        # Word boundary match for city name
        if re.search(r'\b' + re.escape(c_name) + r'\b', lower_content) and c_name not in seen_cities:
            seen_cities.add(c_name)
            # Find numbers near the city name
            pattern = rf"{re.escape(c_name)}.*?(\d[\d,]*)"
            match = re.search(pattern, lower_content, re.IGNORECASE)
            demand_val = 8000.0
            if match:
                try:
                    demand_val = float(match.group(1).replace(",", ""))
                except Exception:
                    pass

            points.append({
                "id": f"doc_{len(points)+1}",
                "name": loc["name"],
                "lat": loc["lat"],
                "lng": loc["lng"],
                "demand": demand_val
            })

    return nlp_result, points


def process_uploaded_document(filename: str, content: str) -> Dict[str, Any]:
    """
    Master document ingestion endpoint.
    Handles CSV, JSON, TXT, and invoice dispatch formats.
    """
    filename_lower = filename.lower()
    points = []
    nlp_res = analyze_user_business(content[:1000])

    if filename_lower.endswith(".csv"):
        points = parse_csv_document(content)
    elif filename_lower.endswith(".json"):
        try:
            data = json.loads(content)
            if isinstance(data, list):
                for i, item in enumerate(data):
                    city = item.get("name") or item.get("location") or item.get("city") or f"Point {i+1}"
                    lat = item.get("lat")
                    lng = item.get("lng")
                    if lat is None or lng is None:
                        lat, lng, city = geocode_city_fuzzy(city)
                    points.append({
                        "id": item.get("id") or f"json_{i+1}",
                        "name": city,
                        "lat": round(lat, 4),
                        "lng": round(lng, 4),
                        "demand": float(item.get("demand", item.get("orders", 5000)))
                    })
            elif isinstance(data, dict):
                if "demand_points" in data:
                    points = data["demand_points"]
                desc = data.get("business_type") or data.get("industry") or data.get("description") or ""
                if desc:
                    nlp_res = analyze_user_business(desc)
        except Exception:
            nlp_res, points = parse_freeform_text(content)
    else:
        # Free-form TXT / Invoice run-sheet
        nlp_res, points = parse_freeform_text(content)

    total_demand = sum(p.get("demand", 0) for p in points)

    return {
        "filename": filename,
        "detected_industry": nlp_res["business_category"],
        "archetype_key": nlp_res["archetype_key"],
        "siting_criteria": nlp_res["siting_criteria"],
        "recommended_zones": nlp_res["recommended_zones"],
        "points_extracted": len(points),
        "total_demand": round(total_demand, 1),
        "demand_points": points
    }
