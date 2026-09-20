import os
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import Dict, Any, List

router = APIRouter(prefix="/api", tags=["Demo Datasets"])

DEMO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "demo"))


@router.get("/demo/sample-csvs")
async def list_sample_csvs():
    """
    Lists all available training and demo CSV files ready for download and testing.
    """
    csv_files = [
        {
            "filename": "sample_karnataka_retail_demand.csv",
            "name": "Karnataka Commercial & Retail Demand (24 Cities)",
            "industry": "Retail & E-Commerce",
            "records": 24,
            "download_url": "/api/demo/download/sample_karnataka_retail_demand.csv"
        },
        {
            "filename": "sample_sugarcane_agro_demand.csv",
            "name": "Karnataka & Maharashtra Sugarcane Belt (12 Towns)",
            "industry": "Sugarcane & Agro-Processing",
            "records": 12,
            "download_url": "/api/demo/download/sample_sugarcane_agro_demand.csv"
        },
        {
            "filename": "sample_pan_india_fmcg.csv",
            "name": "Pan-India Tier-1 & Tier-2 Distribution (20 Metros)",
            "industry": "FMCG & Consumer Goods",
            "records": 20,
            "download_url": "/api/demo/download/sample_pan_india_fmcg.csv"
        }
    ]
    return csv_files


@router.get("/demo/download/{filename}")
async def download_sample_csv(filename: str):
    """
    Downloads a training CSV dataset for upload and testing.
    """
    # Security: prevent path traversal
    safe_filename = os.path.basename(filename)
    filepath = os.path.join(DEMO_DIR, safe_filename)

    if not os.path.exists(filepath) or not safe_filename.endswith((".csv", ".json")):
        raise HTTPException(status_code=404, detail=f"File '{safe_filename}' not found.")

    media_type = "text/csv" if safe_filename.endswith(".csv") else "application/json"
    return FileResponse(
        path=filepath,
        filename=safe_filename,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{safe_filename}"'}
    )


