"""
India Industry-Specific Supply Chain & Logistics Knowledge Base.
Provides domain-specific sourcing clusters, raw-material belts (e.g. sugarcane farms,
textile clusters, port logistics), and industrial park recommendations.
"""

from typing import Dict, List, Any

INDUSTRY_PROFILES: Dict[str, Dict[str, Any]] = {
    "sugar_agro": {
        "name": "Sugar Mills & Agro-Processing",
        "description": "Requires proximity to sugarcane cultivation belts, perennial water, and rail/highway corridors to minimize cane transit weight loss.",
        "key_factors": ["Cane Sourcing Radius (< 40 km)", "Biomass / Bagasse Cogeneration Access", "Heavy Axle Highway Corridors"],
        "recommended_zones": [
            {
                "cluster": "Mandya - Mysuru Sugar Belt",
                "city": "Mandya",
                "state": "Karnataka",
                "lat": 12.5218,
                "lng": 76.8951,
                "reason": "Known as the 'Sugar City of Karnataka' with high-density sugarcane acreage along Cauvery irrigation basin and NH-275 access.",
                "typical_rent_sqft_inr": 14.0
            },
            {
                "cluster": "Belagavi - Sankeshwar - Athani Belt",
                "city": "Belagavi",
                "state": "Karnataka",
                "lat": 16.2625,
                "lng": 74.4820,
                "reason": "Highest sugar output district in Karnataka with 20+ active co-operative mills, bordering Maharashtra sugarcane belt along NH-48.",
                "typical_rent_sqft_inr": 13.0
            },
            {
                "cluster": "Kolhapur - Sangli - Shirol Belt",
                "city": "Kolhapur",
                "state": "Maharashtra",
                "lat": 16.7050,
                "lng": 74.2433,
                "reason": "Premier sugarcane heartland of Western India with Panchaganga basin mills and high sugar recovery rates (11-12%).",
                "typical_rent_sqft_inr": 16.0
            },
            {
                "cluster": "Bagalkot - Mudhol - Sameerwadi Corridor",
                "city": "Bagalkot",
                "state": "Karnataka",
                "lat": 16.1853,
                "lng": 75.6968,
                "reason": "Major Ghataprabha basin sugarcane cluster hosting integrated sugar, ethanol, and distillery complexes.",
                "typical_rent_sqft_inr": 12.0
            }
        ]
    },
    "ecommerce_retail": {
        "name": "E-Commerce & Quick Commerce",
        "description": "Prioritizes same-day / next-day urban reach, multi-tier fulfillment hubs, and expressway ring roads.",
        "key_factors": ["Grade-A Warehousing with Dock Levelers", "Ring Road (ORR/STRR) Ingress", "Hyper-local Delivery Radius (< 15-25 km)"],
        "recommended_zones": [
            {
                "cluster": "Nelamangala - Dabaspet (NH-48)",
                "city": "Bengaluru",
                "state": "Karnataka",
                "lat": 13.0970,
                "lng": 77.3920,
                "reason": "Bengaluru's primary fulfillment hub connecting western and northern Karnataka via NH-48 and NICE road.",
                "typical_rent_sqft_inr": 25.0
            },
            {
                "cluster": "Hosakote - Narasapura Industrial Belt",
                "city": "Bengaluru",
                "state": "Karnataka",
                "lat": 13.0722,
                "lng": 77.7981,
                "reason": "Direct connectivity to Whitefield, East Bengaluru, and the Bengaluru-Chennai Expressway (NE-7).",
                "typical_rent_sqft_inr": 26.0
            },
            {
                "cluster": "Bhiwandi Logistics Hub",
                "city": "Thane / Mumbai",
                "state": "Maharashtra",
                "lat": 19.2967,
                "lng": 73.0631,
                "reason": "National mega-warehousing cluster serving MMR, South Gujarat, and Pune with round-the-clock heavy vehicle movement.",
                "typical_rent_sqft_inr": 32.0
            }
        ]
    },
    "cold_chain_pharma": {
        "name": "Pharma & Temperature-Controlled Cold Chain",
        "description": "Requires uninterrupted power supply, reefer truck staging, and port/air cargo connectivity.",
        "key_factors": ["24x7 Power Backup Infrastructure", "Reefer Vehicle Fleet Parking", "Near Port/Airport Cargo"],
        "recommended_zones": [
            {
                "cluster": "Baikampady Port Industrial Area",
                "city": "Mangaluru",
                "state": "Karnataka",
                "lat": 12.9460,
                "lng": 74.8210,
                "reason": "Adjacent to New Mangalore Port Trust (NMPT) and coastal marine/seafood export logistics corridor on NH-66.",
                "typical_rent_sqft_inr": 22.0
            },
            {
                "cluster": "Shamshabad Air Cargo Logistics SEZ",
                "city": "Hyderabad",
                "state": "Telangana",
                "lat": 17.2403,
                "lng": 78.4294,
                "reason": "Primary vaccine & bulk drug pharmaceutical cold-chain corridor of India with dedicated temperature-controlled tarmac access.",
                "typical_rent_sqft_inr": 28.0
            }
        ]
    },
    "automotive_heavy": {
        "name": "Automotive, Engineering & Heavy Manufacturing",
        "description": "High floor load-bearing capacity, 40-foot container trailer turning radius, and OEM vendor cluster proximity.",
        "key_factors": ["High Power Substation Access", "Over-Dimensional Cargo (ODC) Movement", "Ancillary Supplier Ecosystem"],
        "recommended_zones": [
            {
                "cluster": "Chakan & Talegaon MIDC",
                "city": "Pune",
                "state": "Maharashtra",
                "lat": 18.7597,
                "lng": 73.8569,
                "reason": "The auto capital hub of Western India with major vehicle manufacturers, auto ancillaries, and NH-60 expressway link.",
                "typical_rent_sqft_inr": 25.0
            },
            {
                "cluster": "Bidadi Industrial Area (KIADB)",
                "city": "Ramanagara / Bengaluru",
                "state": "Karnataka",
                "lat": 12.7981,
                "lng": 77.3824,
                "reason": "Host to major automobile plants and heavy engineering suppliers along the Bengaluru-Mysuru 10-lane Expressway.",
                "typical_rent_sqft_inr": 23.0
            }
        ]
    }
}


def get_industry_recommendations(industry_key: str) -> Dict[str, Any]:
    """
    Returns curated sourcing clusters and industrial parks for a given business type.
    """
    key = industry_key.lower().replace(" ", "_").replace("-", "_")
    for k, profile in INDUSTRY_PROFILES.items():
        if k in key or key in k:
            return profile
    return INDUSTRY_PROFILES["ecommerce_retail"]
