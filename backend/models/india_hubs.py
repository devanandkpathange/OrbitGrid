"""
Recognized Indian Logistics, Warehousing, and Industrial Corridors.
Used by GridPoint for industrial hub snapping to ensure recommendations
fall within viable industrial zones with existing highway & freight infrastructure.
"""

from typing import List, Dict, Any

INDIA_INDUSTRIAL_HUBS: List[Dict[str, Any]] = [
    # Karnataka Hubs
    {
        "id": "hub_blr_nelamangala",
        "name": "Nelamangala Logistics Hub (NH-48 / Tumkur Rd)",
        "city": "Bengaluru",
        "state": "Karnataka",
        "lat": 13.0970,
        "lng": 77.3920,
        "type": "Grade-A Warehousing Cluster",
        "highway_access": "NH-48 (Bengaluru - Mumbai)",
        "typical_rent_sqft_inr": 24.0
    },
    {
        "id": "hub_blr_hosakote",
        "name": "Hosakote Industrial Area (KIADB / Chennai Corridor)",
        "city": "Bengaluru",
        "state": "Karnataka",
        "lat": 13.0722,
        "lng": 77.7981,
        "type": "Industrial & E-Commerce Hub",
        "highway_access": "NH-75 (Bengaluru - Chennai)",
        "typical_rent_sqft_inr": 26.0
    },
    {
        "id": "hub_blr_bommasandra",
        "name": "Bommasandra & Jigani Industrial Area",
        "city": "Bengaluru",
        "state": "Karnataka",
        "lat": 12.8163,
        "lng": 77.6917,
        "type": "Electronics & FMCG Hub",
        "highway_access": "NH-44 (Bengaluru - Hosur)",
        "typical_rent_sqft_inr": 28.0
    },
    {
        "id": "hub_mys_nanjangud",
        "name": "Nanjangud Industrial Area (KIADB)",
        "city": "Mysuru",
        "state": "Karnataka",
        "lat": 12.1221,
        "lng": 76.6811,
        "type": "Manufacturing & Distribution Hub",
        "highway_access": "NH-766 (Mysuru - Kerala)",
        "typical_rent_sqft_inr": 18.0
    },
    {
        "id": "hub_hubballi_tarihal",
        "name": "Tarihal & Rayapur Industrial Corridor",
        "city": "Hubballi-Dharwad",
        "state": "Karnataka",
        "lat": 15.3905,
        "lng": 75.1051,
        "type": "North Karnataka Central Distribution Center",
        "highway_access": "NH-48 (Golden Quadrilateral)",
        "typical_rent_sqft_inr": 16.0
    },
    {
        "id": "hub_mangaluru_baikampady",
        "name": "Baikampady Industrial Estate (New Mangalore Port)",
        "city": "Mangaluru",
        "state": "Karnataka",
        "lat": 12.9460,
        "lng": 74.8210,
        "type": "Port & Coastal Logistics Hub",
        "highway_access": "NH-66 (Panvel - Kochi)",
        "typical_rent_sqft_inr": 20.0
    },
    {
        "id": "hub_belagavi_kanabargi",
        "name": "Kanabargi & Udyambag Industrial Area",
        "city": "Belagavi",
        "state": "Karnataka",
        "lat": 15.8824,
        "lng": 74.5381,
        "type": "Auto & Heavy Goods Logistics",
        "highway_access": "NH-48",
        "typical_rent_sqft_inr": 15.0
    },
    {
        "id": "hub_tumakuru_vasanthanarasapura",
        "name": "Vasanthanarasapura Industrial Mega Park",
        "city": "Tumakuru",
        "state": "Karnataka",
        "lat": 13.4350,
        "lng": 77.0180,
        "type": "National Investment & Manufacturing Zone (NIMZ)",
        "highway_access": "NH-48",
        "typical_rent_sqft_inr": 14.0
    },
    {
        "id": "hub_kalaburagi_kapnoor",
        "name": "Kapnoor Industrial Area",
        "city": "Kalaburagi",
        "state": "Karnataka",
        "lat": 17.3450,
        "lng": 76.8620,
        "type": "Kalyana Karnataka Regional Hub",
        "highway_access": "NH-150",
        "typical_rent_sqft_inr": 13.0
    },

    # Maharashtra Hubs
    {
        "id": "hub_mum_bhiwandi",
        "name": "Bhiwandi Warehousing & Fulfillment Hub",
        "city": "Bhiwandi / Thane",
        "state": "Maharashtra",
        "lat": 19.2967,
        "lng": 73.0631,
        "type": "National Mega-Logistics Park",
        "highway_access": "NH-160 / Mumbai-Nashik Expy",
        "typical_rent_sqft_inr": 32.0
    },
    {
        "id": "hub_pune_chakan",
        "name": "Chakan & Talegaon MIDC Logistics Corridor",
        "city": "Pune",
        "state": "Maharashtra",
        "lat": 18.7597,
        "lng": 73.8569,
        "type": "Automotive & Heavy Warehousing",
        "highway_access": "NH-60 & Mumbai-Pune Expy",
        "typical_rent_sqft_inr": 25.0
    },
    {
        "id": "hub_nagpur_mihan",
        "name": "MIHAN SEZ Multi-Modal Logistics Hub",
        "city": "Nagpur",
        "state": "Maharashtra",
        "lat": 21.0560,
        "lng": 79.0520,
        "type": "Zero Mile Center of India",
        "highway_access": "NH-44 & Samruddhi Mahamarg",
        "typical_rent_sqft_inr": 20.0
    },

    # North India / Delhi-NCR / Rajasthan Corridors (NH-48 DMIC Belt)
    {
        "id": "hub_del_neemrana",
        "name": "Neemrana Industrial Zone (RIICO / NH-48 Delhi-Jaipur DMIC Corridor)",
        "city": "Neemrana / Kotputli",
        "state": "Rajasthan",
        "lat": 27.9890,
        "lng": 76.3860,
        "type": "Joint North Metro Siting (Co-serves Delhi 90km & Jaipur 130km)",
        "highway_access": "NH-48 (Delhi-Mumbai Expressway & DMIC)",
        "typical_rent_sqft_inr": 22.0
    },
    {
        "id": "hub_del_bilaspur_tauru",
        "name": "Bilaspur-Tauru & KMP Expressway Warehousing Belt",
        "city": "Gurugram / NCR",
        "state": "Haryana",
        "lat": 28.3200,
        "lng": 76.8200,
        "type": "North India Primary Logistics Belt",
        "highway_access": "NH-48 & Western Peripheral Expressway (KMP)",
        "typical_rent_sqft_inr": 28.0
    },
    {
        "id": "hub_del_manesar",
        "name": "Manesar & Dharuhera Industrial Hub",
        "city": "Rewari / Gurugram",
        "state": "Haryana",
        "lat": 28.2100,
        "lng": 76.7900,
        "type": "Automotive & Retail Distribution Corridor",
        "highway_access": "NH-48",
        "typical_rent_sqft_inr": 26.0
    },
    {
        "id": "hub_jaipur_bagru",
        "name": "Bagru & Mahindra World City Logistics Park",
        "city": "Jaipur",
        "state": "Rajasthan",
        "lat": 26.8150,
        "lng": 75.5450,
        "type": "Rajasthan Regional Distribution Center",
        "highway_access": "NH-48 (Ajmer-Jaipur Rd)",
        "typical_rent_sqft_inr": 18.0
    },
    {
        "id": "hub_del_farukhnagar",
        "name": "Farukhnagar & Pataudi Warehousing Hub",
        "city": "Gurugram / NCR",
        "state": "Haryana",
        "lat": 28.4520,
        "lng": 76.8180,
        "type": "E-Commerce Mega-Fulfillment Hub",
        "highway_access": "KMP Expressway & NH-48",
        "typical_rent_sqft_inr": 28.0
    },

    # West & Gujarat Hubs
    {
        "id": "hub_ahmedabad_sanand",
        "name": "Sanand & Changodar Industrial Logistics Belt",
        "city": "Ahmedabad",
        "state": "Gujarat",
        "lat": 22.9868,
        "lng": 72.3812,
        "type": "Western India Multi-Modal Hub",
        "highway_access": "NH-47 & Ahmedabad-Rajkot Highway",
        "typical_rent_sqft_inr": 21.0
    },

    # Tamil Nadu / Telangana / South Hubs
    {
        "id": "hub_chn_sriperumbudur",
        "name": "Sriperumbudur & Oragadam SIPCOT Cluster",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "lat": 12.9699,
        "lng": 79.9400,
        "type": "Automotive & Electronics Logistics Hub",
        "highway_access": "NH-48 (Chennai - Bengaluru)",
        "typical_rent_sqft_inr": 24.0
    },
    {
        "id": "hub_hyd_shamshabad",
        "name": "Shamshabad & ORR Logistics Park",
        "city": "Hyderabad",
        "state": "Telangana",
        "lat": 17.2403,
        "lng": 78.4294,
        "type": "Air Cargo & Southern Distribution Zone",
        "highway_access": "Hyderabad ORR & NH-44",
        "typical_rent_sqft_inr": 22.0
    },

    # East Hubs
    {
        "id": "hub_kolkata_dankuni",
        "name": "Dankuni Freight Terminal & Industrial Corridor",
        "city": "Kolkata / Hooghly",
        "state": "West Bengal",
        "lat": 22.6850,
        "lng": 88.2930,
        "type": "Eastern Gateway Freight Hub",
        "highway_access": "NH-19 & DFC Eastern Corridor",
        "typical_rent_sqft_inr": 22.0
    }
]