# Comprehensive realistic Indian state datasets for on-demand logistics simulation
INDIAN_STATE_DATASETS: Dict[str, Dict[str, Any]] = {
    "tamil_nadu": {
        "region": "Tamil Nadu",
        "total_demand": 268000,
        "unit": "units/month",
        "demand_points": [
            {"id": "tn_1", "name": "Chennai (Sriperumbudur / Oragadam Corridor)", "lat": 13.0827, "lng": 80.2707, "demand": 68000},
            {"id": "tn_2", "name": "Coimbatore (Textile & Precision Engineering)", "lat": 11.0168, "lng": 76.9558, "demand": 46000},
            {"id": "tn_3", "name": "Tirupur (Knitwear & Garment Export Capital)", "lat": 11.1085, "lng": 77.3411, "demand": 38000},
            {"id": "tn_4", "name": "Salem (Steel & Agro Industrial Cluster)", "lat": 11.6643, "lng": 78.1460, "demand": 29000},
            {"id": "tn_5", "name": "Madurai (Southern Commercial Hub)", "lat": 9.9252, "lng": 78.1198, "demand": 34000},
            {"id": "tn_6", "name": "Hosur (SIPCOT Tech & Auto SEZ)", "lat": 12.7409, "lng": 77.8253, "demand": 32000},
            {"id": "tn_7", "name": "Thoothukudi (Tuticorin Port Cluster)", "lat": 8.7642, "lng": 78.1348, "demand": 21000}
        ]
    },
    "gujarat": {
        "region": "Gujarat",
        "total_demand": 294000,
        "unit": "units/month",
        "demand_points": [
            {"id": "gj_1", "name": "Ahmedabad (Sanand / Changodar Mega GIDC)", "lat": 23.0225, "lng": 72.5714, "demand": 74000},
            {"id": "gj_2", "name": "Surat (Textile & Diamond Export Hub)", "lat": 21.1702, "lng": 72.8311, "demand": 62000},
            {"id": "gj_3", "name": "Vadodara (Heavy Engineering & Pharma GIDC)", "lat": 22.3072, "lng": 73.1812, "demand": 45000},
            {"id": "gj_4", "name": "Rajkot (Engineering & Auto Ancillary Cluster)", "lat": 22.3039, "lng": 70.8022, "demand": 36000},
            {"id": "gj_5", "name": "Morbi (Ceramics & Tiles Global Cluster)", "lat": 22.8120, "lng": 70.8384, "demand": 28000},
            {"id": "gj_6", "name": "Ankleshwar / Dahej (PCPIR Chemical SEZ)", "lat": 21.6264, "lng": 73.0032, "demand": 31000},
            {"id": "gj_7", "name": "Gandhidham / Kandla Port Gateway", "lat": 23.0753, "lng": 70.1337, "demand": 18000}
        ]
    },
    "uttar_pradesh": {
        "region": "Uttar Pradesh",
        "total_demand": 310000,
        "unit": "units/month",
        "demand_points": [
            {"id": "up_1", "name": "Noida / Greater Noida (Tech & Logistics SEZ)", "lat": 28.5355, "lng": 77.3910, "demand": 72000},
            {"id": "up_2", "name": "Lucknow (Transport Nagar Logistics Gateway)", "lat": 26.8467, "lng": 80.9462, "demand": 58000},
            {"id": "up_3", "name": "Kanpur (Panki / Jajmau Industrial Belt)", "lat": 26.4499, "lng": 80.3319, "demand": 51000},
            {"id": "up_4", "name": "Agra (Footwear & Manufacturing Corridor)", "lat": 27.1767, "lng": 78.0081, "demand": 34000},
            {"id": "up_5", "name": "Varanasi (Kashi Freight Terminal)", "lat": 25.3176, "lng": 82.9739, "demand": 38000},
            {"id": "up_6", "name": "Prayagraj (Naini Industrial Growth Centre)", "lat": 25.4358, "lng": 81.8463, "demand": 31000},
            {"id": "up_7", "name": "Bareilly (Northern Agro-Logistics Cluster)", "lat": 28.3670, "lng": 79.4304, "demand": 26000}
        ]
    },
    "rajasthan": {
        "region": "Rajasthan",
        "total_demand": 215000,
        "unit": "units/month",
        "demand_points": [
            {"id": "rj_1", "name": "Jaipur (Sitapura / VKI Industrial Corridor)", "lat": 26.9124, "lng": 75.7873, "demand": 65000},
            {"id": "rj_2", "name": "Jodhpur (Handicrafts & Western Freight Hub)", "lat": 26.2389, "lng": 73.0243, "demand": 38000},
            {"id": "rj_3", "name": "Kota (Industrial & Petrochemical Zone)", "lat": 25.2138, "lng": 75.8648, "demand": 32000},
            {"id": "rj_4", "name": "Alwar / Bhiwadi (Delhi-Mumbai Freight Corridor)", "lat": 27.5530, "lng": 76.6346, "demand": 36000},
            {"id": "rj_5", "name": "Udaipur (Mewar Mining & Logistics Corridor)", "lat": 24.5854, "lng": 73.7125, "demand": 24000},
            {"id": "rj_6", "name": "Bhilwara (Textile City of Rajasthan)", "lat": 25.3407, "lng": 74.6313, "demand": 20000}
        ]
    },
    "telangana": {
        "region": "Telangana",
        "total_demand": 220000,
        "unit": "units/month",
        "demand_points": [
            {"id": "tg_1", "name": "Hyderabad (Shamshabad / Medchal Logistics Hub)", "lat": 17.3850, "lng": 78.4867, "demand": 95000},
            {"id": "tg_2", "name": "Warangal (Kakatiya Mega Textile Park)", "lat": 17.9689, "lng": 79.5941, "demand": 34000},
            {"id": "tg_3", "name": "Nizamabad (Agro & Commercial Trading Hub)", "lat": 18.6725, "lng": 78.0941, "demand": 28000},
            {"id": "tg_4", "name": "Karimnagar (Granite & Grain Corridor)", "lat": 18.4386, "lng": 79.1288, "demand": 27000},
            {"id": "tg_5", "name": "Khammam (Coal & Agri Commercial Centre)", "lat": 17.2473, "lng": 80.1514, "demand": 21000},
            {"id": "tg_6", "name": "Ramagundam (Thermal Energy & Industrial Zone)", "lat": 18.7551, "lng": 79.5134, "demand": 15000}
        ]
    },
    "andhra_pradesh": {
        "region": "Andhra Pradesh",
        "total_demand": 235000,
        "unit": "units/month",
        "demand_points": [
            {"id": "ap_1", "name": "Visakhapatnam (Vizag Port & Steel SEZ)", "lat": 17.6868, "lng": 83.2185, "demand": 62000},
            {"id": "ap_2", "name": "Vijayawada (Commercial Gateway Corridor)", "lat": 16.5062, "lng": 80.6480, "demand": 51000},
            {"id": "ap_3", "name": "Guntur (Tobacco, Chilli & Agro Trade SEZ)", "lat": 16.3067, "lng": 80.4365, "demand": 36000},
            {"id": "ap_4", "name": "Tirupati / Sri City (Multi-Product Mega SEZ)", "lat": 13.6288, "lng": 79.4192, "demand": 38000},
            {"id": "ap_5", "name": "Nellore (Krishnapatnam Port Corridor)", "lat": 14.4426, "lng": 79.9865, "demand": 26000},
            {"id": "ap_6", "name": "Kurnool (Rayalaseema Logistics Hub)", "lat": 15.8281, "lng": 78.0373, "demand": 22000}
        ]
    },
    "kerala": {
        "region": "Kerala",
        "total_demand": 185000,
        "unit": "units/month",
        "demand_points": [
            {"id": "kl_1", "name": "Kochi (Vallarpadam International Port SEZ)", "lat": 9.9312, "lng": 76.2673, "demand": 64000},
            {"id": "kl_2", "name": "Thiruvananthapuram (Vizhinjam Transshipment)", "lat": 8.5241, "lng": 76.9366, "demand": 42000},
            {"id": "kl_3", "name": "Kozhikode (Malabar Trade & Commercial Corridor)", "lat": 11.2588, "lng": 75.7804, "demand": 33000},
            {"id": "kl_4", "name": "Thrissur (Central Commercial & Logistics Hub)", "lat": 10.5276, "lng": 76.2144, "demand": 26000},
            {"id": "kl_5", "name": "Palakkad (KINFRA Integrated Industrial Park)", "lat": 10.7867, "lng": 76.6548, "demand": 20000}
        ]
    },
    "west_bengal": {
        "region": "West Bengal",
        "total_demand": 260000,
        "unit": "units/month",
        "demand_points": [
            {"id": "wb_1", "name": "Kolkata (Dankuni / Howrah Freight Terminal)", "lat": 22.5726, "lng": 88.3639, "demand": 82000},
            {"id": "wb_2", "name": "Durgapur (Asansol Industrial Belt)", "lat": 23.5204, "lng": 87.3119, "demand": 45000},
            {"id": "wb_3", "name": "Siliguri (North-East Chicken's Neck Gateway)", "lat": 26.7271, "lng": 88.3953, "demand": 42000},
            {"id": "wb_4", "name": "Kharagpur (Vidyasagar Industrial Park)", "lat": 22.3460, "lng": 87.2320, "demand": 35000},
            {"id": "wb_5", "name": "Haldia (Deep Water Port & Petrochem SEZ)", "lat": 22.0620, "lng": 88.0825, "demand": 31000},
            {"id": "wb_6", "name": "Bardhaman (Central Agro-Trading Hub)", "lat": 23.2324, "lng": 87.8615, "demand": 25000}
        ]
    },
    "delhi_ncr": {
        "region": "Delhi NCR & Haryana",
        "total_demand": 340000,
        "unit": "units/month",
        "demand_points": [
            {"id": "dl_1", "name": "Delhi Central / Okhla Logistics Center", "lat": 28.6139, "lng": 77.2090, "demand": 85000},
            {"id": "dl_2", "name": "Gurugram / Manesar IMT Corridor", "lat": 28.4595, "lng": 77.0266, "demand": 75000},
            {"id": "dl_3", "name": "Noida / Greater Noida Multi-Modal Park", "lat": 28.5355, "lng": 77.3910, "demand": 68000},
            {"id": "dl_4", "name": "Faridabad Industrial Model Township", "lat": 28.4089, "lng": 77.3178, "demand": 46000},
            {"id": "dl_5", "name": "Panipat (Textile & Refinery Mega Belt)", "lat": 29.3909, "lng": 76.9635, "demand": 38000},
            {"id": "dl_6", "name": "Sonipat / Kundli Logistics Hub", "lat": 28.9931, "lng": 77.0151, "demand": 28000}
        ]
    },
    "madhya_pradesh": {
        "region": "Madhya Pradesh",
        "total_demand": 240000,
        "unit": "units/month",
        "demand_points": [
            {"id": "mp_1", "name": "Indore / Pithampur Auto & Pharma SEZ", "lat": 22.7196, "lng": 75.8577, "demand": 76000},
            {"id": "mp_2", "name": "Bhopal (Mandideep Industrial Area)", "lat": 23.2599, "lng": 77.4126, "demand": 54000},
            {"id": "mp_3", "name": "Jabalpur (Defence & Central Railway Hub)", "lat": 23.1815, "lng": 79.9864, "demand": 38000},
            {"id": "mp_4", "name": "Gwalior (Malanpur Industrial Growth Centre)", "lat": 26.2183, "lng": 78.1828, "demand": 32000},
            {"id": "mp_5", "name": "Ujjain (Agro-Processing & Commercial Node)", "lat": 23.1765, "lng": 75.7885, "demand": 24000},
            {"id": "mp_6", "name": "Dewas (Engineering & Leather SEZ)", "lat": 22.9676, "lng": 76.0534, "demand": 16000}
        ]
    },
    "punjab": {
        "region": "Punjab",
        "total_demand": 205000,
        "unit": "units/month",
        "demand_points": [
            {"id": "pb_1", "name": "Ludhiana (Textile & Bicycle Capital)", "lat": 30.9010, "lng": 75.8573, "demand": 68000},
            {"id": "pb_2", "name": "Amritsar (International Trade Corridor)", "lat": 31.6340, "lng": 74.8723, "demand": 44000},
            {"id": "pb_3", "name": "Jalandhar (Sports Goods & Leather Cluster)", "lat": 31.3260, "lng": 75.5762, "demand": 38000},
            {"id": "pb_4", "name": "Mohali / Chandigarh Tech Corridor", "lat": 30.7046, "lng": 76.7179, "demand": 34000},
            {"id": "pb_5", "name": "Bathinda (Thermal & Cotton Ginning Belt)", "lat": 30.2110, "lng": 74.9455, "demand": 21000}
        ]
    },
    "bihar_jharkhand": {
        "region": "Bihar & Jharkhand",
        "total_demand": 230000,
        "unit": "units/month",
        "demand_points": [
            {"id": "bj_1", "name": "Patna (Eastern Gangetic Commercial Hub)", "lat": 25.5941, "lng": 85.1376, "demand": 62000},
            {"id": "bj_2", "name": "Jamshedpur (Tata Steel & Auto Mega Belt)", "lat": 22.8046, "lng": 86.2029, "demand": 48000},
            {"id": "bj_3", "name": "Ranchi (Tupudana Industrial Area)", "lat": 23.3441, "lng": 85.3096, "demand": 41000},
            {"id": "bj_4", "name": "Dhanbad (Mineral & Energy Freight Corridor)", "lat": 23.7957, "lng": 86.4304, "demand": 32000},
            {"id": "bj_5", "name": "Muzaffarpur (North Bihar Commercial Gateway)", "lat": 26.1226, "lng": 85.3906, "demand": 27000},
            {"id": "bj_6", "name": "Gaya (Grand Trunk Road Transit Hub)", "lat": 24.7914, "lng": 85.0002, "demand": 20000}
        ]
    },
    "odisha": {
        "region": "Odisha",
        "total_demand": 175000,
        "unit": "units/month",
        "demand_points": [
            {"id": "od_1", "name": "Bhubaneswar / Cuttack Twin-City Logistics", "lat": 20.2961, "lng": 85.8245, "demand": 64000},
            {"id": "od_2", "name": "Rourkela (Steel & Heavy Engineering Zone)", "lat": 22.2604, "lng": 84.8536, "demand": 38000},
            {"id": "od_3", "name": "Paradip (Deep Seaport & Petrochem SEZ)", "lat": 20.3165, "lng": 86.6114, "demand": 32000},
            {"id": "od_4", "name": "Sambalpur (Western Industrial Corridor)", "lat": 21.4669, "lng": 83.9812, "demand": 24000},
            {"id": "od_5", "name": "Berhampur (Ganjam Trade Gateway)", "lat": 19.3150, "lng": 84.7941, "demand": 17000}
        ]
    },
    "assam_northeast": {
        "region": "Assam & Northeast Gateway",
        "total_demand": 160000,
        "unit": "units/month",
        "demand_points": [
            {"id": "as_1", "name": "Guwahati (Amingaon Inland Container Depot)", "lat": 26.1445, "lng": 91.7362, "demand": 68000},
            {"id": "as_2", "name": "Silchar (Barak Valley Logistics Hub)", "lat": 24.8333, "lng": 92.7789, "demand": 28000},
            {"id": "as_3", "name": "Dibrugarh (Upper Assam Tea & Petro Hub)", "lat": 27.4728, "lng": 94.9120, "demand": 26000},
            {"id": "as_4", "name": "Jorhat (Central Assam Trading Centre)", "lat": 26.7509, "lng": 94.2037, "demand": 21000},
            {"id": "as_5", "name": "Nagaon (Agri & Transit Corridor)", "lat": 26.3468, "lng": 92.6840, "demand": 17000}
        ]
    }
}


