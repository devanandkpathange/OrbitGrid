"""
NLP & Semantic Supply Chain Classifier.
Analyzes arbitrary free-text user business descriptions (e.g. 'organic jaggery export',
'solar panel assembly', 'leather footwear', 'cold-pressed oils', 'heavy engineering',
'textile spinning mill', 'drone testing', 'ayurvedic pharmaceuticals')
and deduces supply chain archetypes, siting criteria, and recommended Indian corridors.
"""

import re
from typing import Dict, Any, List

# Comprehensive Indian Supply Chain Archetype Definitions
ARCHETYPES: Dict[str, Dict[str, Any]] = {
    "resource_anchored_agro": {
        "archetype": "Resource-Anchored (Agro, Sugar & Commodity Processing)",
        "keywords": [
            "sugar", "sugarcane", "cane", "jaggery", "agro", "farm", "crop", "grain", "wheat",
            "rice", "paddy", "cotton", "oilseed", "soybean", "coffee", "tea", "spices", "fertilizer",
            "biomass", "ethanol", "distillery", "timber", "wood", "paper", "pulp", "flour", "mill",
            "plantation", "tobacco", "coir", "rubber", "arecanut", "cashew"
        ],
        "siting_criteria": [
            "Raw material catchment proximity (< 40 km) to prevent post-harvest sucrose/weight degradation",
            "Heavy commercial multi-axle freight highway access (minimum 2-lane NH/SH)",
            "Perennial groundwater or canal irrigation basin access for continuous washdown/steam",
            "Cost-effective rural/semi-urban leasing benchmarks (₹10 - ₹16 / sqft/month)"
        ],
        "preferred_zones": [
            {"name": "Mandya - Cauvery Sugarcane & Agro Belt", "state": "Karnataka", "lat": 12.5218, "lng": 76.8951, "reason": "High-density sugarcane & agro acreage with NH-275 10-lane expressway access", "typical_rent_sqft": 13.5},
            {"name": "Belagavi - Sankeshwar Sugar & Grain Corridor", "state": "Karnataka", "lat": 16.2625, "lng": 74.4820, "reason": "Premier cooperative agro-processing cluster bordering Maharashtra on NH-48", "typical_rent_sqft": 13.0},
            {"name": "Kolhapur - Panchaganga Sugar & Agro Heartland", "state": "Maharashtra", "lat": 16.7050, "lng": 74.2433, "reason": "High sucrose recovery sugarcane belt with established co-op mills", "typical_rent_sqft": 15.5},
            {"name": "Bagalkot - Mudhol - Sameerwadi Agro Corridor", "state": "Karnataka", "lat": 16.1853, "lng": 75.6968, "reason": "Integrated sugar, bagasse cogen & distillery industrial complexes", "typical_rent_sqft": 12.0},
            {"name": "Shivamogga - Bhadravati Agro & Arecanut Cluster", "state": "Karnataka", "lat": 13.9299, "lng": 75.5681, "reason": "Central Malnad agricultural commodity trading & processing gateway", "typical_rent_sqft": 14.0}
        ]
    },
    "textiles_garments_apparel": {
        "archetype": "Textile, Garments & Apparel Manufacturing",
        "keywords": [
            "textile", "textiles", "garment", "garments", "apparel", "fabric", "cloth", "yarn",
            "spinning", "weaving", "dyeing", "knitting", "hosiery", "saree", "silk", "handloom",
            "powerloom", "cotton ginning", "jeans", "denim", "synthetic fibers"
        ],
        "siting_criteria": [
            "Proximity to specialized spinning, dyeing, or garment stitching labor clusters",
            "Common Effluent Treatment Plant (CETP) availability and high-volume industrial water",
            "High container-freight highway connectivity toward container ports (JNPT, Chennai, Tuticorin)",
            "Moderate industrial warehouse lease rates (₹14 - ₹20 / sqft/month)"
        ],
        "preferred_zones": [
            {"name": "Tirupur - Coimbatore Knitwear & Spinning Corridor", "state": "Tamil Nadu", "lat": 11.1085, "lng": 77.3411, "reason": "India's premier knitwear export capital with global freight forwarding ecosystem", "typical_rent_sqft": 17.0},
            {"name": "Surat - Navsari Synthetic & Silk Textile Belt", "state": "Gujarat", "lat": 21.1702, "lng": 72.8311, "reason": "National powerloom, weaving and man-made fabric manufacturing capital", "typical_rent_sqft": 19.0},
            {"name": "Ichalkaranji Textile Hub (Manchester of Maharashtra)", "state": "Maharashtra", "lat": 16.6944, "lng": 74.4608, "reason": "Dense spinning, sizing and decentralized weaving cluster on NH-166", "typical_rent_sqft": 14.5},
            {"name": "Doddaballapur Integrated Textile Park (KIADB)", "state": "Karnataka", "lat": 13.2980, "lng": 77.5350, "reason": "Modern apparel manufacturing SEZ north of Bengaluru with airport proximity", "typical_rent_sqft": 21.0}
        ]
    },
    "cold_chain_perishable": {
        "archetype": "Temperature-Controlled (Cold-Chain, Dairy & Perishables)",
        "keywords": [
            "milk", "dairy", "cheese", "ice cream", "frozen", "meat", "poultry", "seafood",
            "fish", "prawn", "shrimp", "vaccine", "biologics", "fruit", "fruits",
            "vegetable", "vegetables", "horticulture", "flower", "cold storage", "cold chain",
            "reefer", "ice", "juice", "beverage", "pulp", "paste"
        ],
        "siting_criteria": [
            "Uninterrupted 24x7 high-tension industrial power feeder with dual grid/generator backup",
            "Direct egress to cold-chain reefer staging zones and signal-free national expressways",
            "Multi-temperature zone warehousing capability (Ambient 15-25°C, Chilled 2-8°C, Deep Freeze -20°C)",
            "Proximity to major urban consuming metros or deep-sea export container terminals"
        ],
        "preferred_zones": [
            {"name": "Baikampady Port Marine & Cold-Chain SEZ", "state": "Karnataka", "lat": 12.9460, "lng": 74.8210, "reason": "Direct NH-66 and New Mangalore Port tarmac for coastal seafood/cold exports", "typical_rent_sqft": 22.0},
            {"name": "Kolar - Chintamani Horticulture & Dairy Cluster", "state": "Karnataka", "lat": 13.1367, "lng": 78.1291, "reason": "Massive milk union (KOMUL) and cold storage corridor supplying Bengaluru metro", "typical_rent_sqft": 16.0},
            {"name": "Taloja & Navi Mumbai Cold-Chain Hub", "state": "Maharashtra", "lat": 19.0833, "lng": 73.1167, "reason": "Premier reefer logistics gateway feeding Mumbai MMR and JNPT port container gates", "typical_rent_sqft": 29.0},
            {"name": "Shamshabad Temperature-Controlled Cargo SEZ", "state": "Telangana", "lat": 17.2403, "lng": 78.4294, "reason": "Dedicated cold tarmac pharma & perishable air-freight corridors", "typical_rent_sqft": 26.0}
        ]
    },
    "pharma_biotech_chemicals": {
        "archetype": "Pharmaceuticals, APIs & Specialty Chemicals",
        "keywords": [
            "pharma", "pharmaceutical", "medicine", "drug", "drugs", "api", "formulation",
            "chemical", "chemicals", "petrochemical", "biotech", "biotechnology", "laboratory",
            "solvent", "paint", "pigment", "reagent", "ayurvedic", "herbal", "wellness",
            "cosmetic", "polymer", "resin"
        ],
        "siting_criteria": [
            "Pre-designated Chemical / Bulk Drug Industrial Zone with statutory environmental clearances",
            "Hazardous material containment, fire-suppression systems, and explosion-proof staging",
            "Temperature-monitored clean-room grade warehouse construction (USFDA/WHO compliant)",
            "Access to accredited testing laboratories and bonded international air-cargo facilities"
        ],
        "preferred_zones": [
            {"name": "Hyderabad Pharma City & Genome Valley SEZ", "state": "Telangana", "lat": 17.0850, "lng": 78.6040, "reason": "World's largest integrated pharmaceutical & bulk drug manufacturing ecosystem", "typical_rent_sqft": 26.0},
            {"name": "Ankleshwar - Dahej PCPIR Chemical Belt", "state": "Gujarat", "lat": 21.6264, "lng": 73.0032, "reason": "National petroleum, chemicals and petrochemical investment region on NH-48", "typical_rent_sqft": 20.0},
            {"name": "Bommasandra - Jigani Industrial Area (KIADB)", "state": "Karnataka", "lat": 12.8163, "lng": 77.6917, "reason": "South Bengaluru biopharma, medical device and formulation corridor", "typical_rent_sqft": 27.5},
            {"name": "Tarapur MIDC Chemical Zone", "state": "Maharashtra", "lat": 19.8333, "lng": 72.7000, "reason": "Maharashtra's largest chemical & API processing cluster on the Mumbai-Gujarat line", "typical_rent_sqft": 22.0}
        ]
    },
    "heavy_industrial_oem": {
        "archetype": "Heavy Engineering, Automotive & OEM Manufacturing",
        "keywords": [
            "auto", "automobile", "automotive", "car", "bike", "truck", "electric vehicle", "ev",
            "battery", "motor", "engine", "gear", "metal", "steel", "iron", "casting", "forging",
            "machinery", "heavy equipment", "aerospace", "defense", "hardware", "tooling",
            "fabrication", "welding", "chassis", "crane", "transmission", "aluminium"
        ],
        "siting_criteria": [
            "Heavy industrial floor load-bearing capacity (> 6 to 10 tonnes / m²)",
            "Wide turning radiuses and high-bay clearance for 40ft multi-axle freight trailers",
            "High-tension 11kV/33kV industrial power substation connectivity",
            "Proximity to tier-1 automotive OEM mother plants and vendor component clusters"
        ],
        "preferred_zones": [
            {"name": "Chakan - Talegaon MIDC Auto Corridor", "state": "Maharashtra", "lat": 18.7597, "lng": 73.8569, "reason": "Western India's premier auto & heavy engineering ecosystem hosting global OEMs", "typical_rent_sqft": 27.0},
            {"name": "Bidadi Industrial Area (KIADB)", "state": "Karnataka", "lat": 12.7981, "lng": 77.3824, "reason": "Major automotive mother-plant hub along the Bengaluru-Mysuru Expressway", "typical_rent_sqft": 25.0},
            {"name": "Sriperumbudur - Oragadam Auto Corridor", "state": "Tamil Nadu", "lat": 12.9675, "lng": 79.9400, "reason": "The 'Detroit of South Asia' with auto, EV and heavy equipment supply chains", "typical_rent_sqft": 28.0},
            {"name": "Vasanthanarasapura NIMZ Mega Industrial Park", "state": "Karnataka", "lat": 13.4350, "lng": 77.0180, "reason": "National Investment & Manufacturing Zone along the Bengaluru-Mumbai Industrial Corridor", "typical_rent_sqft": 18.0}
        ]
    },
    "electronics_semiconductor_tech": {
        "archetype": "Electronics, Hardware, Solar & Clean Tech",
        "keywords": [
            "electronics", "electronic", "semiconductor", "solar", "solar panel", "inverter",
            "pcb", "chip", "mobile", "smartphone", "laptop", "computer", "led", "lighting",
            "telecom", "sensor", "drone", "uav", "robotics", "automation", "clean tech",
            "electricals", "switchgear", "circuit"
        ],
        "siting_criteria": [
            "Dust-controlled, electrostatic discharge (ESD) protected Class-A warehouse facility",
            "High-speed expressway and international air-cargo egress for high-value components",
            "Continuous stabilized three-phase power grid with voltage surge protection",
            "Access to skilled technical testing, assembly, and quality inspection workforce"
        ],
        "preferred_zones": [
            {"name": "Whitefield & Electronic City Tech Corridor", "state": "Karnataka", "lat": 12.9698, "lng": 77.7499, "reason": "India's premier high-tech hardware, R&D and electronics testing corridor", "typical_rent_sqft": 30.0},
            {"name": "Noida - Greater Noida Electronics & EV Manufacturing Zone", "state": "Uttar Pradesh", "lat": 28.5355, "lng": 77.3910, "reason": "North India's largest mobile assembly, semiconductor and solar inverter hub", "typical_rent_sqft": 26.0},
            {"name": "Sriperumbudur Electronics SEZ", "state": "Tamil Nadu", "lat": 12.9675, "lng": 79.9400, "reason": "Global smartphone and electronics contract manufacturing corridor", "typical_rent_sqft": 28.5},
            {"name": "Dabaspet Industrial Area (KIADB)", "state": "Karnataka", "lat": 13.2300, "lng": 77.2400, "reason": "Major electricals, switchgear and solar mounting hardware cluster on NH-48", "typical_rent_sqft": 20.0}
        ]
    },
    "building_materials_ceramics": {
        "archetype": "Building Materials, Ceramics, Steel & Construction",
        "keywords": [
            "tiles", "tile", "ceramic", "ceramics", "sanitaryware", "cement", "concrete",
            "brick", "stone", "granite", "marble", "sand", "gravel", "glass", "pipe", "pipes",
            "plumbing", "pvc", "plywood", "laminate", "roofing", "structural steel", "tmt"
        ],
        "siting_criteria": [
            "High structural floor capacity and outdoor unpaved yard staging for heavy bulk stock",
            "Direct connectivity to dedicated Indian Railway freight sidings or bulk mineral corridors",
            "Tolerant industrial zoning for noise, dust, and continuous heavy vehicle movement",
            "Low-cost, large-footprint land availability (₹12 - ₹18 / sqft/month)"
        ],
        "preferred_zones": [
            {"name": "Morbi Ceramic Mega Cluster", "state": "Gujarat", "lat": 22.8120, "lng": 70.8384, "reason": "Produces over 70% of India's ceramic tiles and sanitaryware with direct Kandla port links", "typical_rent_sqft": 14.0},
            {"name": "Toranagallu - Ballari Steel & Metal Cluster", "state": "Karnataka", "lat": 15.1950, "lng": 76.6570, "reason": "Heavy iron, TMT rebar and structural steel manufacturing heartland", "typical_rent_sqft": 12.5},
            {"name": "Nagpur Butibori MIDC Heavy Industrial Zone", "state": "Maharashtra", "lat": 20.9200, "lng": 78.9800, "reason": "Zero-mile geographical center of India for national bulk construction goods distribution", "typical_rent_sqft": 16.5},
            {"name": "Tumakuru Industrial Hub (NH-48)", "state": "Karnataka", "lat": 13.3379, "lng": 77.1010, "reason": "Cement, precast and granite processing corridor feeding the Bengaluru urban boom", "typical_rent_sqft": 17.0}
        ]
    },
    "leather_footwear_handicrafts": {
        "archetype": "Leather, Footwear, Handicrafts & Artisanal Goods",
        "keywords": [
            "leather", "footwear", "shoes", "shoe", "boot", "sandals", "tanning", "tannery",
            "handicraft", "handicrafts", "brassware", "pottery", "carpet", "rug", "woodcraft",
            "bamboo", "cane furniture", "artisanal", "hand-made", "leather goods", "belts", "bags"
        ],
        "siting_criteria": [
            "Proximity to traditional artisan and specialized leather finishing clusters",
            "Compliance with environmental effluent norms (CETP connections for tanning)",
            "Finished goods bonded warehouse facilities with dry packaging humidity controls",
            "High container transport road links to key Indian export ports"
        ],
        "preferred_zones": [
            {"name": "Ambur - Ranipet - Vaniyambadi Leather Cluster", "state": "Tamil Nadu", "lat": 12.7907, "lng": 78.7166, "reason": "Accounts for 60% of India's finished leather exports on the Bengaluru-Chennai axis", "typical_rent_sqft": 16.0},
            {"name": "Kanpur Jajmau Leather & Footwear Belt", "state": "Uttar Pradesh", "lat": 26.4499, "lng": 80.3319, "reason": "North India's traditional leather manufacturing and safety footwear capital", "typical_rent_sqft": 15.0},
            {"name": "Agra Footwear Manufacturing Hub", "state": "Uttar Pradesh", "lat": 27.1767, "lng": 78.0081, "reason": "India's largest domestic footwear production cluster with NH-19 connectivity", "typical_rent_sqft": 18.0}
        ]
    },
    "market_anchored_retail": {
        "archetype": "Market-Anchored (Consumer Retail, E-Commerce & FMCG)",
        "keywords": [
            "clothing", "apparel", "garment", "fashion", "shoes", "footwear", "fmcg", "grocery",
            "ecommerce", "e-commerce", "retail", "consumer goods", "home decor", "furniture",
            "parcels", "packages", "courier", "logistics", "3pl", "fulfillment", "quick commerce",
            "dark store", "hyperlocal", "personal care", "cosmetics", "packaged foods", "beverages"
        ],
        "siting_criteria": [
            "Strategic expressway ring road / bypass location for same-day urban ingress without city entry bans",
            "Grade-A fulfillment specifications (dock levelers, 12m clear height, high dock door ratio)",
            "Proximity to high-density consumer purchasing clusters (Tier-1 and Tier-2 urban metros)",
            "Access to last-mile delivery 2-wheeler and EV van staging infrastructure"
        ],
        "preferred_zones": [
            {"name": "Nelamangala - Dabaspet Logistics Hub (NH-48)", "state": "Karnataka", "lat": 13.0970, "lng": 77.3920, "reason": "Bengaluru's primary fulfillment gateway connecting western & northern regions", "typical_rent_sqft": 24.5},
            {"name": "Hosakote KIADB Logistics Park", "state": "Karnataka", "lat": 13.0722, "lng": 77.7981, "reason": "Access to Whitefield, East Bengaluru, and Bengaluru-Chennai Expressway (NE-7)", "typical_rent_sqft": 26.0},
            {"name": "Bhiwandi Mega Warehousing Belt", "state": "Maharashtra", "lat": 19.2967, "lng": 73.0631, "reason": "Round-the-clock heavy commercial truck operations serving Mumbai MMR & Western India", "typical_rent_sqft": 32.0},
            {"name": "Farukhnagar & Bilaspur Logistics Belt", "state": "Haryana / NCR", "lat": 28.4500, "lng": 76.8200, "reason": "Premier mega-fulfillment hub on KMP Expressway feeding Delhi NCR", "typical_rent_sqft": 26.5}
        ]
    }
}


