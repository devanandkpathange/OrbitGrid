import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

pdf_path = os.path.abspath("d:/winning project/DEMO_VIDEO_SCRIPT.pdf")

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=36,
    leftMargin=36,
    topMargin=32,
    bottomMargin=32
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=20,
    leading=24,
    textColor=colors.HexColor('#0F172A'),
    alignment=1,
    spaceAfter=3
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10.5,
    leading=14,
    textColor=colors.HexColor('#2563EB'),
    alignment=1,
    spaceAfter=10
)

section_title = ParagraphStyle(
    'SecTitle',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=11.5,
    leading=15,
    textColor=colors.HexColor('#0F172A'),
    spaceBefore=0,
    spaceAfter=3
)

action_style = ParagraphStyle(
    'ActionStyle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9.5,
    leading=13,
    textColor=colors.HexColor('#0369A1')
)

say_style = ParagraphStyle(
    'SayStyle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#0F172A')
)

time_badge_style = ParagraphStyle(
    'TimeBadge',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9.5,
    leading=13,
    textColor=colors.HexColor('#FFFFFF'),
    alignment=1
)

elements = []

elements.append(Paragraph("ORBIT GRID — DEMO VIDEO SCRIPT", title_style))
elements.append(Paragraph("2.5-Minute Video Cheat Sheet • Easy Spoken Words &amp; Exact Screen Actions", subtitle_style))
elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#CBD5E1'), spaceAfter=10))

steps = [
    {
        "time": "0:00 - 0:20\n(20s)",
        "title": "1. The Problem &amp; What Orbit Grid Does",
        "action": "<b>Screen:</b> Show browser on <code>http://127.0.0.1:8000/</code> (Login Page).",
        "say": "“In India, companies waste billions of rupees on transport because they guess where to place warehouses.<br/><br/>This is <b>Orbit Grid</b>—a fast, intelligent system that calculates the exact best warehouse locations automatically at zero cost.”"
    },
    {
        "time": "0:20 - 0:40\n(20s)",
        "title": "2. Easy Evaluator Login &amp; Map View",
        "action": "<b>Click:</b> <b>'1-Click Hackathon Evaluator Access'</b> &rarr; Scroll down to the Command Center.",
        "say": "“Judges can log in instantly with our 1-click access button.<br/><br/>This brings us to the live Command Center—a clean, fast interactive map built specifically for Indian logistics.”"
    },
    {
        "time": "0:40 - 1:15\n(35s)",
        "title": "3. Clean Slate &amp; Business Setup",
        "action": "<b>Click:</b> <b>'Business &amp; Network Setup'</b> button.<br/><b>Type:</b> <i>'Textiles'</i> &bull; Existing Hub: <i>'Pune'</i> &bull; Warehouses: <i>2</i> &rarr; Click <b>'Apply Setup'</b>.",
        "say": "“The map starts completely clean without fake data. In the Business Setup window, we enter our business type and our current warehouse in Pune.<br/><br/>The system marks our Pune hub in amber and prepares to optimize new warehouses around it.”"
    },
    {
        "time": "1:15 - 1:50\n(35s)",
        "title": "4. 1-Click Solver &amp; Instant Savings",
        "action": "<b>Select:</b> Region: <b>Maharashtra</b> &rarr; Click <b>'Run Optimization Solver'</b>.<br/><b>Show:</b> Warehouses WH-1 &amp; WH-2 appear &bull; Point to 77% Distance Reduction on top.",
        "say": "“Next, we select Maharashtra and click 'Run Optimization'. In just 3 milliseconds, it calculates optimal locations and connects them directly to real industrial zones like Chakan MIDC.<br/><br/>Delivery distance drops by 77%, cutting transport costs by 64%!”"
    },
    {
        "time": "1:50 - 2:20\n(30s)",
        "title": "5. Viability Report, Green ESG &amp; AI Copilot",
        "action": "<b>Click:</b> <b>'Viability Dossier'</b> (show modal, close) &bull; Point to Green ESG cards &bull; Click <b>'AI Copilot'</b>.",
        "say": "“Clicking 'Viability Dossier' gives us a full financial cost and rent breakdown.<br/><br/>It also tracks green impact, showing saved diesel and CO2 reduction. Our built-in AI Copilot clearly explains the business strategy behind each hub.”"
    },
    {
        "time": "2:20 - 2:45\n(25s)",
        "title": "6. Auto-Save &amp; Conclusion",
        "action": "<b>Click:</b> <b>'Save Analysis'</b> &rarr; Point to <b>'Presentation Deck'</b> in top navigation.",
        "say": "“All results save directly to our database so nothing is lost. We also built an interactive 10-slide presentation deck right into the app.<br/><br/>Orbit Grid turns weeks of manual consulting into an instant decision. Thank you!”"
    }
]

table_data = []

for step in steps:
    time_cell = Paragraph(f"<b>{step['time']}</b>", time_badge_style)
    
    content = [
        Paragraph(f"<b>{step['title']}</b>", section_title),
        Spacer(1, 1),
        Paragraph(step['action'], action_style),
        Spacer(1, 4),
        Paragraph(f"<b>🗣 WHAT TO SAY:</b> {step['say']}", say_style),
        Spacer(1, 3)
    ]
    
    table_data.append([time_cell, content])

t = Table(table_data, colWidths=[65, 475])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#0F172A')),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (1, 0), (1, -1), 10),
    ('RIGHTPADDING', (1, 0), (1, -1), 6),
    ('LINEBELOW', (0, 0), (-1, -2), 1, colors.HexColor('#E2E8F0')),
    ('ROUNDEDCORNERS', [4, 4, 4, 4])
]))

elements.append(t)
elements.append(Spacer(1, 8))
elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5))

footer_text = Paragraph(
    "<b>Pro Tip for Recording:</b> Keep browser in Full Screen (F11) • Speak calmly and pause 1 second before each click.",
    ParagraphStyle('FooterTip', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor('#64748B'), alignment=1)
)
elements.append(footer_text)

doc.build(elements)
print(f"SUCCESS: Generated PDF at {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
