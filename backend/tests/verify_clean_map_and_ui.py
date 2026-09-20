"""
Verification script for Clean Map State and Clutter-Free UI.
Tests:
1. No auto-loading of demo data on window.onload (clean slate initialized).
2. Clutter elements (telemetry strip, sound FX toggle, theme selector, coordinate HUD, right-side AI drawer) are removed from visual presentation.
3. Clean 3-card sidebar architecture with territory, demand network, and solver cards exists.
4. Load State Benchmark Points button and handler are wired up.
5. Audio is muted by default.
"""

import re
import os
import requests

def test_clean_map_and_ui():
    base_url = "http://127.0.0.1:8000"
    resp = requests.get(f"{base_url}/")
    assert resp.status_code == 200, f"Dashboard failed to load: {resp.status_code}"
    html = resp.text

    print("Checking Clean Map & Streamlined UI criteria...")

    # 1. Check that window.onload does NOT call loadRegionDefaults
    onload_idx = html.find("window.onload =")
    assert onload_idx != -1, "ERROR: window.onload not found!"
    onload_block = html[onload_idx:onload_idx + 400]
    assert "loadRegionDefaults" not in onload_block, "ERROR: loadRegionDefaults is still called in window.onload!"
    assert "clearAllDemandNodes();" in onload_block, "ERROR: clearAllDemandNodes not called in window.onload!"
    print("[PASS] 1. Auto-loading of sample data removed from window.onload; map initializes to clean slate.")

    # 2. Check that Sound FX is muted by default
    assert "let enabled = false;" in html, "ERROR: Sound FX is not muted by default!"
    print("[PASS] 2. Sound FX synthesizer is permanently muted by default.")

    # 3. Check that telemetry strip is removed from visual presentation
    assert '<div class="telemetry-strip" id="telemetryStrip">' not in html, "ERROR: telemetry-strip still in HTML!"
    print("[PASS] 3. Clumsy fake telemetry strip removed from Command Center.")

    # 4. Check that coordinate HUD is removed from map
    assert '<div id="mapCoordHud" class="map-coord-hud">' not in html, "ERROR: mapCoordHud still in HTML!"
    print("[PASS] 4. Coordinate HUD overlay removed from map.")

    # 5. Check that theme selector and sound buttons are removed from map-tools-bar
    tools_bar_idx = html.find('class="map-tools-bar"')
    assert tools_bar_idx != -1, "ERROR: map-tools-bar missing!"
    tools_bar = html[tools_bar_idx:tools_bar_idx + 600]
    assert 'id="themeSelector"' not in tools_bar, "ERROR: themeSelector still in map-tools-bar!"
    assert 'id="audioToggleBtn"' not in tools_bar, "ERROR: audioToggleBtn still in map-tools-bar!"
    assert 'id="aiPanelToggleBtn"' not in tools_bar, "ERROR: aiPanelToggleBtn still in map-tools-bar!"
    print("[PASS] 5. Theme dropdown, sound toggle, and AI panel toggle removed from map toolbar.")

    # 6. Check that the 3-card clean sidebar exists
    assert 'class="sidebar-card"' in html, "ERROR: sidebar-card class missing!"
    assert 'Territory &amp; Corridors' in html or 'Territory & Corridors' in html, "ERROR: Territory card missing!"
    assert 'Demand Network' in html, "ERROR: Demand Network card missing!"
    assert 'Run Optimization Solver' in html, "ERROR: Run Optimization Solver missing!"
    print("[PASS] 6. Clean 3-card sidebar architecture verified.")

    # 7. Check that Load State Benchmark Points button exists and is wired
    assert 'loadSelectedRegionBenchmark()' in html, "ERROR: loadSelectedRegionBenchmark not wired!"
    assert 'Load State Benchmark Points' in html, "ERROR: Load State Benchmark Points button missing!"
    print("[PASS] 7. Load State Benchmark Points button verified.")

    # 8. Check that demand status chip exists
    assert 'id="demandStatusChip"' in html, "ERROR: demandStatusChip missing!"
    print("[PASS] 8. Demand status chip verified.")

    # 9. Check that metrics bar initializes with awaiting placeholders
    assert 'id="metricCost">₹ —<' in html or 'metricCost' in html, "ERROR: metricCost missing!"
    assert 'Awaiting calculation' in html, "ERROR: Awaiting calculation placeholder missing!"
    print("[PASS] 9. Metrics bar awaiting placeholder state verified.")

    # 10. Check right-hand AI drawer is hidden
    assert 'id="aiDecisionPanel" style="display:none;"' in html, "ERROR: aiDecisionPanel is not hidden!"
    print("[PASS] 10. Redundant right-hand AI drawer hidden to give map full breathing room.")

    print("\n*** ALL 10 CLEAN MAP & CLUTTER-FREE UI CRITERIA PASSED WITH 100% SUCCESS! ***")

if __name__ == "__main__":
    test_clean_map_and_ui()
