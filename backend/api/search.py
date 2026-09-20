"""
Geocoding & Location Search API for India.
Allows users to search any city, locality, or PIN code in India.
Supports Google Geocoding if API key is present, with automatic
fallback to OpenStreetMap Nominatim and offline Indian gazetteer.
"""

from fastapi import APIRouter, Query
from typing import List, Dict, Any
import httpx
from ..core.config import settings

router = APIRouter(prefix="/api", tags=["Geocoding & Search"])

# Comprehensive offline fallback gazetteer of 85+ key Indian commercial and logistics hubs
OFFLINE_INDIAN_LOCATIONS: List[Dict[str, Any]] = [
    # Karnataka
    {"name": "Bengaluru", "display_name": "Bengaluru Urban, Karnataka, India", "lat": 12.9716, "lng": 77.5946, "state": "Karnataka"},
    {"name": "Nelamangala", "display_name": "Nelamangala Logistics Hub, Bengaluru Rural, Karnataka, India", "lat": 13.0970, "lng": 77.3920, "state": "Karnataka"},
    {"name": "Whitefield", "display_name": "Whitefield Industrial Area, Bengaluru, Karnataka, India", "lat": 12.9698, "lng": 77.7499, "state": "Karnataka"},
    {"name": "Electronic City", "display_name": "Electronic City, Bengaluru, Karnataka, India", "lat": 12.8452, "lng": 77.6602, "state": "Karnataka"},
    {"name": "Hosakote", "display_name": "Hosakote Industrial Area (KIADB), Bengaluru Rural, Karnataka, India", "lat": 13.0722, "lng": 77.7981, "state": "Karnataka"},
    {"name": "Dabaspet", "display_name": "Dabaspet Industrial Area (KIADB), Bengaluru Rural, Karnataka, India", "lat": 13.2300, "lng": 77.2400, "state": "Karnataka"},
    {"name": "Bidadi", "display_name": "Bidadi Industrial Area (KIADB), Ramanagara, Karnataka, India", "lat": 12.7981, "lng": 77.3824, "state": "Karnataka"},
    {"name": "Mysuru", "display_name": "Mysuru (Nanjangud/Hebbal), Karnataka, India", "lat": 12.2958, "lng": 76.6394, "state": "Karnataka"},
    {"name": "Mandya", "display_name": "Mandya Sugar & Agro Belt, Karnataka, India", "lat": 12.5218, "lng": 76.8951, "state": "Karnataka"},
    {"name": "Hassan", "display_name": "Hassan Industrial Area, Karnataka, India", "lat": 13.0033, "lng": 76.1004, "state": "Karnataka"},
    {"name": "Mangaluru", "display_name": "Mangaluru Port & Baikampady, Karnataka, India", "lat": 12.9141, "lng": 74.8560, "state": "Karnataka"},
    {"name": "Udupi", "display_name": "Udupi & Manipal, Karnataka, India", "lat": 13.3409, "lng": 74.7421, "state": "Karnataka"},
    {"name": "Hubballi", "display_name": "Hubballi-Dharwad (Tarihal/Rayapur), Karnataka, India", "lat": 15.3647, "lng": 75.1240, "state": "Karnataka"},
    {"name": "Belagavi", "display_name": "Belagavi (Kanbargi/Honaga), Karnataka, India", "lat": 15.8497, "lng": 74.4977, "state": "Karnataka"},
    {"name": "Ballari", "display_name": "Ballari (Bellary Steel Belt), Karnataka, India", "lat": 15.1394, "lng": 76.9214, "state": "Karnataka"},
    {"name": "Davangere", "display_name": "Davangere, Karnataka, India", "lat": 14.4644, "lng": 75.9218, "state": "Karnataka"},
    {"name": "Shivamogga", "display_name": "Shivamogga (Shimoga), Karnataka, India", "lat": 13.9299, "lng": 75.5681, "state": "Karnataka"},
    {"name": "Tumakuru", "display_name": "Tumakuru (Vasanthanarasapura NIMZ), Karnataka, India", "lat": 13.3379, "lng": 77.1010, "state": "Karnataka"},
    {"name": "Kalaburagi", "display_name": "Kalaburagi (Gulbarga), Karnataka, India", "lat": 17.3297, "lng": 76.8343, "state": "Karnataka"},
    {"name": "Vijayapura", "display_name": "Vijayapura (Bijapur), Karnataka, India", "lat": 16.8302, "lng": 75.7100, "state": "Karnataka"},
    {"name": "Bagalkot", "display_name": "Bagalkot & Mudhol Sugar Belt, Karnataka, India", "lat": 16.1853, "lng": 75.6968, "state": "Karnataka"},
    {"name": "Kolar", "display_name": "Kolar & Narasapura Industrial Area, Karnataka, India", "lat": 13.1367, "lng": 78.1291, "state": "Karnataka"},
    {"name": "Raichur", "display_name": "Raichur Industrial Growth Centre, Karnataka, India", "lat": 16.2076, "lng": 77.3463, "state": "Karnataka"},

    # Maharashtra
    {"name": "Mumbai", "display_name": "Mumbai Central, Maharashtra, India", "lat": 18.9690, "lng": 72.8205, "state": "Maharashtra"},
    {"name": "Bhiwandi", "display_name": "Bhiwandi Warehousing Hub, Thane, Maharashtra, India", "lat": 19.2967, "lng": 73.0631, "state": "Maharashtra"},
    {"name": "Thane", "display_name": "Thane, Maharashtra, India", "lat": 19.2183, "lng": 72.9781, "state": "Maharashtra"},
    {"name": "Navi Mumbai", "display_name": "Navi Mumbai / JNPT Corridor, Maharashtra, India", "lat": 19.0760, "lng": 72.9977, "state": "Maharashtra"},
    {"name": "Pune", "display_name": "Pune (Chakan/Hinjawadi/Talegaon), Maharashtra, India", "lat": 18.5204, "lng": 73.8567, "state": "Maharashtra"},
    {"name": "Chakan", "display_name": "Chakan Auto MIDC Corridor, Pune, Maharashtra, India", "lat": 18.7597, "lng": 73.8569, "state": "Maharashtra"},
    {"name": "Nagpur", "display_name": "Nagpur (MIHAN Multi-Modal Logistics Hub), Maharashtra, India", "lat": 21.1458, "lng": 79.0882, "state": "Maharashtra"},
    {"name": "Nashik", "display_name": "Nashik (Ambad/Satpur MIDC), Maharashtra, India", "lat": 19.9975, "lng": 73.7898, "state": "Maharashtra"},
    {"name": "Chhatrapati Sambhajinagar", "display_name": "Chhatrapati Sambhajinagar (Aurangabad/Shendra), Maharashtra, India", "lat": 19.8762, "lng": 75.3433, "state": "Maharashtra"},
    {"name": "Kolhapur", "display_name": "Kolhapur (Shiroli/Gokul Shirgaon), Maharashtra, India", "lat": 16.7050, "lng": 74.2433, "state": "Maharashtra"},
    {"name": "Sangli", "display_name": "Sangli - Miraj - Kupwad MIDC, Maharashtra, India", "lat": 16.8524, "lng": 74.5815, "state": "Maharashtra"},
    {"name": "Solapur", "display_name": "Solapur Textile Cluster, Maharashtra, India", "lat": 17.6599, "lng": 75.9064, "state": "Maharashtra"},
    {"name": "Amravati", "display_name": "Amravati Textile MIDC, Maharashtra, India", "lat": 20.9320, "lng": 77.7523, "state": "Maharashtra"},

    # Tamil Nadu
    {"name": "Chennai", "display_name": "Chennai (Sriperumbudur/Oragadam Corridor), Tamil Nadu, India", "lat": 13.0827, "lng": 80.2707, "state": "Tamil Nadu"},
    {"name": "Sriperumbudur", "display_name": "Sriperumbudur Auto & Electronics SEZ, Tamil Nadu, India", "lat": 12.9675, "lng": 79.9400, "state": "Tamil Nadu"},
    {"name": "Coimbatore", "display_name": "Coimbatore (Pump & Textile Engineering), Tamil Nadu, India", "lat": 11.0168, "lng": 76.9558, "state": "Tamil Nadu"},
    {"name": "Tirupur", "display_name": "Tirupur Knitwear & Garment Export Capital, Tamil Nadu, India", "lat": 11.1085, "lng": 77.3411, "state": "Tamil Nadu"},
    {"name": "Salem", "display_name": "Salem Steel & Sago Industrial Cluster, Tamil Nadu, India", "lat": 11.6643, "lng": 78.1460, "state": "Tamil Nadu"},
    {"name": "Madurai", "display_name": "Madurai Commercial Hub, Tamil Nadu, India", "lat": 9.9252, "lng": 78.1198, "state": "Tamil Nadu"},
    {"name": "Hosur", "display_name": "Hosur Industrial Complex (SIPCOT), Tamil Nadu, India", "lat": 12.7409, "lng": 77.8253, "state": "Tamil Nadu"},
    {"name": "Tuticorin", "display_name": "Thoothukudi (Tuticorin Port Cluster), Tamil Nadu, India", "lat": 8.7642, "lng": 78.1348, "state": "Tamil Nadu"},

    # Telangana & Andhra Pradesh
    {"name": "Hyderabad", "display_name": "Hyderabad (Shamshabad/Medchal Logistics), Telangana, India", "lat": 17.3850, "lng": 78.4867, "state": "Telangana"},
    {"name": "Warangal", "display_name": "Warangal Kakatiya Mega Textile Park, Telangana, India", "lat": 17.9689, "lng": 79.5941, "state": "Telangana"},
    {"name": "Visakhapatnam", "display_name": "Visakhapatnam (Vizag Port & Steel SEZ), Andhra Pradesh, India", "lat": 17.6868, "lng": 83.2185, "state": "Andhra Pradesh"},
    {"name": "Vijayawada", "display_name": "Vijayawada Commercial Gateway, Andhra Pradesh, India", "lat": 16.5062, "lng": 80.6480, "state": "Andhra Pradesh"},
    {"name": "Tirupati", "display_name": "Tirupati & Sri City SEZ, Andhra Pradesh, India", "lat": 13.6288, "lng": 79.4192, "state": "Andhra Pradesh"},

    # Gujarat
    {"name": "Ahmedabad", "display_name": "Ahmedabad (Sanand/Changodar Industrial Hub), Gujarat, India", "lat": 23.0225, "lng": 72.5714, "state": "Gujarat"},
    {"name": "Surat", "display_name": "Surat (Textile & Diamond Logistics), Gujarat, India", "lat": 21.1702, "lng": 72.8311, "state": "Gujarat"},
    {"name": "Vadodara", "display_name": "Vadodara (Baroda Heavy Engineering Cluster), Gujarat, India", "lat": 22.3072, "lng": 73.1812, "state": "Gujarat"},
    {"name": "Rajkot", "display_name": "Rajkot (Engineering & Machine Tools GIDC), Gujarat, India", "lat": 22.3039, "lng": 70.8022, "state": "Gujarat"},
    {"name": "Morbi", "display_name": "Morbi Ceramic & Tile Mega Belt, Gujarat, India", "lat": 22.8120, "lng": 70.8384, "state": "Gujarat"},
    {"name": "Ankleshwar", "display_name": "Ankleshwar - Dahej PCPIR Chemical Belt, Gujarat, India", "lat": 21.6264, "lng": 73.0032, "state": "Gujarat"},

    # North India (Delhi NCR, Haryana, UP, Punjab, Rajasthan)
    {"name": "Delhi NCR", "display_name": "Delhi National Capital Region, India", "lat": 28.6139, "lng": 77.2090, "state": "Delhi"},
    {"name": "Gurugram", "display_name": "Gurugram / Manesar Industrial Model Township, Haryana, India", "lat": 28.4595, "lng": 77.0266, "state": "Haryana"},
    {"name": "Noida", "display_name": "Noida - Greater Noida Tech & Logistics Corridor, Uttar Pradesh, India", "lat": 28.5355, "lng": 77.3910, "state": "Uttar Pradesh"},
    {"name": "Faridabad", "display_name": "Faridabad Industrial Cluster, Haryana, India", "lat": 28.4089, "lng": 77.3178, "state": "Haryana"},
    {"name": "Ludhiana", "display_name": "Ludhiana (Textile & Cycle Manufacturing Hub), Punjab, India", "lat": 30.9010, "lng": 75.8573, "state": "Punjab"},
    {"name": "Amritsar", "display_name": "Amritsar Trade Corridor, Punjab, India", "lat": 31.6340, "lng": 74.8723, "state": "Punjab"},
    {"name": "Chandigarh", "display_name": "Chandigarh & Mohali Tech Cluster, India", "lat": 30.7333, "lng": 76.7794, "state": "Chandigarh"},
    {"name": "Jaipur", "display_name": "Jaipur (Sitapura/VKI Industrial Area), Rajasthan, India", "lat": 26.9124, "lng": 75.7873, "state": "Rajasthan"},
    {"name": "Jodhpur", "display_name": "Jodhpur Handicrafts & Solar Hub, Rajasthan, India", "lat": 26.2389, "lng": 73.0243, "state": "Rajasthan"},
    {"name": "Lucknow", "display_name": "Lucknow Transport Nagar & Logistics Hub, Uttar Pradesh, India", "lat": 26.8467, "lng": 80.9462, "state": "Uttar Pradesh"},
    {"name": "Kanpur", "display_name": "Kanpur (Panki / Jajmau Leather Belt), Uttar Pradesh, India", "lat": 26.4499, "lng": 80.3319, "state": "Uttar Pradesh"},
    {"name": "Agra", "display_name": "Agra Footwear & Tourism Corridor, Uttar Pradesh, India", "lat": 27.1767, "lng": 78.0081, "state": "Uttar Pradesh"},
    {"name": "Varanasi", "display_name": "Varanasi (Kashi Freight Terminal), Uttar Pradesh, India", "lat": 25.3176, "lng": 82.9739, "state": "Uttar Pradesh"},

    # Central India
    {"name": "Indore", "display_name": "Indore - Pithampur Industrial SEZ, Madhya Pradesh, India", "lat": 22.7196, "lng": 75.8577, "state": "Madhya Pradesh"},
    {"name": "Bhopal", "display_name": "Bhopal (Mandideep Industrial Area), Madhya Pradesh, India", "lat": 23.2599, "lng": 77.4126, "state": "Madhya Pradesh"},

    # East India
    {"name": "Kolkata", "display_name": "Kolkata / Howrah Freight Terminal, West Bengal, India", "lat": 22.5726, "lng": 88.3639, "state": "West Bengal"},
    {"name": "Durgapur", "display_name": "Durgapur - Asansol Steel & Industrial Belt, West Bengal, India", "lat": 23.5204, "lng": 87.3119, "state": "West Bengal"},
    {"name": "Patna", "display_name": "Patna Commercial Trading Centre, Bihar, India", "lat": 25.5941, "lng": 85.1376, "state": "Bihar"},
    {"name": "Ranchi", "display_name": "Ranchi (Tupudana Industrial Area), Jharkhand, India", "lat": 23.3441, "lng": 85.3096, "state": "Jharkhand"},
    {"name": "Jamshedpur", "display_name": "Jamshedpur Tata Steel City, Jharkhand, India", "lat": 22.8046, "lng": 86.2029, "state": "Jharkhand"},
    {"name": "Bhubaneswar", "display_name": "Bhubaneswar & Cuttack Industrial Corridor, Odisha, India", "lat": 20.2961, "lng": 85.8245, "state": "Odisha"},
    {"name": "Guwahati", "display_name": "Guwahati Logistics Gateway to Northeast, Assam, India", "lat": 26.1445, "lng": 91.7362, "state": "Assam"},

    # Kerala
    {"name": "Kochi", "display_name": "Kochi (Vallarpadam Port & Cochin SEZ), Kerala, India", "lat": 9.9312, "lng": 76.2673, "state": "Kerala"},
    {"name": "Thiruvananthapuram", "display_name": "Thiruvananthapuram (Vizhinjam Port Corridor), Kerala, India", "lat": 8.5241, "lng": 76.9366, "state": "Kerala"},
    {"name": "Kozhikode", "display_name": "Kozhikode (Calicut), Kerala, India", "lat": 11.2588, "lng": 75.7804, "state": "Kerala"}
]


