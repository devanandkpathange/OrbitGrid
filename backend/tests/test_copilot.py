"""
Unit tests for AI Logistics Copilot & Custom LLM Connector.
"""

import unittest
from fastapi.testclient import TestClient
from backend.main import app
from backend.core.config import settings


class TestAICopilot(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_copilot_fallback_query(self):
        response = self.client.post(
            "/api/copilot/chat",
            json={
                "question": "Why should we co-serve Delhi and Jaipur?",
                "context": {
                    "warehouses": [{"id": "WH1", "name": "Neemrana Hub"}],
                    "demand_points": [{"id": "delhi", "name": "Delhi"}, {"id": "jaipur", "name": "Jaipur"}],
                    "metrics": {"total_cost": 250000, "average_distance": 110}
                }
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Neemrana", data["answer"])
        self.assertIn("source", data)
        self.assertTrue(len(data["key_takeaways"]) > 0)

    def test_copilot_config_keys(self):
        # Test configuring custom LLM URL
        response = self.client.post(
            "/api/config/keys",
            json={"custom_llm_url": "http://localhost:8001/chat"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["custom_llm_configured"])
        self.assertEqual(data["custom_llm_url"], "http://localhost:8001/chat")

        # Test getting config status
        get_resp = self.client.get("/api/config/keys")
        self.assertEqual(get_resp.status_code, 200)
        get_data = get_resp.json()
        self.assertTrue(get_data["custom_llm_configured"])
        self.assertEqual(get_data["mode"], "Custom LLM Connected")

        # Clean up settings
        settings.CUSTOM_LLM_URL = None


if __name__ == "__main__":
    unittest.main()