def analyze_user_business(user_input: str) -> Dict[str, Any]:
    """
    Parses arbitrary user business text and produces tailored supply-chain intelligence.
    Works for ANY user input string.
    """
    cleaned = (user_input or "").strip().lower()
    if not cleaned:
        cleaned = "general commerce and retail distribution"

    # Score each archetype against input keywords
    scores = {}
    for key, data in ARCHETYPES.items():
        score = 0
        for kw in data["keywords"]:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, cleaned):
                score += 3
            elif kw in cleaned:
                score += 1
        scores[key] = score

    best_key = max(scores, key=scores.get)
    # If no match, intelligently determine whether it sounds like raw-material or consumer market
    if scores[best_key] == 0:
        if any(term in cleaned for term in ["farm", "extract", "raw", "bulk", "mine", "crude", "heavy", "plant"]):
            best_key = "resource_anchored_agro"
        elif any(term in cleaned for term in ["chip", "circuit", "tech", "digital", "data", "device"]):
            best_key = "electronics_semiconductor_tech"
        elif any(term in cleaned for term in ["clean", "wash", "soap", "eat", "drink", "food"]):
            best_key = "fmcg_packaged_goods"
        else:
            best_key = "market_anchored_retail"

    matched = ARCHETYPES.get(best_key, ARCHETYPES["market_anchored_retail"])
    business_title = (user_input or "General Supply Chain").strip().title()

    # Generate dynamic summary
    summary = (
        f"For '{business_title}', our model identifies a {matched['archetype']} profile. "
        f"Key priorities: {matched['siting_criteria'][0]}. "
        f"Recommended strategy: place logistics nodes in designated industrial corridors with direct highway infrastructure."
    )

    return {
        "user_query": user_input,
        "archetype_key": best_key,
        "business_category": matched["archetype"],
        "summary": summary,
        "siting_criteria": matched["siting_criteria"],
        "recommended_zones": matched["preferred_zones"]
    }
