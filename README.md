# GridPoint — Optimization + Maps Backend (Role 3, India-Focused)

> **Role 3 Specification & Implementation**: Mathematical Optimization & Geographic Intelligence Engine tailored for the Indian logistics and supply chain ecosystem. Operates with **₹0 cost (Zero paid APIs)**, requiring no Google Maps or Mapbox API keys.

---

## 🌟 Key Capabilities & Differentiators

1. **Dual Candidate Placement Engine**:
   - **Continuous Gravity / Weiszfeld Fermat-Weber**: Iterative continuous optimization for single or multi-facility centers of gravity.
   - **Weighted K-Medoids (PAM)**: Discrete combinatorial facility location minimizing total weighted freight transport distance.
   - **Indian Industrial Hub Snapping**: Option to snap mathematical centroids to recognized Indian industrial clusters (e.g., Nelamangala & Hosakote in Bengaluru, Nanjangud in Mysuru, Tarihal in Hubballi, Bhiwandi in Mumbai) with real highway access and verified rental benchmarks.
2. **Capacitated Facility Location (CFLP) & SLA Radius Enforcement**:
   - Hard capacity ceilings per warehouse with automated greedy regret reassignment.
   - Maximum delivery radius constraint (e.g. 150 km same-day delivery across Indian districts).
3. **Indian Logistics Economics & Green Logistics (ESG)**:
   - **₹ (INR) Currency**: Direct freight calculation using base dispatch fee, ₹/km/ton transit rate, handling charges, and monthly fixed warehouse lease overhead.
   - **BS-VI Green Metrics**: Estimates commercial truck diesel consumption (litres) and carbon emissions (kg CO2) avoided.
4. **Pareto "Elbow Curve" What-If Analysis (`POST /api/elbow`)**:
   - Evaluates $k=1$ to $k=6$ warehouses simultaneously to identify the exact commercial sweet spot where fixed warehouse overhead intersects transport savings. Perfect for Agent 2's AI LLM to cite hard numbers.
5. **Before-vs-After Baseline Benchmark (`POST /api/benchmark`)**:
   - Compares the optimized multi-warehouse network against a single legacy central hub, computing exact percentage reductions in freight spend, transit km, and emissions.
6. **Zero-Cost Leaflet Ready GeoJSON & Routing**:
   - Generates curved transit corridor polylines and GeoJSON service catchment polygons (`FeatureCollection`) for Agent 1's Leaflet map.

---

## 🚀 Quick Start

### 1. Run the Backend
From the project root:
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Interactive Swagger Documentation
Open your browser at:
**[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 📡 API Contract Specification

### 1. `POST /api/optimize`
Runs warehouse location optimization and demand assignment.

#### Request Body
```json
{
  "region": "Karnataka",
  "business_type": "clothing",
  "warehouse_count": 2,
  "objective": "minimize_delivery_cost",
  "constraints": {
    "capacity": 35000,
    "max_radius": 250,
    "snap_to_industrial_hubs": true,
    "fixed_warehouse_cost_inr": 150000,
    "freight_rate_per_km_unit_inr": 0.05
  },
  "demand_points": [
    { "id": "blr_south", "name": "Bengaluru South", "lat": 12.8452, "lng": 77.6602, "demand": 14200 },
    { "id": "mysuru", "name": "Mysuru", "lat": 12.2958, "lng": 76.6394, "demand": 8400 },
    { "id": "hubballi", "name": "Hubballi", "lat": 15.3647, "lng": 75.1240, "demand": 9200 }
  ]
}
```

#### Response Body
```json
{
  "warehouses": [
    {
      "id": "WH1",
      "name": "WH1 - Nelamangala Logistics Hub (NH-48 / Tumkur Rd)",
      "lat": 13.097,
      "lng": 77.392,
      "cost": 178520.0,
      "assigned_demand": 22600.0,
      "capacity": 35000.0,
      "utilization_pct": 64.6,
      "fixed_cost_inr": 150000.0,
      "variable_cost_inr": 28520.0
    },
    {
      "id": "WH2",
      "name": "WH2 - Tarihal & Rayapur Industrial Corridor",
      "lat": 15.3905,
      "lng": 75.1051,
      "cost": 153200.0,
      "assigned_demand": 9200.0,
      "capacity": 35000.0,
      "utilization_pct": 26.3,
      "fixed_cost_inr": 150000.0,
      "variable_cost_inr": 3200.0
    }
  ],
  "assignments": [
    {
      "demand_id": "blr_south",
      "demand_name": "Bengaluru South",
      "warehouse_id": "WH1",
      "distance": 45.2,
      "cost": 32252.0,
      "demand_volume": 14200.0,
      "route_geometry": [[13.097, 77.392], [12.971, 77.526], [12.8452, 77.6602]]
    }
  ],
  "metrics": {
    "total_distance": 182.4,
    "total_cost": 331720.0,
    "transport_cost_inr": 31720.0,
    "fixed_facility_cost_inr": 300000.0,
    "average_distance": 60.8,
    "currency": "INR",
    "total_demand": 31800.0,
    "co2_emissions_kg": 242.6,
    "diesel_litres": 90.5,
    "sla_compliance_pct": 100.0,
    "warehouses_used": 2
  },
  "total_cost": 331720.0,
  "geojson_catchment": {
    "type": "FeatureCollection",
    "features": [ ... ]
  }
}
```

---

### 2. `POST /api/benchmark`
Generates Before vs. After comparison for ROI presentation.
```json
{
  "before": { "warehouse_count": 1, "metrics": { ... } },
  "after": { "warehouse_count": 2, "metrics": { ... } },
  "comparisons": [
    {
      "metric": "Delivery Transport Cost",
      "before_value": 482000.0,
      "after_value": 331720.0,
      "unit": "INR (₹)",
      "percentage_change": -31.2,
      "interpretation": "31.2% cost reduction"
    }
  ],
  "summary": "Optimizing to 2 warehouses reduces total delivery cost by 31.2%..."
}
```

---

### 3. `POST /api/elbow`
Returns Pareto curve for $k=1 \dots K$ to substantiate AI recommendations.

---

### 4. `GET /api/demo/{region}`
Returns instant demo datasets (`karnataka`, `maharashtra`, `pan_india`).

---

### 5. `GET /api/hubs?state=Karnataka`
Returns verified Indian industrial warehousing parks (KIADB, MIDC, etc.).

---

## 🧪 Running Automated Tests
```bash
python -m unittest discover backend/tests
```
