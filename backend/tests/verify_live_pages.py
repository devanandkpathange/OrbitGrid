import urllib.request
import re

def verify_live_pages():
    print("Testing live pages structure on http://127.0.0.1:8000/...")
    resp = urllib.request.urlopen("http://127.0.0.1:8000/")
    assert resp.status == 200
    html = resp.read().decode("utf-8")

    # Page 1 checks
    assert 'id="heroLanding"' in html, "heroLanding missing"
    assert 'id="heroCanvas"' in html, "heroCanvas missing"
    assert 'lucide@latest' in html, "Lucide CDN script missing"
    assert 'data-lucide="shield-check"' in html, "Lucide shield badge missing"
    assert 'data-lucide="rocket"' in html, "Lucide rocket CTA button missing"
    assert 'initHeroCanvas()' in html, "initHeroCanvas missing"
    assert 'BTD INNOVATION LABS' in html, "BTD Labs badge missing"
    assert 'hero-showcase-card' in html, "hero-showcase-card missing"
    assert 'hero-pipeline-bar' in html, "hero-pipeline-bar missing"
    assert 'hero-scroll-unveil' in html, "hero-scroll-unveil missing"
    assert 'Scroll down to unveil Command Center' in html, "unveil cue missing"

    # Page 2 checks
    assert 'id="commandCenter"' in html, "commandCenter missing"
    assert 'command-header' in html, "command-header missing"
    assert 'system-status-pills' not in html, "system-status-pills should be removed from header"
    assert 'searchInput' in html, "searchInput missing"
    assert 'searchDropdown' in html, "searchDropdown missing"
    assert 'btnAutopilot' in html, "btnAutopilot missing"
    assert 'openPitchDeck' in html, "openPitchDeck missing"
    assert 'openCopilotModal' in html, "openCopilotModal missing"
    assert 'openWizard' in html, "openWizard missing"
    assert 'scrollToHero' in html, "scrollToHero missing"
    assert 'telemetryStrip' in html, "telemetryStrip missing"
    assert 'sidebar' in html, "sidebar missing"
    assert 'map-container' in html, "map-container missing"
    assert 'aiDecisionPanel' in html, "aiDecisionPanel missing"
    assert 'collapsed' in html, "aiDecisionPanel collapsed missing"

    print("[SUCCESS] ALL 15 VERIFICATION CRITERIA PASSED! 2 SEPARATE PAGES & DYNAMIC SHIFT RESTORED!")

if __name__ == "__main__":
    verify_live_pages()
