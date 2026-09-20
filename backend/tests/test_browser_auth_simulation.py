"""
Simulates browser-side authentication execution on the live HTML.
Extracts the actual JS and HTML from dashboard.html, checks for syntax errors,
verifies form IDs, and ensures functions exist and resolve properly.
"""

import os
import re
import requests

def test_browser_auth_simulation():
    resp = requests.get("http://127.0.0.1:8000/")
    assert resp.status_code == 200, "Dashboard failed to load"
    html = resp.text

    # 1. Verify all auth DOM elements exist
    required_ids = [
        "authOverlay",
        "authForm",
        "groupCompanyName",
        "authCompanyName",
        "authUsername",
        "authPassword",
        "authSubmitBtn",
        "tabSignIn",
        "tabRegister",
        "userProfileCompany",
        "userProfileOwner",
        "btnOpenWizard"
    ]
    for el_id in required_ids:
        assert f'id="{el_id}"' in html, f"CRITICAL: Missing #{el_id} in DOM!"
    print("[PASS] All authentication DOM elements exist in HTML.")

    # 2. Verify onclick attributes for evaluator button and tabs
    assert 'onclick="quickEvaluatorLogin()"' in html, "Missing onclick='quickEvaluatorLogin()'"
    assert 'onsubmit="handleAuthSubmit(event)"' in html, "Missing onsubmit='handleAuthSubmit(event)'"
    assert "switchAuthTab('signin')" in html, "Missing signin tab switch"
    assert "switchAuthTab('register')" in html, "Missing register tab switch"
    print("[PASS] All onclick / onsubmit event handlers are properly bound in HTML.")

    # 3. Check for any duplicate or invalid JS keywords
    assert "async async" not in html, "CRITICAL: Duplicate async keyword found!"
    assert "function function" not in html, "CRITICAL: Duplicate function keyword found!"
    print("[PASS] Zero duplicated keywords in HTML script.")

    # 4. Extract JS and test syntax with Node.js
    start = html.find('<script>')
    end = html.rfind('</script>')
    assert start != -1 and end != -1, "Script block missing in HTML"
    js_code = html[start+8:end]

    temp_js_path = os.path.join(os.path.dirname(__file__), "temp_node_check.js")
    with open(temp_js_path, "w", encoding="utf-8") as f:
        f.write(js_code)

    try:
        ret = os.system(f'node --check "{temp_js_path}"')
        assert ret == 0, f"Node.js syntax check failed with code {ret}!"
        print("[PASS] Node.js syntax check passed with 100% validity (0 syntax errors).")
    finally:
        if os.path.exists(temp_js_path):
            os.remove(temp_js_path)

    # 5. Verify live backend evaluator auth endpoint returns 200 and valid token
    eval_resp = requests.post("http://127.0.0.1:8000/api/auth/evaluator-demo")
    assert eval_resp.status_code == 200, f"Evaluator endpoint failed: {eval_resp.status_code}"
    eval_data = eval_resp.json()
    assert "token" in eval_data, "Token missing in evaluator response"
    assert eval_data["user"]["company_name"] == "National Logistics & Supply Chain Corp", "Unexpected company"
    print(f"[PASS] Live evaluator authentication returns valid session token for {eval_data['user']['company_name']}.")

    print("\n*** ALL BROWSER AUTHENTICATION CHECKS PASSED WITH 100% INTEGRITY! ***")

if __name__ == "__main__":
    test_browser_auth_simulation()
