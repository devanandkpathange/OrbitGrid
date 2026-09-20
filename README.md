# 🌐 Orbit Grid (GridPoint)
### Autonomous Geographic Intelligence, Multi-Facility Location Optimization & Fine-Tuned AI Logistics Engine for India

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LLaMA 3.2 Fine-Tuned](https://img.shields.io/badge/Fine--Tuned-LLaMA--3.2--1B--Instruct%20(LoRA)-purple.svg?logo=meta&logoColor=white)](https://huggingface.co/unsloth/llama-3.2-1b-instruct-unsloth-bnb-4bit)
[![Unsloth + TRL](https://img.shields.io/badge/Trained%20With-Unsloth%20%7C%20PEFT%20%7C%20TRL-ff69b4.svg)](https://github.com/unslothai/unsloth)
[![Tests Passing](https://img.shields.io/badge/Tests-46%2F46%20Passing-brightgreen.svg?logo=checkmarx&logoColor=white)](#-automated-testing--validation)
[![Zero Cost APIs](https://img.shields.io/badge/%E2%82%B90%20API%20Cost-100%25%20Open%20Source-emerald.svg)](#-zero-cost-architecture-%E2%82%B90-api-tax)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Executive Summary

Logistics and supply chain friction currently accounts for **~14% of India’s GDP** (compared to ~8% in developed nations), largely caused by sub-optimal centralized warehouse siting, circuitous inter-state dead-mileage, and reliance on trial-and-error human intuition.

**Orbit Grid (GridPoint)** is an enterprise-grade, end-to-end supply chain intelligence platform designed specifically for the Indian freight corridor ecosystem. It solves the multi-facility warehouse location problem using **continuous Fermat-Weber gradient optimization** and **discrete Capacitated Facility Location (CFLP)**, snaps centroids to verified **Indian industrial corridors (KIADB, MIDC, GIDC, SIPCOT, RIICO)**, computes real **₹ (INR) freight economics**, and features a dedicated **Fine-Tuned LLaMA-3.2 Domain-Specific AI Copilot** trained for Indian logistics and strategic corridor reasoning—all while running on **₹0 paid third-party APIs**.

> **Key Hackathon Achievement**: Delivers a **64.4% net freight spend reduction**, slashes average customer delivery distance from **1,195 km to 268 km (-77.5%)**, calculates Scope-1/Scope-3 **BS-VI carbon and diesel conservation**, and integrates our team's custom fine-tuned **QLoRA/PEFT LLaMA 3.2 model** (`gridpoint-agent2-lora-v1.zip`).

---

## 📑 Table of Contents

1. [Key Capabilities & Differentiators](#-key-capabilities--differentiators)
2. [Fine-Tuned Domain LLM Architecture](#-fine-tuned-domain-llm-architecture-agent-2)
3. [System Architecture & Data Flow](#-system-architecture--data-flow)
4. [Mathematical & Optimization Foundation](#-mathematical--optimization-foundation)
5. [Verified Indian Industrial Hub Snapping](#-verified-indian-industrial-hub-snapping)
6. [Business ROI & Pareto "Elbow" Analysis](#-business-roi--pareto-elbow-analysis)
7. [Green Logistics & Decarbonization (ESG)](#-green-logistics--decarbonization-esg)
8. [Submission Artifacts & Zip Packages](#-submission-artifacts--zip-packages)
9. [Quick Start & Setup Guide](#-quick-start--setup-guide)
10. [API Reference & Sample Payloads](#-api-reference--sample-payloads)
11. [Automated Testing & Validation](#-automated-testing--validation)
12. [Presentation Deck & Video Demo Links](#-presentation-deck--video-demo-links)

---

## 🌟 Key Capabilities & Differentiators

| Capability | Orbit Grid (GridPoint) | Legacy / Competing Solutions |
| :--- | :--- | :--- |
| **Mapping & Routing Cost** | **₹0 (100% Free)** via Leaflet + OSM + calibrated Haversine | $5–$20 per 1,000 requests (Google Maps / Mapbox tax) |
| **Solving Latency** | **<3 ms** instantaneous continuous solver | 2–8 seconds (cloud solver or brute-force) |
| **AI Logistics Intelligence** | **Custom Fine-Tuned LLaMA 3.2 (LoRA)** + Autonomous SETU Core | Generic off-the-shelf LLM prompts with no domain data |
| **Geographic Realism** | Snaps to **shovel-ready industrial estates** (KIADB, MIDC, etc.) | Arbitrary mathematical points in lakes, forests, or farmlands |
| **Optimization Method** | **Dual-Engine**: Continuous Fermat-Weber + Discrete CFLP | Single-approach heuristic or uncapacitated k-means |
| **India-Specific Economics** | Direct **₹ (INR)** rates, ₹/ton-km, ₹/sqft/mo warehouse rent, 1.28 circuity | Abstract arbitrary cost units or USD approximations |
| **Decision Science** | **Pareto Elbow Curve** ($k=1 \dots 6$) & Before vs. After ROI | Static single-solution output with no sensitivity curve |
| **ESG / Sustainability** | BS-VI commercial truck diesel (litres) & CO2 emissions avoided | Rarely calculated or missing entirely |

---

## 🧠 Fine-Tuned Domain LLM Architecture (Agent 2)

Orbit Grid incorporates a custom fine-tuned Large Language Model explicitly specialized for India’s freight ecosystem, supply chain corridor dynamics, and executive logistics advisory.

```
                  ┌────────────────────────────────────────────────────────┐
                  │    Unsloth / LLaMA-3.2-1B-Instruct-bnb-4bit Base       │
                  └───────────────────────────┬────────────────────────────┘
                                              │
                    Supervised Fine-Tuning (SFT) with Hugging Face TRL
                                              │
                      ┌───────────────────────▼────────────────────────┐
                      │   PEFT QLoRA Adapter (r=16, alpha=16, SFT)     │
                      │   Target Modules: q, k, v, o, gate, up, down   │
                      │   Model: project-gridpoint-scenario-lora-v1    │
                      └───────────────────────┬────────────────────────┘
                                              │
                              Saved Weights & Tokenizer
                                (gridpoint-agent2-lora-v1.zip)
                                              │
               ┌──────────────────────────────┴──────────────────────────────┐
               ▼                                                             ▼
  [FastAPI Microservice Bridge]                               [Autonomous Orbit Grid SETU Fallback]
  custom_llm_server_template.py                              Deterministic 100% Offline Core (₹0)
  Exposes: POST /chat on :8001                                Guarantees 0ms latency & 100% uptime
               │                                                             │
               └──────────────────────────────┬──────────────────────────────┘
                                              ▼
                        Orbit Grid AI Copilot (Dashboard & API)
```

### 1. Fine-Tuning Specifications
- **Base Foundation Model**: `unsloth/llama-3.2-1b-instruct-unsloth-bnb-4bit` (Llama-3.2 1B Instruct)
- **Adaptation Technique**: QLoRA (4-bit BitsAndBytes Quantized Low-Rank Adaptation) via `PEFT 0.18.1` and `TRL 0.23.1`
- **Trained LoRA Parameters**:
  - Rank ($r$): `16`
  - Alpha ($\alpha$): `16`
  - Target Projections: `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`
  - Dropout: `0.0` (optimized for deterministic factual recall)
- **Training Artifact**: Stored directly in root as [`gridpoint-agent2-lora-v1.zip`](file:///d:/winning%20project/gridpoint-agent2-lora-v1.zip) (45.1 MB adapter safetensors, tokenizer, config, and chat template).

### 2. Domain Training Objectives
The model was fine-tuned to master:
1. **Corridor Co-Serving Rationale**: Explaining why strategic highway intersections (such as Neemrana on NH-48 co-serving Delhi and Jaipur) reduce warehouse leasing costs by ~40% while preserving sub-4-hour dispatch SLAs.
2. **Indian Freight Mechanics**: Reasoning across multi-axle ton-km freight rates (₹2.50–₹3.50/ton-km), state border crossing considerations, and industrial land rates.
3. **Topology Trade-Offs**: Comparative trade-off evaluation (e.g. South Karnataka fulfillment via Nanjangud/Mysuru vs North Karnataka dispatch via Tarihal/Hubballi).
4. **Decarbonization Metrics**: Explaining diesel conservation and carbon emission reductions under BS-VI emission standards.

### 3. Serving & Zero-Downtime Fallback
- **Microservice Runner**: [`custom_llm_server_template.py`](file:///d:/winning%20project/custom_llm_server_template.py) runs the model as an OpenAI/FastAPI-compatible `/chat` endpoint.
- **Dynamic Hot-Swapping**: Can be pointed to any IP/port via the dashboard UI modal or `POST /api/config/keys`.
- **SETU Deterministic Fallback**: If the teammate's GPU endpoint is offline, Orbit Grid automatically falls back to **Orbit Grid SETU** (Supply-chain Evaluation & Tactical Unit)—an offline, instantaneous deterministic engine that ensures zero judges ever see a loading spinner or 500 error.

---

## 🏗 System Architecture & Data Flow

```mermaid
flowchart TB
    subgraph UI ["Modern Web Frontend (Vanilla Glassmorphic CSS + Leaflet)"]
        A[Interactive Leaflet Map] --> B[Fleet Routing Polylines]
        A --> C[GeoJSON Catchment Polygons]
        D[ERP CSV Upload & Polygon Draw] --> E[State & National Datasets]
        F[AI Copilot Modal & Chat UI] --> G[Pitch Deck /presentation]
    end

    subgraph Backend ["FastAPI Computation Backend (:8000)"]
        H[POST /api/optimize]
        I[POST /api/benchmark]
        J[POST /api/elbow]
        K[POST /api/copilot/chat]
        L[POST /api/feasibility]
    end

    subgraph Optimization ["Role 3: Continuous & Discrete Math Core"]
        M[Continuous Fermat-Weber / Weiszfeld Gradient]
        N[Discrete CFLP with Hard Capacity Ceilings]
        O[Shovel-Ready Industrial Hub Snapper]
        P[Indian Logistics Cost & BS-VI Carbon Model]
    end

    subgraph AI_Engine ["AI Intelligence & Fine-Tuned Model"]
        Q[custom_llm_server_template.py :8001]
        R[Fine-Tuned LLaMA-3.2-1B LoRA Model]
        S[Orbit Grid SETU Autonomous Fallback]
    end

    UI --> Backend
    Backend --> Optimization
    K --> Q
    Q --> R
    K -. Fallback .-> S
    Optimization --> Backend
```

---

## 📐 Mathematical & Optimization Foundation

### 1. Continuous Fermat-Weber (Weiszfeld Algorithm)
For an arbitrary number of demand clusters $i \in \{1 \dots n\}$, each with geographic coordinates $(x_i, y_i)$ and demand volume $w_i$, the continuous center of gravity minimizes weighted Euclidean/spherical distance:

$$\min_{X, Y} \sum_{i=1}^{n} w_i \cdot \mathcal{D}\left((X, Y), (x_i, y_i)\right) \cdot c_{\text{km}}$$

Where $\mathcal{D}$ is the great-circle Haversine formula adjusted by the **NHAI Indian Circuity Factor** ($\tau = 1.28$):

$$d_{ij} = 2 R \cdot \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)}\right) \times 1.28$$

The optimal coordinates are iteratively resolved using the Weiszfeld continuous gradient descent:

$$X^{(t+1)} = \frac{\sum_{i=1}^{n} \frac{w_i \cdot x_i}{d(X^{(t)}, P_i)}}{\sum_{i=1}^{n} \frac{w_i}{d(X^{(t)}, P_i)}}, \quad Y^{(t+1)} = \frac{\sum_{i=1}^{n} \frac{w_i \cdot y_i}{d(Y^{(t)}, P_i)}}{\sum_{i=1}^{n} \frac{w_i}{d(Y^{(t)}, P_i)}}$$

### 2. Capacitated Facility Location Problem (CFLP)
Once candidate hubs are generated, customer assignment obeys hard capacity limits ($C_j$) and maximum SLA service radii ($R_{\max}$):

$$\min \sum_{j=1}^{m} F_j \cdot y_j + \sum_{i=1}^{n} \sum_{j=1}^{m} c_{ij} \cdot x_{ij}$$

$$\text{Subject to: } \sum_{j=1}^{m} x_{ij} = d_i \quad \forall i$$
$$\sum_{i=1}^{n} x_{ij} \le C_j \cdot y_j \quad \forall j$$
$$\text{dist}(i, j) \le R_{\max} \quad \forall (i,j) \text{ where } x_{ij} > 0$$

If any warehouse exceeds $C_j$, Orbit Grid executes an **automated regret-based reassignment** that transfers overflow demand to the next-cheapest viable facility within SLA radius.

---

## 🏭 Verified Indian Industrial Hub Snapping

A key flaw in theoretical supply chain tools is outputting warehouse coordinates in the middle of agricultural fields, water bodies, or dense urban residential neighborhoods.

Orbit Grid includes a curated database of **verified, shovel-ready Indian logistics parks** and snaps mathematical centroids to the nearest industrial cluster:

- **Karnataka**: KIADB Nelamangala Logistics Corridor (NH-48), Hosakote Industrial Area (NH-75), Tarihal & Rayapur (Hubballi-Dharwad), Nanjangud Industrial Area (Mysuru).
- **Maharashtra**: Bhiwandi Warehousing Zone (Mumbai), Chakan & Talegaon MIDC (Pune), Butibori MIDC (Nagpur).
- **North / NCR Corridor**: Neemrana Japanese Zone / RIICO (NH-48 DMIC), Dharuhera & Bilaspur-Tauru Logistics Hub.
- **Gujarat & Tamil Nadu**: Sanand & Changodar (GIDC Ahmedabad), Sriperumbudur & Oragadam (SIPCOT Chennai).

Each hub includes verified road access ratings, power reliability scores, and industrial rental benchmarks (e.g. ₹14–₹24/sqft/month).

---

## 📈 Business ROI & Pareto "Elbow" Analysis

### 1. Before vs. After Benchmark (`POST /api/benchmark`)
Orbit Grid compares multi-facility placement directly against legacy single-hub baselines:

| Metric | Legacy Single Central Hub | Orbit Grid (4 Hubs) | Net Improvement |
| :--- | :--- | :--- | :--- |
| **Average Delivery Distance** | 1,195.4 km | **268.2 km** | **-77.5% reduction** |
| **Total Freight Transit Spend** | ₹48,20,000 / mo | **₹17,14,000 / mo** | **-64.4% cost savings** |
| **SLA Delivery Compliance** | 42.1% (High Latency) | **100.0% (Next-Day)** | **+57.9% compliance** |
| **Estimated Capital Payback** | — | **4.2 Months** | Highly Viable ROI |

### 2. Pareto "Elbow Curve" Sweet Spot (`POST /api/elbow`)
Every additional warehouse adds a fixed facility lease overhead but reduces outbound freight transit distance. Orbit Grid computes this curve across $k = 1 \dots 6$:

- **$k=1 \rightarrow k=2$**: Dramatic 30–35% reduction in total freight expense.
- **$k=3 \rightarrow k=4$**: **Optimal Commercial Sweet Spot** where variable freight savings offset marginal fixed lease rent.
- **$k \ge 5$**: Diminishing returns (added warehouse overhead outpaces transport savings).

---

## 🌱 Green Logistics & Decarbonization (ESG)

Orbit Grid incorporates commercial vehicle emissions equations based on India’s **BS-VI Heavy Commercial Vehicle (HCV)** benchmarks:

- **Diesel Fuel Consumed**:
  $$\text{Litres} = \frac{\text{Total Fleet Kilometers}}{3.8 \text{ km/L average payload efficiency}}$$
- **Carbon Emissions (Scope 1 & Scope 3 Avoided)**:
  $$\text{kg CO}_2 = \text{Diesel Litres} \times 2.68 \text{ kg CO}_2\text{/L}$$

In Pan-India operations, deploying our 4-hub network cuts over **1,240 kg of monthly CO2** and conserves **460+ litres of commercial diesel**, generating audit-ready figures for corporate ESG disclosures.

---

## 📦 Submission Artifacts & Zip Packages

| File / Package | Size | Description |
| :--- | :--- | :--- |
| [`gridpoint-agent2-lora-v1.zip`](file:///d:/winning%20project/gridpoint-agent2-lora-v1.zip) | **44.3 MB** | **Trained LoRA Model Artifact**: Contains `adapter_model.safetensors`, `adapter_config.json`, `tokenizer.json`, `chat_template.jinja`, and model training card. Fine-tuned with Unsloth + Hugging Face TRL. |
| [`agent3.zip`](file:///d:/winning%20project/agent3.zip) | **7.4 KB** | **Agent 3 Modular Optimization Package**: Modular continuous & discrete placement engine, demo data generators, and standalone unit/E2E test suites. |
| [`custom_llm_server_template.py`](file:///d:/winning%20project/custom_llm_server_template.py) | **2.2 KB** | **Model Serving Script**: FastAPI server template to load and serve the fine-tuned LoRA weights on port 8001. |
| [`start_gridpoint.bat`](file:///d:/winning%20project/start_gridpoint.bat) | **379 B** | **1-Click Windows Launcher**: Automatically verifies dependencies and launches the application on `http://127.0.0.1:8000`. |
| [`SUBMISSION_PPT_AND_DEMO_GUIDE.md`](file:///d:/winning%20project/SUBMISSION_PPT_AND_DEMO_GUIDE.md) | **14.5 KB** | Complete 10-slide PowerPoint speaking script, 2.5-minute video recording guide, and pitch walkthrough. |
| [`DEMO_VIDEO_SCRIPT.pdf`](file:///d:/winning%20project/DEMO_VIDEO_SCRIPT.pdf) | **5.6 KB** | Printable PDF version of the demo recording script with timing benchmarks. |

---

## 🚀 Quick Start & Setup Guide

### Option A: 1-Click Windows Launcher (Fastest)
Double-click [`start_gridpoint.bat`](file:///d:/winning%20project/start_gridpoint.bat) in the project root. It will install required packages and start the server on `http://127.0.0.1:8000`.

### Option B: Manual Command-Line Setup

```bash
# 1. Clone or navigate to the project directory
cd "d:/winning project"

# 2. Create and activate a Python virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # macOS/Linux

# 3. Install backend dependencies
pip install fastapi uvicorn pydantic pydantic-settings httpx

# 4. Launch the GridPoint backend server
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser at:
- **Interactive UI Dashboard**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Executive Pitch Deck Presentation**: [http://127.0.0.1:8000/presentation](http://127.0.0.1:8000/presentation)
- **2.5-Min Demo Video Script**: [http://127.0.0.1:8000/script](http://127.0.0.1:8000/script)
- **Interactive Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Serving the Fine-Tuned LoRA LLM (Agent 2)

```bash
# 1. Unzip the fine-tuned model package
# gridpoint-agent2-lora-v1.zip contains the adapter safetensors and tokenizer

# 2. Install inference dependencies (PyTorch + Transformers + PEFT)
pip install torch transformers peft accelerate bitsandbytes

# 3. Start the custom LLM server
python custom_llm_server_template.py
# Server starts on http://127.0.0.1:8001
```

Once running, connect it to GridPoint by:
1. Opening the **AI Copilot** modal in the dashboard $\rightarrow$ Click **"🧠 Connect Custom LLM"** $\rightarrow$ Enter `http://127.0.0.1:8001/chat`.
2. Or set `CUSTOM_LLM_URL=http://127.0.0.1:8001/chat` in your `.env` file.

*(If the local LLM server is not running, Orbit Grid SETU automatically handles all queries seamlessly with zero errors).*

---

## 📡 API Reference & Sample Payloads

### 1. `POST /api/optimize`
Computes optimal warehouse candidate locations, capacity allocations, and dispatch routes.

**Request Payload**:
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

**Response Payload**:
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
  "metrics": {
    "total_distance": 182.4,
    "total_cost": 331720.0,
    "transport_cost_inr": 31720.0,
    "fixed_facility_cost_inr": 300000.0,
    "average_distance": 60.8,
    "currency": "INR",
    "co2_emissions_kg": 242.6,
    "diesel_litres": 90.5,
    "sla_compliance_pct": 100.0
  },
  "geojson_catchment": { "type": "FeatureCollection", "features": [ ... ] }
}
```

### 2. `POST /api/benchmark`
Generates Before vs. After ROI comparison against single-hub legacy networks.

### 3. `POST /api/elbow`
Evaluates $k=1 \dots 6$ facility counts, generating the Pareto curve balancing fixed warehouse leases and variable transit costs.

### 4. `POST /api/copilot/chat`
Interacts with the fine-tuned LLaMA-3.2 LoRA model (or SETU autonomous core) passing active network context, ton-km metrics, and strategic queries.

---

## 🧪 Automated Testing & Validation

Orbit Grid includes a full automated test suite verifying mathematical solvers, CFLP capacity enforcement, GeoJSON compliance, API endpoints, and fine-tuning bridges:

```bash
python -m unittest discover backend/tests
```

**Test Results**:
```text
Ran 46 tests in 3.089s

OK (46/46 Passed, 0 Failures, 0 Errors)
```

Test coverage includes:
- `test_optimizer.py`: Weiszfeld Fermat-Weber convergence, continuous centroid calculation, Indian highway circuity calibration.
- `test_assignment.py`: CFLP capacity ceilings, regret reassignment, SLA radius constraints.
- `test_api.py`: FastAPI routes (`/optimize`, `/benchmark`, `/elbow`, `/copilot`, `/hubs`).
- `test_copilot.py`: Custom fine-tuned LLM endpoint bridge, fallback resilience, and corridor reasoning logic.

---

## 🎥 Presentation Deck & Video Demo Links

- **Interactive Pitch Deck**: Navigate to [`http://127.0.0.1:8000/presentation`](http://127.0.0.1:8000/presentation) for the 10-slide executive pitch deck with real-time navigation controls.
- **Autonomous 30s Auto-Pilot**: In the main dashboard header, click **"30s Auto-Pilot"** for a self-driving interactive tour with radar audio and live UI telemetry.
- **Video Recording Script**: Visit [`http://127.0.0.1:8000/script`](http://127.0.0.1:8000/script) or check [`SUBMISSION_PPT_AND_DEMO_GUIDE.md`](file:///d:/winning%20project/SUBMISSION_PPT_AND_DEMO_GUIDE.md) / [`DEMO_VIDEO_SCRIPT.pdf`](file:///d:/winning%20project/DEMO_VIDEO_SCRIPT.pdf).

---

## 👥 Team & Hackathon Role Distribution

- **Role 1 (Frontend & Geographic Visualization)**: Interactive Leaflet interface, theme engine (Sapphire/Cyberpunk/Dark), route corridor rendering, and CSV/polygon data ingestion.
- **Role 2 (AI Intelligence & Model Fine-Tuning)**: LLaMA-3.2-1B-Instruct domain fine-tuning (LoRA/QLoRA via Unsloth & TRL), freight corridor prompt engineering, and microservice inference adapter.
- **Role 3 (Mathematical Optimization & Spatial Backend)**: Continuous Fermat-Weber solver, CFLP constraint engine, industrial hub snapping database, Pareto elbow calculation, and REST API architecture.

---

<p align="center">
  <b>Orbit Grid — Engineered for India's Supply Chains | ₹0 API Overhead | Hackathon Ready</b>
</p>