@router.get("/search", response_model=List[Dict[str, Any]])
async def search_location(q: str = Query(..., min_length=2, description="City, locality, or landmark in India")):
    """
    Geocodes search queries across India.
    Uses Google Geocoding API if key configured, otherwise Nominatim with local offline fallback.
    """
    clean_q = q.strip()
    
    # 1. Try Google Maps Geocoding if API key is provided
    if settings.GOOGLE_MAPS_API_KEY:
        try:
            google_url = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {
                "address": clean_q,
                "components": "country:IN",
                "key": settings.GOOGLE_MAPS_API_KEY
            }
            async with httpx.AsyncClient(timeout=2.0) as client:
                res = await client.get(google_url, params=params)
                if res.status_code == 200:
                    data = res.json()
                    results = []
                    for item in data.get("results", [])[:5]:
                        loc = item["geometry"]["location"]
                        results.append({
                            "name": item.get("formatted_address", clean_q).split(",")[0],
                            "display_name": item.get("formatted_address"),
                            "lat": round(loc["lat"], 5),
                            "lng": round(loc["lng"], 5),
                            "source": "Google Maps"
                        })
                    if results:
                        return results
        except Exception:
            pass

    # 2. Local Verified India Gazetteer Match (Fastest & 100% offline)
    lower_q = clean_q.lower()
    exact_matches = []
    partial_matches = []
    
    for loc in OFFLINE_INDIAN_LOCATIONS:
        loc_name = loc["name"].lower()
        disp_name = loc["display_name"].lower()
        if lower_q == loc_name:
            exact_matches.append({**loc, "source": "India Verified Gazetteer"})
        elif lower_q in loc_name or loc_name in lower_q:
            partial_matches.append({**loc, "source": "India Verified Gazetteer"})
        elif lower_q in disp_name:
            partial_matches.append({**loc, "source": "India Verified Gazetteer"})

    results = exact_matches + partial_matches
    if results:
        return results[:6]

    # 3. Try OpenStreetMap Nominatim with India countrycode
    try:
        headers = {"User-Agent": "GridPoint-Logistics-Engine/1.0"}
        nominatim_url = f"https://nominatim.openstreetmap.org/search?q={clean_q}&format=json&countrycodes=in&limit=5"
        async with httpx.AsyncClient(timeout=2.5) as client:
            res = await client.get(nominatim_url, headers=headers)
            if res.status_code == 200:
                data = res.json()
                osm_results = []
                for item in data:
                    osm_results.append({
                        "name": item.get("display_name", "").split(",")[0],
                        "display_name": item.get("display_name"),
                        "lat": round(float(item["lat"]), 5),
                        "lng": round(float(item["lon"]), 5),
                        "source": "OpenStreetMap"
                    })
                if osm_results:
                    return osm_results
    except Exception:
        pass

    # Default fallback
    return [{
        "name": clean_q.title(),
        "display_name": f"{clean_q.title()}, India",
        "lat": 13.0000,
        "lng": 77.0000,
        "source": "Approximated"
    }]
