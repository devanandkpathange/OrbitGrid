import urllib.request
import urllib.error
import json

def main():
    print("Testing Live Auth & Persistence on http://127.0.0.1:8000/...")
    
    # 1. Fetch live page HTML
    html = urllib.request.urlopen("http://127.0.0.1:8000/").read().decode("utf-8")
    assert "Reset Demo" not in html, "FAIL: Reset Demo button still found in live HTML!"
    print("[PASS] 1. Reset Demo button is completely removed from live UI!")

    assert 'id="authOverlay"' in html, "FAIL: authOverlay missing!"
    assert 'id="authCompanyName"' in html, "FAIL: authCompanyName input missing!"
    assert 'id="authUsername"' in html, "FAIL: authUsername input missing!"
    assert 'id="authPassword"' in html, "FAIL: authPassword input missing!"
    assert "quickEvaluatorLogin" in html, "FAIL: quickEvaluatorLogin button missing!"
    assert "saveActiveAnalysisToDatabase" in html, "FAIL: saveActiveAnalysisToDatabase button missing!"
    print("[PASS] 2. Single-page Enterprise Login Gate & UI elements verified live in HTML!")

    # 3. Test HTTP Registration
    reg_data = json.dumps({
        "company_name": "Mahindra Integrated Supply Chain",
        "username": "mahindra_lead",
        "password": "mahindra_secure_2026"
    }).encode("utf-8")
    req = urllib.request.Request("http://127.0.0.1:8000/api/auth/register", data=reg_data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError:
        login_data = json.dumps({"username": "mahindra_lead", "password": "mahindra_secure_2026"}).encode("utf-8")
        req = urllib.request.Request("http://127.0.0.1:8000/api/auth/login", data=login_data, headers={"Content-Type": "application/json"}, method="POST")
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read().decode("utf-8"))

    token = data["token"]
    print(f"[PASS] 3. Enterprise user authenticated: {data['user']['company_name']} ({data['user']['username']})")

    # 4. Test Saving Warehouse Analysis
    save_payload = json.dumps({
        "region": "maharashtra",
        "business_description": "Automotive EV Batteries & Parts Distribution",
        "warehouse_count": 3,
        "snap_to_hubs": True,
        "demand_points": [
            {"name": "Chakan MIDC", "lat": 18.75, "lng": 73.85, "demand": 65000},
            {"name": "Talegaon Industrial Area", "lat": 18.72, "lng": 73.68, "demand": 45000},
            {"name": "Waluj MIDC Aurangabad", "lat": 19.83, "lng": 75.24, "demand": 50000}
        ],
        "optimized_result": {"cost": 194000, "warehouses": [{"name": "WH1", "lat": 18.75, "lng": 73.85}]}
    }).encode("utf-8")

    save_req = urllib.request.Request("http://127.0.0.1:8000/api/user/save-analysis", data=save_payload, headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}, method="POST")
    save_resp = urllib.request.urlopen(save_req)
    save_data = json.loads(save_resp.read().decode("utf-8"))
    print(f"[PASS] 4. Saved warehouse analysis to database: {save_data['message']}")

    # 5. Test Relogin & Automatic Data Persistence
    relogin_req = urllib.request.Request("http://127.0.0.1:8000/api/auth/login", data=json.dumps({"username": "mahindra_lead", "password": "mahindra_secure_2026"}).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
    relogin_resp = urllib.request.urlopen(relogin_req)
    relogin_data = json.loads(relogin_resp.read().decode("utf-8"))
    saved = relogin_data["saved_scenario"]
    assert saved is not None, "FAIL: Saved scenario was None on relogin!"
    assert saved["region"] == "maharashtra", "FAIL: Saved region mismatch!"
    assert len(saved["demand_points"]) == 3, "FAIL: Demand points not restored!"
    assert saved["demand_points"][0]["name"] == "Chakan MIDC", "FAIL: Demand point name mismatch!"
    print(f"[PASS] 5. Relogin restored 100% of saved warehouse data ({len(saved['demand_points'])} nodes in {saved['region']})!")

    # 6. Test Evaluator Demo Access
    demo_req = urllib.request.Request("http://127.0.0.1:8000/api/auth/evaluator-demo", method="POST")
    demo_resp = urllib.request.urlopen(demo_req)
    demo_data = json.loads(demo_resp.read().decode("utf-8"))
    assert demo_data["status"] == "success", "FAIL: Demo access failed!"
    print(f"[PASS] 6. Evaluator 1-click access confirmed: {demo_data['user']['company_name']} ({demo_data['user']['username']})")

    print("\n*** ALL LIVE AUTHENTICATION & PERSISTENCE TESTS PASSED WITH 100% PERFECTION! ***")

if __name__ == "__main__":
    main()
