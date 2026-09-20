"""
Integration tests for FastAPI endpoints.
"""

import unittest
from fastapi.testclient import TestClient
from backend.main import app


class TestAPIEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.sample_payload = {
            "demand_points": [
                {"id": "blr", "name": "Bengaluru", "lat": 12.9716, "lng": 77.5946, "demand": 15000},
                {"id": "mys", "name": "Mysuru", "lat": 12.2958, "lng": 76.6394, "demand": 8000},
                {"id": "hub", "name": "Hubballi", "lat": 15.3647, "lng": 75.1240, "demand": 7000}
            ],
            "warehouse_count": 2,
            "objective": "minimize_delivery_cost",
            "region": "Karnataka",
            "constraints": {
                "capacity": None,
                "max_radius": None,
                "snap_to_industrial_hubs": False
            }
        }

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])

        info_resp = self.client.get("/api/info")
        self.assertEqual(info_resp.status_code, 200)
        data = info_resp.json()
        self.assertEqual(data["currency"], "INR (₹)")
        self.assertEqual(data["target_region"], "India")

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_optimize_endpoint(self):
        response = self.client.post("/api/optimize", json=self.sample_payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["warehouses"]), 2)
        self.assertEqual(len(data["assignments"]), 3)
        self.assertIn("metrics", data)
        self.assertEqual(data["metrics"]["currency"], "INR")
        self.assertIn("geojson_catchment", data)

    def test_benchmark_endpoint(self):
        response = self.client.post("/api/benchmark", json=self.sample_payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("before", data)
        self.assertIn("after", data)
        self.assertIn("comparisons", data)
        self.assertIn("summary", data)

    def test_elbow_endpoint(self):
        payload = {
            "demand_points": self.sample_payload["demand_points"],
            "max_k": 3,
            "region": "Karnataka"
        }
        response = self.client.post("/api/elbow", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("recommended_k", data)
        self.assertIn("points", data)
        self.assertIn("executive_summary", data)

    def test_hubs_endpoint(self):
        response = self.client.get("/api/hubs?state=Karnataka")
        self.assertEqual(response.status_code, 200)
        hubs = response.json()
        self.assertGreater(len(hubs), 0)
        self.assertEqual(hubs[0]["state"], "Karnataka")

    def test_demo_dataset_endpoint(self):
        response = self.client.get("/api/demo/karnataka")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["region"], "Karnataka")
        self.assertGreater(len(data["demand_points"]), 10)

    def test_search_endpoint(self):
        response = self.client.get("/api/search?q=Bengaluru")
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertGreater(len(results), 0)
        self.assertIn("lat", results[0])
        self.assertIn("lng", results[0])

    def test_api_keys_endpoint(self):
        response = self.client.get("/api/config/keys")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("mode", data)

    def test_sample_csvs_and_download(self):
        # 1. Test listing sample CSVs
        resp = self.client.get("/api/demo/sample-csvs")
        self.assertEqual(resp.status_code, 200)
        csvs = resp.json()
        self.assertGreaterEqual(len(csvs), 3)
        self.assertEqual(csvs[0]["filename"], "sample_karnataka_retail_demand.csv")

        # 2. Test downloading sample CSV
        download_resp = self.client.get("/api/demo/download/sample_karnataka_retail_demand.csv")
        self.assertEqual(download_resp.status_code, 200)
        self.assertIn("text/csv", download_resp.headers.get("content-type", ""))
        self.assertIn("Bengaluru", download_resp.text)
        self.assertIn("Mandya", download_resp.text)


    def test_copilot_chat(self):
        resp = self.client.post("/api/copilot/chat", json={
            "question": "Why co-serve Delhi and Jaipur together on NH-48?",
            "context": {
                "demand_points": [{"name": "Delhi"}, {"name": "Jaipur"}],
                "warehouses": [{"name": "WH1 - Neemrana Industrial Zone"}],
                "metrics": {"total_cost": 450000}
            }
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("answer", data)
        self.assertIn("source", data)
        self.assertIn("Neemrana", data["answer"])


if __name__ == "__main__":
    unittest.main()