def find_nearest_hub(lat: float, lng: float, state: str = None, max_distance_km: float = 180.0) -> Dict[str, Any]:
    """
    Finds the nearest recognized industrial warehousing park to given coordinates.
    If state is provided, first checks if a hub in that state is within max_distance_km.
    If not (e.g. centroid is in North India but state filter was Karnataka), searches
    all national industrial parks across India to avoid picking a distant 1,000 km hub.
    If no hub is within max_distance_km, returns None so the exact mathematical
    centroid is preserved.
    """
    import math

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    # 1. Try state filter if specified
    if state and state.lower() not in ["pan_india", "india", "all"]:
        state_candidates = [h for h in INDIA_INDUSTRIAL_HUBS if h["state"].lower() == state.lower()]
        if state_candidates:
            best_state_hub = None
            min_state_dist = float("inf")
            for hub in state_candidates:
                d = haversine(lat, lng, hub["lat"], hub["lng"])
                if d < min_state_dist:
                    min_state_dist = d
                    best_state_hub = {**hub, "distance_to_centroid_km": round(d, 2)}
            # If the state hub is within a reasonable distance, return it
            if best_state_hub and min_state_dist <= max_distance_km:
                return best_state_hub

    # 2. Search all national hubs across India
    best_hub = None
    min_dist = float("inf")
    for hub in INDIA_INDUSTRIAL_HUBS:
        d = haversine(lat, lng, hub["lat"], hub["lng"])
        if d < min_dist:
            min_dist = d
            best_hub = {**hub, "distance_to_centroid_km": round(d, 2)}

    # 3. Only snap if the nearest hub is within max_distance_km
    if best_hub and min_dist <= max_distance_km:
        return best_hub

    return None
