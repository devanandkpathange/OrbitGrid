import urllib.request
import json

def main():
    print("Testing Live Dashboard HTML...")
    req = urllib.request.urlopen("http://127.0.0.1:8000/")
    assert req.status == 200
    html = req.read().decode("utf-8")
    
    assert 'id="heroLanding"' in html, "heroLanding missing"
    assert 'id="commandCenter"' in html, "commandCenter missing"
    assert 'tamil_nadu' in html, "tamil_nadu missing"
    assert 'importActiveMapNodesToEditor' in html, "importActiveMapNodesToEditor missing"
    assert 'scrollToCommandCenter' in html, "scrollToCommandCenter missing"
    assert 'Business &amp; Network Setup' in html or 'Business & Network Setup' in html, "Business & Network Setup button missing"
    assert '<div class="badge-free">' not in html, "badge-free must be removed from header"
    print("[PASS] Live HTML has Hero Landing, Command Center, All States, Business Setup button, and free badges removed!")

    print("\nTesting Indian State Demo APIs over HTTP...")
    states = [
        "karnataka", "maharashtra", "pan_india",
        "tamil_nadu", "gujarat", "uttar_pradesh", "rajasthan",
        "telangana", "andhra_pradesh", "kerala", "west_bengal",
        "delhi_ncr", "madhya_pradesh", "punjab", "bihar_jharkhand",
        "odisha", "assam_northeast"
    ]
    for s in states:
        url = f"http://127.0.0.1:8000/api/demo/{s}"
        resp = urllib.request.urlopen(url)
        assert resp.status == 200, f"Failed for {s}"
        data = json.loads(resp.read().decode("utf-8"))
        assert "demand_points" in data and len(data["demand_points"]) > 0
        tot = sum(p['demand'] for p in data['demand_points'])
        print(f"  * {s}: {data['region']} -> {len(data['demand_points'])} nodes ({tot:,} units)")

    print("\n[PASS] ALL LIVE HTTP TESTS PASSED PERFECTLY!")

if __name__ == "__main__":
    main()
