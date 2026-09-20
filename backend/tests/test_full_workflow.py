"""
Full end-to-end integration and workflow test suite for GridPoint.
Verifies all capabilities: business profiling, document parsing,
feasibility reporting, geocoding, and optimization math.
"""

import unittest
from fastapi.testclient import TestClient
from backend.main import app


class TestFullWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_dashboard_renders(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("GridPoint", resp.text)
        self.assertIn("wizardModal", resp.text)
        self.assertIn("feasibilityModal", resp.text)
        self.assertIn("docUploadModal", resp.text)
        # Ensure Esri dark gray tile is present (watermark-free)
        self.assertIn("World_Dark_Gray_Base", resp.text)

    def test_analyze_business_open_ended(self):
        # 1. Sugarcane
        r1 = self.client.post("/api/analyze-business", json={"business_description": "Sugarcane processing and ethanol distillery"})
        self.assertEqual(r1.status_code, 200)
        self.assertIn("Agro", r1.json()["business_category"])

        # 2. Textiles
        r2 = self.client.post("/api/analyze-business", json={"business_description": "Cotton yarn spinning mill and apparel garment export"})
        self.assertEqual(r2.status_code, 200)
        self.assertIn("Textile", r2.json()["business_category"])

        # 3. Cold chain
        r3 = self.client.post("/api/analyze-business", json={"business_description": "Frozen seafood, shrimp and cold chain logistics"})
        self.assertEqual(r3.status_code, 200)
        self.assertIn("Cold-Chain", r3.json()["business_category"])

        # 4. Electronics / Solar
        r4 = self.client.post("/api/analyze-business", json={"business_description": "Solar inverter manufacturing, lithium batteries and EV chargers"})
        self.assertEqual(r4.status_code, 200)
        self.assertTrue("Electronics" in r4.json()["business_category"] or "Engineering" in r4.json()["business_category"])

    def test_document_ingestion_csv(self):
        csv_content = (
            "City,Demand\n"
            "Bengaluru,15000\n"
            "Mysuru,8000\n"
            "Mandya,12000\n"
            "Hubballi,9000\n"
            "Belagavi,11000\n"
        )
        files = {"file": ("orders.csv", csv_content.encode("utf-8"), "text/csv")}
        resp = self.client.post("/api/upload-document", files=files)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["points_extracted"], 5)
        self.assertGreater(data["total_demand"], 50000)
        self.assertEqual(data["demand_points"][0]["name"], "Bengaluru")

    def test_document_ingestion_text(self):
        text_content = "Weekly Dispatches: Mandya 14000 tonnes, Belagavi 22000 tonnes, Kolhapur 18000 tonnes, Mysuru 9000 tonnes"
        resp = self.client.post("/api/upload-document", data={"text_content": text_content})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["points_extracted"], 4)
        names = [p["name"] for p in data["demand_points"]]
        self.assertIn("Mandya", names)
        self.assertIn("Belagavi", names)

    def test_feasibility_report(self):
        payload = {
            "candidate_city": "Mandya",
            "candidate_lat": 12.5218,
            "candidate_lng": 76.8951,
            "industry": "Sugarcane refining & jaggery manufacturing",
            "demand_points": [
                {"id": "d1", "name": "Mandya", "lat": 12.52, "lng": 76.89, "demand": 14000},
                {"id": "d2", "name": "Mysuru", "lat": 12.29, "lng": 76.63, "demand": 8000},
                {"id": "d3", "name": "Bengaluru", "lat": 12.97, "lng": 77.59, "demand": 16000}
            ],
            "existing_warehouses": [
                {"name": "Bengaluru Hub", "lat": 12.9716, "lng": 77.5946}
            ]
        }
        resp = self.client.post("/api/feasibility", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("mathematical_basis", data)
        self.assertIn("logistics_impact", data)
        self.assertIn("demand_metrics", data)
        self.assertGreater(data["demand_metrics"]["within_250km_pct"], 90.0)

    def test_search_gazetteer(self):
        cities_to_test = ["Mandya", "Tirupur", "Bhiwandi", "Morbi", "Chakan", "Nelamangala"]
        for city in cities_to_test:
            resp = self.client.get(f"/api/search?q={city}")
            self.assertEqual(resp.status_code, 200)
            results = resp.json()
            self.assertGreater(len(results), 0)
            self.assertIn(city.lower(), results[0]["name"].lower())


if __name__ == "__main__":
    unittest.main()
