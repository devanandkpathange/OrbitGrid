with open('backend/templates/dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'id="commandCenter"' in line or 'class="command-header"' in line or '<!-- Right Action Items -->' in line or 'class="sidebar"' in line:
        print(f"{i+1}: {line.strip()[:100]}")
