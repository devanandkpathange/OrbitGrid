with open('backend/templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add "Business & Network Setup" button to header actions
header_target = """        <!-- Pitch Deck Presentation -->
        <button class="btn-wizard-trigger" onclick="openPitchDeck()\""""

header_new = """        <!-- Business & Network Setup Wizard Button -->
        <button class="btn-wizard-trigger" id="btnOpenWizard" onclick="openWizard()" style="background: linear-gradient(135deg, #0284C7, #2563EB); font-size: 11px; padding: 6px 13px; box-shadow: 0 0 14px rgba(37,99,235,0.45); color: #fff; font-weight: 700; border: 1px solid rgba(56,189,248,0.4); border-radius: 8px; cursor: pointer; display: flex; align-items: center; gap: 6px;" title="Business &amp; Network Profiler: Configure your business type, existing warehouses, and expansion goals">
          <i data-lucide="briefcase" style="width:13px; height:13px;"></i> Business &amp; Network Setup
        </button>

        <!-- Pitch Deck Presentation -->
        <button class="btn-wizard-trigger" onclick="openPitchDeck()\""""

assert header_target in content, "header_target not found"
content = content.replace(header_target, header_new, 1)
print("Step 1: Header button restored.")

# 2. Add Business & Network Setup Wizard button inside sidebar Card 1
sidebar_target = """      <!-- CARD 1: TERRITORY & CORRIDORS -->
      <div class="sidebar-card">
        <div class="sidebar-card-header">
          <i data-lucide="map-pin" style="color: #38BDF8;"></i>
          <span>Territory &amp; Corridors</span>
        </div>"""

sidebar_new = """      <!-- CARD 1: TERRITORY & CORRIDORS -->
      <div class="sidebar-card">
        <div class="sidebar-card-header">
          <i data-lucide="map-pin" style="color: #38BDF8;"></i>
          <span>Territory &amp; Corridors</span>
        </div>

        <!-- Business & Network Setup Wizard Trigger -->
        <button type="button" class="btn-wizard-sidebar" onclick="openWizard()" style="width:100%; background: linear-gradient(135deg, rgba(37,99,235,0.22), rgba(14,165,233,0.18)); border: 1px solid rgba(56,189,248,0.45); color: #38BDF8; font-size: 11px; font-weight: 700; padding: 8px 10px; border-radius: 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 7px; margin-bottom: 2px; box-shadow: 0 0 12px rgba(56,189,248,0.2); transition: all 0.2s ease;" title="Configure your business type, existing warehouses, and expansion goals">
          <i data-lucide="briefcase" style="width:13px; height:13px; color:#38BDF8;"></i> Business &amp; Network Setup
        </button>

        <div id="activeBusinessTag" style="display:none; font-size: 11px; background: rgba(56,189,248,0.08); border: 1px solid rgba(56,189,248,0.25); padding: 5px 8px; border-radius: 6px; color: #93C5FD; margin-bottom: 4px;">
          <span style="color:#38BDF8; font-weight:700;">Profile:</span> <span id="activeBusinessText">General Supply Chain</span>
        </div>"""

assert sidebar_target in content, "sidebar_target not found"
content = content.replace(sidebar_target, sidebar_new, 1)
print("Step 2: Sidebar Card 1 wizard button added.")

# 3. Update applyWizardSetup to be async and update activeBusinessTag
apply_target = """function applyWizardSetup() {
      const bizText = document.getElementById('wizBusinessInput').value.trim() || "General Retail & Supply Chain";"""

apply_new = """async function applyWizardSetup() {
      const bizText = document.getElementById('wizBusinessInput').value.trim() || "General Retail & Supply Chain";
      const bizTag = document.getElementById('activeBusinessTag');
      const bizSpan = document.getElementById('activeBusinessText');
      if (bizTag && bizSpan) {
        bizSpan.innerText = bizText;
        bizTag.style.display = 'block';
      }"""

assert apply_target in content, "apply_target not found"
content = content.replace(apply_target, apply_new, 1)
print("Step 3: applyWizardSetup updated with activeBusinessTag display.")

# 4. Update restoreUserScenario to also show activeBusinessTag
restore_target = """        if (scenario.business_description) {
          userBusinessDescription = scenario.business_description;
          const bizInp = document.getElementById('sidebarBusinessInput');
          if (bizInp) bizInp.value = scenario.business_description;
        }"""

restore_new = """        if (scenario.business_description) {
          userBusinessDescription = scenario.business_description;
          const bizInp = document.getElementById('sidebarBusinessInput');
          if (bizInp) bizInp.value = scenario.business_description;
          const bizTag = document.getElementById('activeBusinessTag');
          const bizSpan = document.getElementById('activeBusinessText');
          if (bizTag && bizSpan) {
            bizSpan.innerText = scenario.business_description;
            bizTag.style.display = 'block';
          }
        }"""

assert restore_target in content, "restore_target not found"
content = content.replace(restore_target, restore_new, 1)
print("Step 4: restoreUserScenario updated.")

with open('backend/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Wizard triggers and business profile badges restored!")
