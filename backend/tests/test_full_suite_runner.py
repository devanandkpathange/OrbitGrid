"""
Exhaustive Automated Test Suite Runner for GridPoint.
Exercises every endpoint, dataset, business profile, and AI Copilot feature.
"""

import unittest
import json
import os
from fastapi.testclient import TestClient
from backend.main import app

class FullApplicationExhaustiveTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    # ==========================================
    # 1. SYSTEM & HEALTH ENDPOINTS
    # ==========================================
    def test_01_health_and_info(self):
        r = self.client.get("/api/health")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json().get("status"), "healthy")

        r_info = self.client.get("/api/info")
        self.assertEqual(r_info.status_code, 200)
        self.assertIn("GridPoint", r_info.json().get("system"))

    def test_02_dashboard_html_serving(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("text/html", r.headers.get("content-type", ""))
        self.assertIn("GridPoint", r.text)
        self.assertIn("AI Copilot", r.text)
        self.assertIn("leaflet", r.text.lower())

        r_dash = self.client.get("/dashboard")
        self.assertEqual(r_dash.status_code, 200)
        self.assertEqual(r.text, r_dash.text)

    # ==========================================
    # 2. DEMO DATASETS & SAMPLE FILES
    # ==========================================
    def test_03_demo_datasets_loading(self):
        for region in ["karnataka", "maharashtra", "pan_india"]:
            r = self.client.get(f"/api/demo/{region}")
            self.assertEqual(r.status_code, 200, f"Failed for demo region: {region}")
            data = r.json()
            self.assertIn("demand_points", data)
            self.assertGreater(len(data["demand_points"]), 0)

        # Sample CSVs endpoint
        r_csvs = self.client.get("/api/demo/sample-csvs")
        self.assertEqual(r_csvs.status_code, 200)
        csv_list = r_csvs.json()
        self.assertIsInstance(csv_list, list)
        self.assertGreater(len(csv_list), 0)

        # Test download of each sample CSV
        for csv_meta in csv_list:
            fname = csv_meta.get("filename") or csv_meta.get("name")
            if fname:
                r_dl = self.client.get(f"/api/demo/download/{fname}")
                self.assertEqual(r_dl.status_code, 200, f"Download failed for {fname}")

    # ==========================================
    # 3. SEARCH & GEOCODING
    # ==========================================
    def test_04_search_queries(self):
        queries = [
            "Peenya",
            "Bhiwandi",
            "Neemrana",
            "Sriperumbudur",
            "560058",
            "Whitefield",
            "Nelamangala",
            "Navi Mumbai"
        ]
        for q in queries:
            r = self.client.get(f"/api/search?q={q}")
            self.assertEqual(r.status_code, 200, f"Search failed for {q}")
            res = r.json()
            self.assertIsInstance(res, list)
            self.assertGreater(len(res), 0, f"Expected search results for {q}")

    # ==========================================
    # 4. INDUSTRIAL HUBS QUERY
    # ==========================================
    def test_05_industrial_hubs(self):
        for reg in ["karnataka", "maharashtra", "pan_india", "all"]:
            r = self.client.get(f"/api/hubs?region={reg}")
            self.assertEqual(r.status_code, 200)
            hubs = r.json()
            self.assertIsInstance(hubs, list)
            self.assertGreater(len(hubs), 0)
            for h in hubs:
                self.assertIn("lat", h)
                self.assertIn("lng", h)
                self.assertIn("name", h)

    # ==========================================
    # 5. NLP BUSINESS CLASSIFIER
    # ==========================================
    def test_06_business_classifier(self):
        cases = [
            {
                "description": "We are a quick-commerce grocery delivery startup in Bangalore with 15-minute SLA",
                "expected_category": "qcommerce"
            },
            {
                "description": "We manufacture heavy automotive components and machinery parts in Pune",
                "expected_category": "automotive"
            },
            {
                "description": "Cold-chain pharmaceutical delivery for temperature sensitive vaccine distribution across India",
                "expected_category": "pharma"
            },
            {
                "description": "Direct to consumer online fashion retail clothing brand",
                "expected_category": "ecommerce"
            },
            {
                "description": "Fresh sugarcane harvest and agro processing cooperative in Mandya",
                "expected_category": "agro"
            }
        ]
        for c in cases:
            r = self.client.post("/api/analyze-business", json={"business_description": c["description"]})
            self.assertEqual(r.status_code, 200)
            data = r.json()
            self.assertIn("business_category", data)
            self.assertIn("summary", data)
            self.assertIn("siting_criteria", data)
            self.assertIn("recommended_zones", data)
            self.assertGreater(len(data["recommended_zones"]), 0)

    # ==========================================
    # 6. DOCUMENT PARSING & UPLOADS
    # ==========================================
    def test_07_document_parsing(self):
        csv_content = (
            "city,demand,lat,lng\n"
            "Bengaluru,50000,12.9716,77.5946\n"
            "Mysuru,20000,12.2958,76.6394\n"
            "Mangaluru,15000,12.9141,74.8560\n"
        )
        files = {"file": ("demand.csv", csv_content.encode("utf-8"), "text/csv")}
        r = self.client.post("/api/upload-document", files=files)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("demand_points", data)
        self.assertEqual(len(data["demand_points"]), 3)

        # JSON upload test
        json_content = json.dumps([
            {"name": "Delhi", "lat": 28.6139, "lng": 77.2090, "demand": 40000},
            {"name": "Jaipur", "lat": 26.9124, "lng": 75.7873, "demand": 25000}
        ])
        files_json = {"file": ("network.json", json_content.encode("utf-8"), "application/json")}
        r_json = self.client.post("/api/upload-document", files=files_json)
        self.assertEqual(r_json.status_code, 200)
        self.assertEqual(len(r_json.json()["demand_points"]), 2)

    # ==========================================
    # 7. OPTIMIZATION RUNS WITH DIVERSE NETWORKS
    # ==========================================
    def test_08_optimization_pan_india_delhi_jaipur_mumbai_chennai(self):
        payload = {
            "demand_points": [
                {"id": "D1", "name": "Delhi NCR", "lat": 28.6139, "lng": 77.2090, "demand": 50000},
                {"id": "D2", "name": "Jaipur", "lat": 26.9124, "lng": 75.7873, "demand": 30000},
                {"id": "D3", "name": "Mumbai", "lat": 19.0760, "lng": 72.8777, "demand": 60000},
                {"id": "D4", "name": "Chennai", "lat": 13.0827, "lng": 80.2707, "demand": 40000}
            ],
            "warehouse_count": 3,
            "region": "pan_india",
            "constraints": {
                "snap_to_industrial_hubs": True,
                "capacity": 100000,
                "max_radius": 600
            }
        }
        r = self.client.post("/api/optimize", json=payload)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(len(data["warehouses"]), 3)
        self.assertEqual(len(data["assignments"]), 4)

        # Check that Delhi & Jaipur are co-served by one warehouse
        wh_served = {w["name"]: w.get("served_cities", []) for w in data["warehouses"]}
        
        # Verify Farukhnagar/Neemrana or similar NH-48 co-serving Delhi & Jaipur
        delhi_jaipur_co_served = any(
            ("Delhi NCR" in served and "Jaipur" in served) 
            for served in wh_served.values()
        )
        self.assertTrue(delhi_jaipur_co_served, f"Expected Delhi & Jaipur to be co-served. Served maps: {wh_served}")

        # Check reasoning
        for wh in data["warehouses"]:
            self.assertIsNotNone(wh.get("reasoning"))
            self.assertGreater(len(wh["reasoning"]), 15)

    def test_09_optimization_single_warehouse_k1(self):
        payload = {
            "demand_points": [
                {"id": "B1", "name": "Bengaluru", "lat": 12.9716, "lng": 77.5946, "demand": 80000},
                {"id": "M1", "name": "Mysuru", "lat": 12.2958, "lng": 76.6394, "demand": 25000}
            ],
            "warehouse_count": 1,
            "region": "Karnataka",
            "constraints": {"snap_to_industrial_hubs": True}
        }
        r = self.client.post("/api/optimize", json=payload)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(len(data["warehouses"]), 1)
        self.assertEqual(data["metrics"]["warehouses_used"], 1)

    def test_10_optimization_south_india_corridor(self):
        payload = {
            "demand_points": [
                {"id": "BLR", "name": "Bengaluru", "lat": 12.9716, "lng": 77.5946, "demand": 70000},
                {"id": "CHN", "name": "Chennai", "lat": 13.0827, "lng": 80.2707, "demand": 60000},
                {"id": "HYD", "name": "Hyderabad", "lat": 17.3850, "lng": 78.4867, "demand": 50000},
                {"id": "COI", "name": "Coimbatore", "lat": 11.0168, "lng": 76.9558, "demand": 20000},
                {"id": "KOC", "name": "Kochi", "lat": 9.9312, "lng": 76.2673, "demand": 25000}
            ],
            "warehouse_count": 3,
            "region": "pan_india",
            "constraints": {"snap_to_industrial_hubs": True, "capacity": 120000}
        }
        r = self.client.post("/api/optimize", json=payload)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(len(data["warehouses"]), 3)
        self.assertGreater(data["metrics"]["total_cost"], 0)
        self.assertGreater(data["metrics"]["sla_compliance_pct"], 0)

    # ==========================================
    # 8. PARETO / ELBOW ANALYSIS
    # ==========================================
    def test_11_pareto_elbow(self):
        demands = [
            {"id": "D1", "name": "City 1", "lat": 12.97, "lng": 77.59, "demand": 40000},
            {"id": "D2", "name": "City 2", "lat": 12.29, "lng": 76.63, "demand": 20000},
            {"id": "D3", "name": "City 3", "lat": 15.36, "lng": 75.12, "demand": 30000},
            {"id": "D4", "name": "City 4", "lat": 12.91, "lng": 74.85, "demand": 25000}
        ]
        r = self.client.post("/api/elbow", json={"demand_points": demands, "max_k": 3})
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("points", data)
        self.assertIn("recommended_k", data)
        self.assertEqual(len(data["points"]), 3)

    # ==========================================
    # 9. BEFORE VS AFTER BENCHMARK
    # ==========================================
    def test_12_benchmark_before_after(self):
        payload = {
            "demand_points": [
                {"id": "D1", "name": "Bengaluru", "lat": 12.97, "lng": 77.59, "demand": 50000},
                {"id": "D2", "name": "Hubballi", "lat": 15.36, "lng": 75.12, "demand": 30000}
            ],
            "warehouse_count": 2,
            "region": "Karnataka"
        }
        r = self.client.post("/api/benchmark", json=payload)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("before", data)
        self.assertIn("after", data)
        self.assertIn("comparisons", data)
        self.assertIn("summary", data)
        self.assertGreater(len(data["comparisons"]), 0)

    # ==========================================
    # 10. FEASIBILITY & ROI ANALYSIS
    # ==========================================
    def test_13_feasibility_analysis(self):
        payload = {
            "candidate_city": "Peenya",
            "candidate_lat": 13.0285,
            "candidate_lng": 77.5197,
            "demand_points": [
                {"id": "D1", "name": "Bengaluru", "lat": 12.97, "lng": 77.59, "demand": 50000},
                {"id": "D2", "name": "Mysuru", "lat": 12.29, "lng": 76.63, "demand": 20000}
            ],
            "industry": "ecommerce_retail"
        }
        r = self.client.post("/api/feasibility", json=payload)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("candidate_city", data)
        self.assertIn("executive_recommendation", data)
        self.assertIn("demand_metrics", data)
        self.assertIn("logistics_impact", data)
        self.assertIn("mathematical_basis", data)

    # ==========================================
    # 11. AI COPILOT INTERACTIVE Q&A
    # ==========================================
    def test_14_ai_copilot_questions(self):
        questions = [
            "Why co-serve Delhi and Jaipur along the NH-48 corridor?",
            "How should we site warehouses for Mumbai, Pune, and Chennai?",
            "How does a 20% surge in diesel fuel prices affect our delivery costs?",
            "What is the optimal warehouse count tradeoff according to the Pareto elbow curve?",
            "What are the top industrial logistics parks in Karnataka near KIADB?"
        ]
        for q in questions:
            r = self.client.post("/api/copilot/chat", json={
                "question": q,
                "context": {
                    "business_type": "Automotive & Retail",
                    "region": "pan_india"
                }
            })
            self.assertEqual(r.status_code, 200, f"Copilot failed on question: {q}")
            data = r.json()
            self.assertIn("answer", data)
            self.assertGreater(len(data["answer"]), 50)
            self.assertIn("source", data)
            self.assertIn("key_takeaways", data)

    # ==========================================
    # 12. RUNTIME API KEYS CONFIGURATION
    # ==========================================
    def test_15_api_keys_config(self):
        r_get = self.client.get("/api/config/keys")
        self.assertEqual(r_get.status_code, 200)
        self.assertIn("mode", r_get.json())

        r_post = self.client.post("/api/config/keys", json={
            "custom_llm_url": "http://127.0.0.1:8001/chat"
        })
        self.assertEqual(r_post.status_code, 200)
        self.assertTrue(r_post.json()["custom_llm_configured"])

        # Reset it cleanly
        self.client.post("/api/config/keys", json={"custom_llm_url": ""})
    # ==========================================
    # 13. MANUAL DEMAND ENTRY & GEOLOCATION WORKFLOW
    # ==========================================
    def test_16_manual_demand_workflow(self):
        # Simulate user searching for unlisted cities to add manually
        cities_to_add = ["Jaipur", "Lucknow", "Bhopal", "Surat"]
        manual_points = []
        for city in cities_to_add:
            r = self.client.get(f"/api/search?q={city}")
            self.assertEqual(r.status_code, 200)
            res = r.json()
            self.assertGreater(len(res), 0)
            loc = res[0]
            manual_points.append({
                "id": f"manual_{city.lower()}",
                "name": city,
                "lat": loc["lat"],
                "lng": loc["lng"],
                "demand": 25000
            })

        # Run optimization on manually created demand network
        opt_req = {
            "demand_points": manual_points,
            "warehouse_count": 2,
            "region": "pan_india",
            "constraints": {"snap_to_industrial_hubs": True}
        }
        r_opt = self.client.post("/api/optimize", json=opt_req)
        self.assertEqual(r_opt.status_code, 200)
        opt_data = r_opt.json()
        self.assertEqual(len(opt_data["warehouses"]), 2)
        self.assertEqual(len(opt_data["assignments"]), 4)
        self.assertGreater(opt_data["metrics"]["total_cost"], 0)

if __name__ == "__main__":
    unittest.main()
