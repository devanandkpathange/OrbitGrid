import re

with open('backend/templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS for clean sidebar cards, action grid, solver buttons, status chips
css_target = """    .sidebar {
      width: 310px;
      min-width: 310px;
      background: rgba(10, 15, 26, 0.98);
      border-right: 1px solid var(--card-border);
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      overflow-y: auto;
      z-index: 500;
      transition: all 0.3s ease;
    }"""

new_css = """    .sidebar {
      width: 320px;
      min-width: 320px;
      background: rgba(10, 15, 26, 0.98);
      border-right: 1px solid var(--card-border);
      padding: 14px 12px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      overflow-y: auto;
      z-index: 500;
      transition: all 0.3s ease;
    }

    /* Clean Enterprise Sidebar Cards */
    .sidebar-card {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 10px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      backdrop-filter: blur(8px);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }
    .sidebar-card-header {
      display: flex;
      align-items: center;
      gap: 7px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: #94A3B8;
      margin-bottom: 2px;
    }
    .sidebar-card-header i, .sidebar-card-header svg {
      width: 14px;
      height: 14px;
    }
    .demand-status-chip {
      margin-left: auto;
      font-size: 10px;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 999px;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.35);
      color: #38BDF8;
      letter-spacing: 0.3px;
      white-space: nowrap;
    }
    .demand-status-chip.loaded {
      background: rgba(16, 185, 129, 0.15);
      border-color: rgba(16, 185, 129, 0.4);
      color: #34D399;
    }
    .btn-preset-load {
      width: 100%;
      background: rgba(56, 189, 248, 0.1);
      border: 1px dashed rgba(56, 189, 248, 0.35);
      color: #38BDF8;
      font-size: 11px;
      font-weight: 600;
      padding: 7px 10px;
      border-radius: 6px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s ease;
    }
    .btn-preset-load:hover {
      background: rgba(56, 189, 248, 0.2);
      border-style: solid;
      transform: translateY(-1px);
    }
    .sidebar-action-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 7px;
    }
    .btn-action-tile {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.09);
      color: #E2E8F0;
      font-size: 11px;
      font-weight: 600;
      padding: 10px 8px;
      border-radius: 8px;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 5px;
      text-align: center;
      transition: all 0.2s ease;
    }
    .btn-action-tile i, .btn-action-tile svg {
      width: 16px;
      height: 16px;
      color: #94A3B8;
      transition: color 0.2s ease;
    }
    .btn-action-tile:hover {
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(255, 255, 255, 0.2);
      transform: translateY(-1px);
    }
    .btn-action-tile.highlight {
      background: rgba(37, 99, 235, 0.16);
      border-color: rgba(37, 99, 235, 0.45);
      color: #93C5FD;
    }
    .btn-action-tile.highlight i, .btn-action-tile.highlight svg {
      color: #60A5FA;
    }
    .btn-action-tile.highlight:hover {
      background: rgba(37, 99, 235, 0.28);
    }
    .btn-action-tile.danger {
      color: #FCA5A5;
      border-color: rgba(239, 68, 68, 0.25);
    }
    .btn-action-tile.danger i, .btn-action-tile.danger svg {
      color: #F87171;
    }
    .btn-action-tile.danger:hover {
      background: rgba(239, 68, 68, 0.15);
      border-color: rgba(239, 68, 68, 0.45);
    }
    .btn-solver-primary {
      width: 100%;
      background: linear-gradient(135deg, #2563EB, #059669);
      color: #ffffff;
      border: none;
      padding: 12px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.4px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 7px;
      box-shadow: 0 0 16px rgba(37, 99, 235, 0.4);
      transition: all 0.25s ease;
    }
    .btn-solver-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 0 24px rgba(37, 99, 235, 0.6);
    }
    .btn-solver-secondary {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #CBD5E1;
      font-size: 11px;
      font-weight: 600;
      padding: 8px 6px;
      border-radius: 6px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      transition: all 0.2s ease;
    }
    .btn-solver-secondary:hover {
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(255, 255, 255, 0.22);
      transform: translateY(-1px);
    }"""

assert css_target in content, "CSS target not found"
content = content.replace(css_target, new_css, 1)
print("Step 1: CSS updated successfully.")

# 2. Update Header, Sidebar, and Map HTML
# Find from <div class="header-actions"> down to </div> <!-- closes .app-body -->
header_actions_start = content.find('<!-- Right Action Items -->')
assert header_actions_start != -1, "header actions start not found"

app_body_end = content.find('</div> <!-- closes .app-body -->')
assert app_body_end != -1, "app body end not found"

replacement_markup = """<!-- Right Action Items -->
      <div class="header-actions">
        <!-- Pitch Deck Presentation -->
        <button class="btn-wizard-trigger" onclick="openPitchDeck()" style="background: linear-gradient(135deg, #10B981, #059669); font-size: 11px; padding: 6px 11px; box-shadow: 0 0 12px rgba(16, 185, 129, 0.4);" title="Open Judge Presentation Deck [Hot-Key: P]">
          <i data-lucide="presentation" style="width:12px; height:12px;"></i> Pitch Deck
        </button>

        <!-- Orbit Grid SETU AI Copilot -->
        <button class="btn-wizard-trigger" onclick="openCopilotModal()" style="background: linear-gradient(135deg, #2563EB, #8B5CF6); font-size: 11px; padding: 6px 12px; box-shadow: 0 0 14px rgba(139, 92, 246, 0.45);" title="Open Orbit Grid SETU Strategic AI Console">
          <i data-lucide="sparkles" style="width:12px; height:12px;"></i> AI Copilot
        </button>

        <!-- Logged-in Company User Profile -->
        <div class="user-auth-badge" id="userAuthBadge" style="display: flex; align-items: center; gap: 6px; font-size: 11px; padding: 5px 10px; background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 8px; color: #E2E8F0;">
          <i data-lucide="building-2" style="width: 12px; height: 12px; color: #38BDF8;"></i>
          <span id="userProfileCompany" style="max-width: 120px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">Company</span>
          <span style="opacity: 0.5;">·</span>
          <span id="userProfileOwner" style="color: #38BDF8; font-weight: 600; max-width: 80px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">User</span>
        </div>

        <!-- Save Analysis to DB Button -->
        <button class="btn-topbar-save" id="btnSaveAnalysis" onclick="saveActiveAnalysisToDatabase()" style="font-size: 11px; padding: 6px 11px; background: rgba(16, 185, 129, 0.18); border: 1px solid rgba(16, 185, 129, 0.45); border-radius: 8px; color: #34D399; cursor: pointer; display: flex; align-items: center; gap: 5px; font-weight: 600;" title="Save current warehouse analysis and demand nodes to database">
          <i data-lucide="save" style="width: 12px; height: 12px;"></i> Save Analysis
        </button>

        <!-- Logout Button -->
        <button class="btn-topbar-logout" id="btnLogout" onclick="performLogout()" style="font-size: 11px; padding: 6px 9px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; color: #94A3B8; cursor: pointer; display: flex; align-items: center; gap: 4px;" title="Sign out from session">
          <i data-lucide="log-out" style="width: 12px; height: 12px;"></i>
        </button>

        <!-- Preserved hidden items for API / JS integrity -->
        <button id="btnAutopilot" style="display:none;" onclick="runAutoPilotTour()"></button>
        <button id="btnBriefingToggle" style="display:none;"></button>
      </div>
    </header>

  <!-- App Body -->
  <div class="app-body">
    
    <!-- Clean, Streamlined Controls Sidebar -->
    <aside class="sidebar">

      <!-- CARD 1: TERRITORY & CORRIDORS -->
      <div class="sidebar-card">
        <div class="sidebar-card-header">
          <i data-lucide="map-pin" style="color: #38BDF8;"></i>
          <span>Territory &amp; Corridors</span>
        </div>

        <div class="input-group">
          <label for="regionSelect">Logistics Region</label>
          <select id="regionSelect" onchange="handleRegionChange(this.value)">
            <option value="pan_india" selected>Pan-India Logistics Corridors (All Metros)</option>
            <option value="karnataka">Karnataka (Bengaluru, Mysuru, Belagavi...)</option>
            <option value="maharashtra">Maharashtra (Mumbai, Pune, Nagpur, Chakan...)</option>
            <option value="tamil_nadu">Tamil Nadu (Chennai, Coimbatore, Hosur...)</option>
            <option value="gujarat">Gujarat (Ahmedabad, Surat, Vadodara...)</option>
            <option value="delhi_ncr">Delhi NCR &amp; Haryana (Gurugram, Faridabad...)</option>
            <option value="uttar_pradesh">Uttar Pradesh (Noida, Lucknow, Kanpur...)</option>
            <option value="telangana">Telangana (Hyderabad, Medchal...)</option>
            <option value="andhra_pradesh">Andhra Pradesh (Visakhapatnam, Sri City...)</option>
            <option value="rajasthan">Rajasthan (Jaipur, Bhiwadi, Kota...)</option>
            <option value="punjab">Punjab (Ludhiana, Amritsar...)</option>
            <option value="west_bengal">West Bengal (Kolkata, Durgapur...)</option>
            <option value="madhya_pradesh">Madhya Pradesh (Indore, Pithampur...)</option>
            <option value="kerala">Kerala (Kochi, Kozhikode...)</option>
            <option value="bihar_jharkhand">Bihar &amp; Jharkhand (Patna, Jamshedpur...)</option>
            <option value="odisha">Odisha (Bhubaneswar, Rourkela...)</option>
            <option value="assam_northeast">Assam &amp; Northeast (Guwahati...)</option>
          </select>
        </div>

        <button type="button" class="btn-preset-load" onclick="loadSelectedRegionBenchmark()" title="Load pre-packaged benchmark demand points for this state">
          <i data-lucide="download-cloud" style="width:12px; height:12px;"></i> Load State Benchmark Points
        </button>

        <div class="input-group">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
            <label style="margin-bottom:0;">Warehouses to Optimize ($k$)</label>
            <span class="range-val" id="rangeDisplay">2</span>
          </div>
          <input type="range" id="warehouseCount" min="1" max="5" value="2" oninput="updateRangeVal(this.value)">
        </div>

        <div class="checkbox-wrap" style="margin-top: 2px;">
          <input type="checkbox" id="snapToHubs" checked>
          <label class="checkbox-label" for="snapToHubs">
            <strong style="font-size: 11px;">Snap to Industrial Parks</strong>
            <span style="font-size: 10px; color: var(--text-muted); display: block;">Verified KIADB / MIDC SEZ infrastructure</span>
          </label>
        </div>
      </div>

      <!-- CARD 2: DEMAND NETWORK -->
      <div class="sidebar-card">
        <div class="sidebar-card-header">
          <i data-lucide="layers" style="color: #10B981;"></i>
          <span>Demand Network</span>
          <span class="demand-status-chip" id="demandStatusChip">0 Points</span>
        </div>

        <div class="sidebar-action-grid">
          <button class="btn-action-tile highlight" onclick="openManualDemandEditor()" title="Configure customer cities and dispatch volumes">
            <i data-lucide="table-properties"></i>
            <span>Business Analyser</span>
          </button>
          <button class="btn-action-tile" onclick="openModal('docUploadModal')" title="Upload CSV or spreadsheet of customer coordinates">
            <i data-lucide="upload"></i>
            <span>Upload CSV</span>
          </button>
          <button class="btn-action-tile" id="addPointBtn" onclick="toggleAddPointMode()" title="Click on map to drop demand locations">
            <i data-lucide="map-pin-plus"></i>
            <span>Add on Map</span>
          </button>
          <button class="btn-action-tile danger" onclick="clearAllDemandNodes()" title="Clear all nodes and reset map">
            <i data-lucide="trash-2"></i>
            <span>Clear Map</span>
          </button>
        </div>
      </div>

      <!-- CARD 3: SOLVER & REPORTS -->
      <div class="sidebar-card" style="margin-top: auto;">
        <button class="btn-solver-primary" id="btnRunOptimizer" onclick="runOptimization()">
          <i data-lucide="zap" style="width:16px; height:16px;"></i>
          <span>Run Optimization Solver</span>
        </button>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
          <button class="btn-solver-secondary" onclick="generateFeasibilityForSelected()" title="View Location Feasibility &amp; CapEx/OpEx Breakdown">
            <i data-lucide="file-check-2" style="width:13px; height:13px;"></i>
            <span>Viability Dossier</span>
          </button>
          <button class="btn-solver-secondary" onclick="openCopilotModal()" title="Ask SETU Strategic AI Copilot">
            <i data-lucide="sparkles" style="width:13px; height:13px; color: #C084FC;"></i>
            <span>SETU AI Copilot</span>
          </button>
        </div>
      </div>

      <!-- Preserved hidden elements for backward compatibility with existing JS -->
      <div style="display:none;">
        <div id="industryBanner"><strong id="bannerTitle"></strong><span id="bannerDesc"></span></div>
        <input type="text" id="sidebarBusinessInput">
        <input type="number" id="capacityLimit" value="35000">
        <input type="number" id="radiusLimit" value="250">
        <button id="drawPolyBtn" onclick="toggleDrawPolygon()"></button>
        <div id="demandSummary"></div>
        <span id="hudDemandCount"></span>
        <span id="hudLatency"></span>
        <button id="themeSelector"></button>
        <button id="audioToggleBtn"></button>
        <button id="aiPanelToggleBtn"></button>
        <div id="mapCoordHud"></div>
        <div id="telemetryStrip"></div>
      </div>

    </aside>

    <!-- Map Container -->
    <main class="map-container">

      <!-- Map Floating Minimal Basemap Switcher -->
      <div class="map-tools-bar">
        <button class="tool-chip active" id="tileDark" onclick="setTileLayer('dark')" title="Dark Canvas Basemap">Dark Canvas</button>
        <button class="tool-chip" id="tileSat" onclick="setTileLayer('satellite')" title="Satellite Imagery Basemap">Satellite</button>
        <button class="tool-chip" id="tileStreet" onclick="setTileLayer('osm')" title="OpenStreetMap Street">Street</button>
        <div style="width: 1px; height: 16px; background: rgba(255,255,255,0.18); margin: 0 4px;"></div>
        <button class="tool-chip" id="layoutToggleBtn" onclick="toggleLayoutMode()" title="Toggle Fullscreen Map View">
          <i data-lucide="maximize-2" style="width:12px; height:12px; margin-right:4px;"></i> Fullscreen
        </button>
      </div>

      <div id="map"></div>

      <!-- Floating Analytics Bar -->
      <div class="metrics-bar">
        <div class="metric-card">
          <div class="metric-label">Estimated Delivery Cost</div>
          <div class="metric-value" id="metricCost">₹ —</div>
          <div class="metric-sub" id="metricCostSub">Awaiting calculation</div>
        </div>

        <div class="metric-card">
          <div class="metric-label">Average Distance</div>
          <div class="metric-value" id="metricAvgDist">— km</div>
          <div class="metric-sub" id="metricTotalDist">Awaiting calculation</div>
        </div>

        <div class="metric-card">
          <div class="metric-label">Warehouses Placed</div>
          <div class="metric-value" id="metricWhCount">0</div>
          <div class="metric-sub" id="metricSla">Awaiting run</div>
        </div>

        <div class="metric-card">
          <div class="metric-label">Green ESG Reduction</div>
          <div class="metric-value" id="metricCo2">0 kg</div>
          <div class="metric-sub" id="metricDiesel">Diesel: 0 L</div>
        </div>
      </div>
    </main>

    <!-- Hidden AI Decision Panel for DOM script compatibility -->
    <aside class="ai-decision-panel" id="aiDecisionPanel" style="display:none;">
      <div id="aiPanelStatusBadge"></div>
      <div id="aiRecCard"></div>
      <div id="aiRecHubName"></div>
      <div id="aiRecSub"></div>
      <div id="aiRecWhyList"></div>
      <div id="aiConfidenceVal"></div>
      <div id="aiConfidenceBar"></div>
      <input type="text" id="aiPanelQuestionInput">
      <button id="btnAIPanelSend"></button>
      <div id="aiPanelResponse"></div>
    </aside>
"""

content = content[:header_actions_start] + replacement_markup + content[app_body_end:]
print("Step 2: Markup replaced successfully.")

# 3. Update Audio: mute sound by default
content = content.replace("let enabled = true;", "let enabled = false;", 1)
print("Step 3: GP_Audio muted by default.")

# 4. Update initMap() center and clean up mousemove hud
init_map_idx = content.find("function initMap() {")
assert init_map_idx != -1, "initMap not found"

# 5. Add handleRegionChange and loadSelectedRegionBenchmark, update loadRegionDefaults
load_reg_idx = content.find("async function loadRegionDefaults(region) {")
assert load_reg_idx != -1, "loadRegionDefaults not found"

new_region_logic = """    function updateDemandStatusDisplay() {
      const chip = document.getElementById('demandStatusChip');
      if (!chip) return;
      if (!currentDemandData || currentDemandData.length === 0) {
        chip.innerText = '0 Points';
        chip.classList.remove('loaded');
      } else {
        const totalUnits = currentDemandData.reduce((s, p) => s + (p.demand || 0), 0);
        chip.innerText = `${currentDemandData.length} Nodes (${totalUnits.toLocaleString('en-IN')} units)`;
        chip.classList.add('loaded');
      }
    }

    function handleRegionChange(region) {
      const regionViews = {
        pan_india: { center: [20.5937, 78.9629], zoom: 4.6 },
        karnataka: { center: [14.4, 76.0], zoom: 5.7 },
        maharashtra: { center: [19.2, 75.8], zoom: 5.6 },
        tamil_nadu: { center: [11.1, 78.6], zoom: 5.8 },
        gujarat: { center: [22.4, 71.8], zoom: 5.8 },
        uttar_pradesh: { center: [27.0, 80.8], zoom: 5.6 },
        delhi_ncr: { center: [28.6, 77.1], zoom: 7.2 },
        rajasthan: { center: [26.8, 74.2], zoom: 5.4 },
        telangana: { center: [17.8, 79.1], zoom: 5.9 },
        andhra_pradesh: { center: [15.8, 80.0], zoom: 5.7 },
        kerala: { center: [10.3, 76.3], zoom: 5.9 },
        west_bengal: { center: [23.5, 87.8], zoom: 5.8 },
        madhya_pradesh: { center: [23.2, 77.4], zoom: 5.4 },
        punjab: { center: [31.1, 75.3], zoom: 6.4 },
        bihar_jharkhand: { center: [24.5, 85.5], zoom: 5.7 },
        odisha: { center: [20.5, 84.5], zoom: 5.7 },
        assam_northeast: { center: [26.2, 92.5], zoom: 5.5 }
      };
      if (map && regionViews[region]) {
        map.setView(regionViews[region].center, regionViews[region].zoom);
      }
    }

    async function loadSelectedRegionBenchmark() {
      const reg = document.getElementById('regionSelect')?.value || 'pan_india';
      await loadRegionDefaults(reg, true);
    }

    async function loadRegionDefaults(region, executeOptimization = true) {"""

content = content.replace("async function loadRegionDefaults(region) {", new_region_logic, 1)
print("Step 4: Region functions added.")

# 6. Update renderDemandPoints to call updateDemandStatusDisplay()
render_dem_idx = content.find("function renderDemandPoints() {")
assert render_dem_idx != -1, "renderDemandPoints not found"
content = content.replace("function renderDemandPoints() {", "function renderDemandPoints() {\n      updateDemandStatusDisplay();", 1)

# 7. Update clearAllDemandNodes to reset demandStatusChip and layers
clear_nodes_str = """      if (mapLayers.demandPoints) mapLayers.demandPoints.clearLayers();
      if (mapLayers.warehouses) mapLayers.warehouses.clearLayers();
      if (mapLayers.routes) mapLayers.routes.clearLayers();"""

new_clear_nodes = """      if (mapLayers.demands) mapLayers.demands.clearLayers();
      if (mapLayers.demandPoints) mapLayers.demandPoints.clearLayers();
      if (mapLayers.warehouses) mapLayers.warehouses.clearLayers();
      if (mapLayers.routes) mapLayers.routes.clearLayers();
      if (mapLayers.catchment) mapLayers.catchment.clearLayers();
      updateDemandStatusDisplay();"""

assert clear_nodes_str in content, "clear_nodes_str not found"
content = content.replace(clear_nodes_str, new_clear_nodes, 1)

# 8. Remove the auto-loading of pan_india from window.onload!
window_onload_target = """      try {
        await loadRegionDefaults('pan_india');
      } catch (err) {
        console.error('Initial auto-load error:', err);
      }
      await initAuth();"""

new_window_onload = """      // Start with clean map state (awaiting user's company demand input)
      clearAllDemandNodes();
      await initAuth();"""

assert window_onload_target in content, "window_onload_target not found"
content = content.replace(window_onload_target, new_window_onload, 1)
print("Step 5: window.onload updated to keep clean slate.")

# Save modified content
with open('backend/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: dashboard.html updated cleanly.")
