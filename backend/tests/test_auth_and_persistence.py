import unittest
from fastapi.testclient import TestClient
from backend.main import app
from backend.db.database import get_connection

class TestAuthAndPersistence(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Clear test users if needed
        with get_connection() as conn:
            conn.cursor().execute("DELETE FROM users WHERE username IN ('test_company_user', 'save_user')")
            conn.commit()

    def test_registration_and_login_flow(self):
        # 1. Register
        reg_payload = {
            "company_name": "Adani Express Logistics",
            "username": "test_company_user",
            "password": "secure_password_2026"
        }
        res = self.client.post("/api/auth/register", json=reg_payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["user"]["company_name"], "Adani Express Logistics")
        token = data["token"]
        self.assertTrue(len(token) > 20)

        # 2. Get Me with Bearer Token
        me_res = self.client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(me_res.status_code, 200)
        me_data = me_res.json()
        self.assertEqual(me_data["user"]["username"], "test_company_user")

        # 3. Log In with valid credentials
        login_payload = {
            "username": "test_company_user",
            "password": "secure_password_2026"
        }
        login_res = self.client.post("/api/auth/login", json=login_payload)
        self.assertEqual(login_res.status_code, 200)
        login_data = login_res.json()
        self.assertEqual(login_data["status"], "success")
        self.assertEqual(login_data["user"]["company_name"], "Adani Express Logistics")

        # 4. Log In with invalid credentials
        bad_login = self.client.post("/api/auth/login", json={"username": "test_company_user", "password": "wrongpassword"})
        self.assertEqual(bad_login.status_code, 401)

    def test_save_and_restore_warehouse_analysis(self):
        # Register user
        reg_payload = {
            "company_name": "Reliance Retail Warehousing",
            "username": "save_user",
            "password": "password123"
        }
        reg_res = self.client.post("/api/auth/register", json=reg_payload)
        token = reg_res.json()["token"]

        # Save custom warehouse analysis
        demand_points = [
            {"name": "Ahmedabad Hub", "lat": 23.02, "lng": 72.57, "demand": 45000},
            {"name": "Surat Hub", "lat": 21.17, "lng": 72.83, "demand": 30000},
            {"name": "Vadodara Hub", "lat": 22.30, "lng": 73.18, "demand": 25000}
        ]
        save_payload = {
            "region": "gujarat",
            "business_description": "Petrochemicals & Retail Distribution",
            "warehouse_count": 2,
            "snap_to_hubs": True,
            "demand_points": demand_points,
            "optimized_result": {
                "total_cost": 284500,
                "warehouses": [{"name": "WH1", "lat": 22.3, "lng": 73.0, "assigned_demand": 100000}]
            },
            "scenario_name": "Gujarat High-Velocity Grid"
        }
        save_res = self.client.post("/api/user/save-analysis", json=save_payload, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(save_res.status_code, 200)
        save_data = save_res.json()
        self.assertEqual(save_data["status"], "success")
        self.assertEqual(save_data["details"]["demand_points_count"], 3)

        # Retrieve saved analysis
        get_res = self.client.get("/api/user/my-analysis", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(get_res.status_code, 200)
        get_data = get_res.json()
        self.assertTrue(get_data["has_saved_analysis"])
        analysis = get_data["analysis"]
        self.assertEqual(analysis["region"], "gujarat")
        self.assertEqual(analysis["warehouse_count"], 2)
        self.assertEqual(len(analysis["demand_points"]), 3)
        self.assertEqual(analysis["demand_points"][0]["name"], "Ahmedabad Hub")

        # Simulate relogin and verify that login payload includes saved scenario
        relogin = self.client.post("/api/auth/login", json={"username": "save_user", "password": "password123"})
        self.assertEqual(relogin.status_code, 200)
        relogin_data = relogin.json()
        self.assertIsNotNone(relogin_data["saved_scenario"])
        self.assertEqual(relogin_data["saved_scenario"]["region"], "gujarat")
        self.assertEqual(len(relogin_data["saved_scenario"]["demand_points"]), 3)

    def test_evaluator_demo_login(self):
        res = self.client.post("/api/auth/evaluator-demo")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["user"]["username"], "evaluator")
        self.assertEqual(data["user"]["company_name"], "National Logistics & Supply Chain Corp")
        self.assertTrue(len(data["token"]) > 20)

if __name__ == "__main__":
    unittest.main()