@router.get("/demo/{region}", response_model=Dict[str, Any])
async def get_demo_dataset(region: str):
    """
    Returns authentic Indian regional demo datasets.
    Supports built-in disk JSONs (Karnataka, Maharashtra, Pan-India) as well as
    high-precision models for all Indian states.
    """
    normalized = region.lower().strip().replace("-", "_").replace(" ", "_")
    filename = f"{normalized}_demand.json"
    filepath = os.path.join(DEMO_DIR, filename)

    # 1. Primary: load from pre-existing demo JSON files if present
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to load demo dataset: {str(e)}")

    # 2. Secondary: load from comprehensive Indian state catalogue
    if normalized in INDIAN_STATE_DATASETS:
        return INDIAN_STATE_DATASETS[normalized]

    # Normalize alias matching
    alias_map = {
        "tamilnadu": "tamil_nadu",
        "uttarpradesh": "uttar_pradesh",
        "up": "uttar_pradesh",
        "tn": "tamil_nadu",
        "delhi": "delhi_ncr",
        "ncr": "delhi_ncr",
        "haryana": "delhi_ncr",
        "madhyapradesh": "madhya_pradesh",
        "mp": "madhya_pradesh",
        "andhra": "andhra_pradesh",
        "ap": "andhra_pradesh",
        "bihar": "bihar_jharkhand",
        "jharkhand": "bihar_jharkhand",
        "westbengal": "west_bengal",
        "bengal": "west_bengal",
        "northeast": "assam_northeast",
        "assam": "assam_northeast"
    }
    if normalized in alias_map and alias_map[normalized] in INDIAN_STATE_DATASETS:
        return INDIAN_STATE_DATASETS[alias_map[normalized]]

    available = [
        "karnataka", "maharashtra", "pan_india",
        "tamil_nadu", "gujarat", "uttar_pradesh", "rajasthan",
        "telangana", "andhra_pradesh", "kerala", "west_bengal",
        "delhi_ncr", "madhya_pradesh", "punjab", "bihar_jharkhand",
        "odisha", "assam_northeast"
    ]
    raise HTTPException(
        status_code=404, 
        detail=f"Demo dataset for '{region}' not found. Available Indian regional datasets: {available}"
    )

