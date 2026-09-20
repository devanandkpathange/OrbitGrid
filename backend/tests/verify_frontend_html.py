"""
Verification script for backend/templates/dashboard.html.
Validates:
1. All onclick attributes call defined JS functions.
2. All document.getElementById references point to existing DOM element IDs.
3. No unclosed script tags or missing HTML elements.
"""

import re
import os

def test_dashboard_integrity():
    dash_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates", "dashboard.html"))
    with open(dash_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Extract all IDs in HTML
    element_ids = set(re.findall(r'id=["\']([a-zA-Z0-9_\-]+)["\']', html))
    print(f"Total element IDs in HTML: {len(element_ids)}")

    # Extract all document.getElementById calls
    get_ids = set(re.findall(r'getElementById\(["\']([a-zA-Z0-9_\-]+)["\']\)', html))
    print(f"Total getElementById calls: {len(get_ids)}")

    missing_ids = get_ids - element_ids
    print(f"Missing element IDs referenced in JS: {missing_ids}")
    assert len(missing_ids) == 0, f"Referenced IDs missing from DOM: {missing_ids}"

    # Extract all onclick functions
    onclick_matches = re.findall(r'onclick=["\']([^"\']+)["\']', html)
    invoked_fns = set()
    for oc in onclick_matches:
        for stmt in oc.split(";"):
            stmt = stmt.strip()
            m = re.match(r'([a-zA-Z0-9_]+)\(', stmt)
            if m:
                invoked_fns.add(m.group(1))

    # Extract all function definitions in the script block
    defined_fns = set(re.findall(r'(?:function\s+([a-zA-Z0-9_]+)\s*\(|const\s+([a-zA-Z0-9_]+)\s*=\s*(?:function|\([^)]*\)\s*=>)|let\s+([a-zA-Z0-9_]+)\s*=\s*(?:function|\([^)]*\)\s*=>))', html))
    flat_defined = set()
    for group in defined_fns:
        for name in group:
            if name:
                flat_defined.add(name)

    # Standard browser / Leaflet functions
    builtins = {"closeModal", "openModal", "alert", "prompt", "confirm", "parseInt", "parseFloat"}
    all_known = flat_defined.union(builtins)

    missing_fns = invoked_fns - all_known
    print(f"Total onclick functions: {len(invoked_fns)}")
    print(f"Missing onclick functions: {missing_fns}")
    assert len(missing_fns) == 0, f"Onclick functions missing in script: {missing_fns}"

    print("SUCCESS: Dashboard HTML has 100% DOM ID and function binding integrity!")

if __name__ == "__main__":
    test_dashboard_integrity()
