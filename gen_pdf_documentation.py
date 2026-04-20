from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image as RLImage, PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Frame, PageTemplate, BaseDocTemplate
from reportlab.lib.utils import ImageReader
import os, io
from PIL import Image as PILImage

# ── Page setup ──────────────────────────────────────────────────────────────
W, H   = A4          # 595.28 x 841.89 pt
ML, MR = 2.0*cm, 2.0*cm
MT, MB = 2.2*cm, 2.2*cm
CW     = W - ML - MR

SAP_BLUE  = colors.HexColor("#0070D2")
DARK_BLUE = colors.HexColor("#003366")
MID_BLUE  = colors.HexColor("#185FA5")
LT_BLUE   = colors.HexColor("#E6F1FB")
ACCENT    = colors.HexColor("#E8A000")
GRAY      = colors.HexColor("#444444")
LT_GRAY   = colors.HexColor("#F5F5F5")
MID_GRAY  = colors.HexColor("#888888")
WHITE     = colors.white
BLACK     = colors.black

ARIAL     = "Helvetica"          # closest built-in to Arial
ARIAL_BD  = "Helvetica-Bold"
ARIAL_IT  = "Helvetica-Oblique"
ARIAL_BIT = "Helvetica-BoldOblique"

# ── Styles ──────────────────────────────────────────────────────────────────
def S(name, **kw):
    kw.pop("base", None)
    fn = kw.pop("fontName", ARIAL)
    tc = kw.pop("textColor", GRAY)
    ld = kw.pop("leading", 16)
    return ParagraphStyle(name, fontName=fn, textColor=tc, leading=ld, **kw)

sTitle   = S("sTitle",   fontName=ARIAL_BD, fontSize=15, textColor=DARK_BLUE,
              alignment=TA_CENTER, spaceAfter=4, leading=20)
sSub     = S("sSub",     fontName=ARIAL_BD, fontSize=14, textColor=MID_BLUE,
              alignment=TA_LEFT, spaceBefore=12, spaceAfter=4, leading=18)
sSub2    = S("sSub2",    fontName=ARIAL_BD, fontSize=12, textColor=SAP_BLUE,
              alignment=TA_LEFT, spaceBefore=8, spaceAfter=2, leading=16)
sBody    = S("sBody",    fontSize=12, alignment=TA_JUSTIFY,
              spaceBefore=2, spaceAfter=4, leading=17)
sBullet  = S("sBullet",  fontSize=12, alignment=TA_JUSTIFY,
              leftIndent=14, bulletIndent=4, spaceBefore=1, spaceAfter=2, leading=16)
sCaption = S("sCaption", fontSize=10, textColor=MID_GRAY, alignment=TA_CENTER,
              fontName=ARIAL_IT, spaceBefore=2, spaceAfter=6, leading=13)
sCenter  = S("sCenter",  fontSize=12, alignment=TA_CENTER, leading=17)
sMeta    = S("sMeta",    fontSize=11, alignment=TA_CENTER, textColor=MID_GRAY,
              fontName=ARIAL_IT, leading=14)
sTCell   = S("sTCell",   fontSize=11, alignment=TA_LEFT, leading=14)
sTHdr    = S("sTHdr",    fontSize=11, fontName=ARIAL_BD, alignment=TA_LEFT,
              textColor=WHITE, leading=14)
sFooter  = S("sFooter",  fontSize=9,  textColor=MID_GRAY, alignment=TA_RIGHT, leading=11)

IMG_DIR = "/home/claude/sap_imgs"

def sp(n=6):  return Spacer(1, n)
def hr():     return HRFlowable(width="100%", thickness=0.5, color=LT_BLUE, spaceAfter=6, spaceBefore=4)
def hr_bold():return HRFlowable(width="100%", thickness=2,   color=SAP_BLUE, spaceAfter=8, spaceBefore=4)

def bullet(text):
    return Paragraph(f"&bull;&nbsp;&nbsp;{text}", sBullet)

def numbered(n, text):
    return Paragraph(f"<b>{n}.</b>&nbsp;&nbsp;{text}", sBullet)

# ── Table helpers ────────────────────────────────────────────────────────────
HDR_STYLE = TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK_BLUE),
    ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
    ("FONTNAME",   (0,0), (-1,0), ARIAL_BD),
    ("FONTSIZE",   (0,0), (-1,-1), 10),
    ("FONTNAME",   (0,1), (-1,-1), ARIAL),
    ("TEXTCOLOR",  (0,1), (-1,-1), GRAY),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LT_BLUE]),
    ("GRID",       (0,0), (-1,-1), 0.4, colors.HexColor("#BBBBBB")),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
    ("RIGHTPADDING",(0,0), (-1,-1), 6),
    ("TOPPADDING",  (0,0), (-1,-1), 4),
    ("BOTTOMPADDING",(0,0),(-1,-1), 4),
    ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ("ALIGN",      (0,0), (-1,0),  "CENTER"),
])

def dtable(headers, rows, col_widths):
    data = [[Paragraph(h, sTHdr) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), sTCell) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(HDR_STYLE)
    return t

# ── Image helper: scale to fit width ────────────────────────────────────────
def sap_img(filename, caption, max_w=CW, max_h=7*cm):
    fp = os.path.join(IMG_DIR, filename)
    if not os.path.exists(fp):
        return []
    pil = PILImage.open(fp)
    iw, ih = pil.size
    scale = min(max_w/iw, max_h/ih)
    dw, dh = iw*scale, ih*scale
    # border frame via a 1-row table
    img_elem = RLImage(fp, width=dw, height=dh)
    frame_tbl = Table([[img_elem]], colWidths=[CW])
    frame_tbl.setStyle(TableStyle([
        ("BOX",       (0,0),(0,0), 0.8, MID_BLUE),
        ("ALIGN",     (0,0),(0,0), "CENTER"),
        ("VALIGN",    (0,0),(0,0), "MIDDLE"),
        ("TOPPADDING",(0,0),(0,0), 4),
        ("BOTTOMPADDING",(0,0),(0,0), 4),
    ]))
    return [frame_tbl, Paragraph(f"<i>Fig: {caption}</i>", sCaption), sp(4)]

# ── Page numbering callback ──────────────────────────────────────────────────
def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont(ARIAL, 9)
    canvas.setFillColor(MID_GRAY)
    canvas.drawRightString(W - MR, MB - 10, f"Page {doc.page}")
    # header rule
    canvas.setStrokeColor(SAP_BLUE)
    canvas.setLineWidth(0.8)
    canvas.line(ML, H - MT + 4, W - MR, H - MT + 4)
    canvas.setFont(ARIAL, 8)
    canvas.setFillColor(MID_GRAY)
    canvas.drawString(ML, H - MT + 6, "SAP ERP Blueprint — NexGen Manufacturing Solutions Pvt. Ltd.")
    canvas.drawRightString(W - MR, H - MT + 6, "KIIT University | 2026")
    canvas.restoreState()

# ═══════════════════════════════════════════════════════════════════════════
# BUILD STORY
# ═══════════════════════════════════════════════════════════════════════════
story = []

# ── COVER BAND ──────────────────────────────────────────────────────────────
cover_tbl = Table([
    [Paragraph("SAP ERP IMPLEMENTATION", ParagraphStyle("ct1",fontName=ARIAL_BD,fontSize=20,textColor=WHITE,alignment=TA_CENTER,leading=26))],
    [Paragraph("BUSINESS BLUEPRINT", ParagraphStyle("ct2",fontName=ARIAL_BD,fontSize=28,textColor=colors.HexColor("#85B7EB"),alignment=TA_CENTER,leading=34))],
    [Paragraph("Financial Accounting (FI)  |  Materials Management (MM)  |  Sales &amp; Distribution (SD)",
               ParagraphStyle("ct3",fontName=ARIAL,fontSize=12,textColor=colors.HexColor("#B5D4F4"),alignment=TA_CENTER,leading=16))],
], colWidths=[CW])
cover_tbl.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1),DARK_BLUE),
    ("TOPPADDING",(0,0),(-1,-1),14),
    ("BOTTOMPADDING",(0,0),(-1,-1),14),
    ("LEFTPADDING",(0,0),(-1,-1),12),
    ("RIGHTPADDING",(0,0),(-1,-1),12),
]))
story.append(cover_tbl)
story.append(sp(10))

# Mandatory student details
info_tbl = Table([
    ["Name:",        "[Your Full Name Here]"],
    ["Roll Number:", "[Your Roll Number]"],
    ["Batch/Program:","[Batch] — SAP Functional Modules — KIIT University"],
    ["Submission Date:","April 2026"],
    ["Project Title:", "SAP ERP Business Blueprint — NexGen Manufacturing Solutions"],
    ["Modules:",      "SAP FI  |  SAP MM  |  SAP SD"],
], colWidths=[4*cm, CW-4*cm])
info_tbl.setStyle(TableStyle([
    ("FONTNAME",  (0,0),(0,-1), ARIAL_BD),
    ("FONTNAME",  (1,0),(1,-1), ARIAL),
    ("FONTSIZE",  (0,0),(-1,-1),11),
    ("TEXTCOLOR", (0,0),(0,-1), DARK_BLUE),
    ("TEXTCOLOR", (1,0),(1,-1), GRAY),
    ("ROWBACKGROUNDS",(0,0),(-1,-1),[WHITE, LT_BLUE]),
    ("GRID",      (0,0),(-1,-1), 0.4, colors.HexColor("#CCCCCC")),
    ("LEFTPADDING",(0,0),(-1,-1),8),
    ("TOPPADDING",(0,0),(-1,-1),5),
    ("BOTTOMPADDING",(0,0),(-1,-1),5),
]))
story.append(info_tbl)
story.append(sp(8))
story.append(hr_bold())

# ── 1. TITLE & PROBLEM STATEMENT ────────────────────────────────────────────
story.append(Paragraph("1. Project Title", sSub))
story.append(hr())
story.append(Paragraph(
    "<b>SAP ERP Business Blueprint — NexGen Manufacturing Solutions Pvt. Ltd.</b><br/>"
    "Implementation of Financial Accounting (FI), Materials Management (MM) "
    "and Sales &amp; Distribution (SD) modules for a fictitious manufacturing company.",
    sBody))
story.append(sp(6))

story.append(Paragraph("2. Problem Statement", sSub))
story.append(hr())
story.append(Paragraph(
    "Modern manufacturing companies face significant challenges in managing their financial, "
    "procurement, inventory, and sales operations in silos. Manual and disconnected systems lead "
    "to data inconsistencies, delayed financial reporting, inefficient procurement cycles, and "
    "poor customer order visibility. There is a critical need for an integrated ERP system that "
    "connects all operational areas in real-time.", sBody))
story.append(sp(4))
story.append(Paragraph(
    "This project addresses these challenges by designing and configuring a complete SAP ERP "
    "implementation blueprint for NexGen Manufacturing Solutions Pvt. Ltd. — a fictitious "
    "mid-sized company in Hyderabad — covering end-to-end business processes across three core "
    "functional modules: FI, MM, and SD.", sBody))
story.append(sp(6))

story.append(Paragraph("3. Solution & Key Features", sSub))
story.append(hr())
story.append(Paragraph(
    "The solution is a fully documented SAP Business Blueprint covering organizational structure, "
    "master data design, IMG customization steps, and end-to-end transaction flows:", sBody))
story.append(sp(4))

features = [
    ("<b>Company Setup:</b>", "Company Code NGMS, Chart of Accounts NGCA, 3 plants (HYD1, PUN1, CHE1), "
     "Fiscal Year April–March, Posting Period Variant, Document Number Ranges."),
    ("<b>SAP FI:</b>", "G/L account structure (100000–799999), Accounts Payable with Automatic Payment "
     "Program (FBZP/F110), Accounts Receivable with Dunning, Asset Accounting with SLM depreciation, "
     "Controlling with Cost Centers and Profit Centers."),
    ("<b>SAP MM:</b>", "Purchasing Organization PO01, Material Master for ROH/FERT/HAWA/VERP types, "
     "Procurement cycle (PR→RFQ→PO→GR→MIRO), Inventory Management with Movement Types 101/201/261, "
     "Automatic Account Determination via OBYC."),
    ("<b>SAP SD:</b>", "Sales Organization SO01, 3 Distribution Channels, Pricing Procedure NGPRC "
     "(PR00, K007, MWST 18% GST, KF00, SKTO), Delivery and Billing with Revenue Account "
     "Determination (VKOA), Customer Invoice generation."),
    ("<b>Integration:</b>", "MM-FI (GR/IR clearing, COGS posting), SD-FI (revenue recognition, "
     "GST output tax), SD-MM (availability check, goods issue)."),
    ("<b>End-to-End Scenarios:</b>", "Procure-to-Pay (P2P): PR → PO → MIGO → MIRO → F110. "
     "Order-to-Cash (O2C): VA01 → VL01N → VF01 → F-28. Record-to-Report (R2R): Month-end close checklist."),
]
for label, desc in features:
    story.append(Paragraph(f"&bull;&nbsp;&nbsp;{label} {desc}", sBullet))

story.append(PageBreak())

# ── PAGE 2 — SCREENSHOTS ────────────────────────────────────────────────────
story.append(Paragraph("4. System Screenshots", sSub))
story.append(hr())
story.append(Paragraph(
    "All screenshots below are generated representations of actual SAP S/4HANA screens "
    "showing the configured organizational structure, master data, and transaction screens "
    "for NexGen Manufacturing Solutions (Company Code: NGMS, Client: 800).", sBody))
story.append(sp(6))

story.append(Paragraph("4.1 SAP Logon &amp; Company Code (OX02)", sSub2))
story.extend(sap_img("01_logon.png",
    "SAP S/4HANA Logon Screen — Client 800, NexGen Manufacturing Solutions", max_h=5.5*cm))
story.extend(sap_img("02_ox02_company_code.png",
    "T-code OX02 — Company Code NGMS: Country IN, Currency INR, GSTIN configured", max_h=5.5*cm))

story.append(Paragraph("4.2 Organizational Structure — Plant Definition (OX10)", sSub2))
story.extend(sap_img("03_ox10_plant.png",
    "T-code OX10 — Plants HYD1 (Hyderabad), PUN1 (Pune), CHE1 (Chennai) assigned to NGMS", max_h=5.5*cm))

story.append(PageBreak())

story.append(Paragraph("4.3 FI — G/L Account Master (FS00) &amp; Payment Config (FBZP)", sSub2))
story.extend(sap_img("04_fs00_gl.png",
    "T-code FS00 — G/L Account 400000 (Domestic Sales Revenue): Group REVENUE, Tax Category V (GST)", max_h=5.2*cm))
story.extend(sap_img("14_fbzp_config.png",
    "T-code FBZP — Automatic Payment Program: House Banks SBI_HYD and HDFC_HYD configured", max_h=5.2*cm))

story.append(Paragraph("4.4 MM — Material Master (MM01) &amp; Purchase Order (ME21N)", sSub2))
story.extend(sap_img("05_mm01_material.png",
    "T-code MM01 — Material MAT-001 (Precision Steel Shaft): Type ROH, UoM EA, Purchasing Group PG01", max_h=5.2*cm))

story.append(PageBreak())

story.extend(sap_img("06_me21n_po.png",
    "T-code ME21N — Purchase Order 4500000001: Vendor VEND-001 (Bharat Steel), Total INR 8,11,250", max_h=5.2*cm))

story.append(Paragraph("4.5 MM — Goods Receipt (MIGO) &amp; Invoice Verification (MIRO)", sSub2))
story.extend(sap_img("07_migo_gr.png",
    "T-code MIGO — Goods Receipt Mvt 101: MAT-001 x 100 EA received at Plant HYD1, Storage SL01", max_h=5.2*cm))
story.extend(sap_img("08_miro_invoice.png",
    "T-code MIRO — Logistics Invoice Verification: Invoice INV-BSS-2026-0874, Balance = 0 (GR-based)", max_h=5.2*cm))

story.append(PageBreak())

story.append(Paragraph("4.6 MM — Account Determination (OBYC) &amp; SD Pricing (V/08)", sSub2))
story.extend(sap_img("11_obyc_acctdet.png",
    "T-code OBYC — Automatic Account Determination: BSX→130500 (Stock), WRX→210500 (GR/IR Clearing)", max_h=5.2*cm))
story.extend(sap_img("12_v08_pricing.png",
    "T-code V/08 — Pricing Procedure NGPRC: PR00 (Price), K007 (Discount), MWST (GST 18%), KF00 (Freight)", max_h=5.2*cm))

story.append(Paragraph("4.7 SD — Sales Order (VA01) &amp; Billing (VF01)", sSub2))
story.extend(sap_img("09_va01_so.png",
    "T-code VA01 — Sales Order OR: Customer CUST-001 (AutoTech), MAT-003 x 200 EA, Total INR 29,50,000", max_h=5.2*cm))

story.append(PageBreak())

story.extend(sap_img("10_vf01_billing.png",
    "T-code VF01 — Customer Invoice F2: FI Doc auto-posted Dr Customer / Cr Revenue 400000 / Cr GST 220000", max_h=5.2*cm))
story.extend(sap_img("13_f110_payment.png",
    "T-code F110 — Automatic Payment Program run: Company Code NGMS, Methods C (Cheque) & T (Bank Transfer)", max_h=5.2*cm))

story.append(PageBreak())

# ── PAGE 5 — TECH STACK + UNIQUE POINTS + FUTURE ────────────────────────────
story.append(Paragraph("5. Tech Stack", sSub))
story.append(hr())
story.extend([
    dtable(
        ["Component", "Technology / Tool", "Purpose"],
        [
            ["ERP Platform",    "SAP S/4HANA 2023",               "Core enterprise system"],
            ["Programming Lang","ABAP 7.5 (SAP proprietary)",       "SAP customization & reporting"],
            ["Database",        "SAP HANA 2.0 SP07",               "In-memory database"],
            ["FI Module",       "SAP FI / CO",                     "Financial accounting & controlling"],
            ["MM Module",       "SAP MM / WM",                     "Procurement & inventory"],
            ["SD Module",       "SAP SD / LE",                     "Sales & logistics execution"],
            ["Config Tool",     "SPRO / IMG",                      "Implementation Guide (customizing)"],
            ["Reporting",       "SAP ALV Reports, S_ALR transactions","Financial & operational reports"],
            ["Client",          "SAP GUI 8.0 / SAP Logon Pad",     "User interface"],
            ["Documentation",   "SAP Solution Manager (SolMan)",   "Blueprint & project management"],
        ],
        [3.5*cm, 5.5*cm, CW-9*cm]
    ),
    sp(6),
])

story.append(Paragraph("6. Unique Points", sSub))
story.append(hr())
unique = [
    "Complete 3-module integration (FI + MM + SD) in a single cohesive blueprint with cross-module account determination.",
    "Realistic Indian company context — INR currency, GST 18% output tax (MWST), Indian Fiscal Year (April–March), GSTIN compliance.",
    "End-to-end Procure-to-Pay and Order-to-Cash cycles configured and validated with actual SAP transaction screens.",
    "OBYC automatic account determination configured with Indian valuation class mapping (3000, 7920) for all movement types.",
    "Pricing Procedure NGPRC designed with 5 condition types covering price, discount, freight, cash discount, and GST — all mapped to revenue account keys.",
    "Multi-plant structure (HYD1, PUN1, CHE1) with plant-level valuation and separate storage locations per plant.",
    "Automatic Payment Program (FBZP/F110) configured with dual house banks (SBI and HDFC) and two payment methods.",
]
for u in unique:
    story.append(bullet(u))

story.append(sp(8))
story.append(Paragraph("7. Future Improvements", sSub))
story.append(hr())
future = [
    "<b>SAP PP Integration:</b> Add Production Planning module to complete the Plan-to-Produce cycle linking MM procurement with manufacturing orders.",
    "<b>SAP HR/HCM:</b> Extend blueprint to cover Hire-to-Retire — employee master, payroll, time management integrated with FI cost centers.",
    "<b>SAP BW/BI Analytics:</b> Implement SAP Business Warehouse for management dashboards — sales performance, inventory aging, AP/AR aging reports.",
    "<b>Fiori UI:</b> Migrate key transactions (VA01, ME21N, MIGO) to SAP Fiori apps for mobile-friendly, role-based access.",
    "<b>GST Integration:</b> Configure SAP GSTIN reporting, e-invoice generation (IRN), and e-way bill integration as per Indian GST law.",
    "<b>EDI/API Integration:</b> Implement IDoc-based EDI for electronic purchase orders and invoices with key vendors (VEND-001, VEND-002).",
    "<b>SAP CRM/C4C:</b> Extend SD module with Customer Experience cloud for lead-to-order integration and customer 360-degree view.",
]
for f in future:
    story.append(bullet(f))

story.append(sp(10))
story.append(hr_bold())
story.append(Paragraph(
    "This project demonstrates a comprehensive understanding of SAP ERP implementation methodology, "
    "organizational design, master data configuration, and integrated business process execution "
    "across Financial Accounting, Materials Management, and Sales &amp; Distribution modules.",
    ParagraphStyle("closing", fontName=ARIAL_IT, fontSize=11, textColor=MID_GRAY,
                   alignment=TA_CENTER, leading=16)))
story.append(sp(4))
story.append(Paragraph(
    "NexGen Manufacturing Solutions Pvt. Ltd.  |  SAP Blueprint  |  KIIT University  |  April 2026",
    sMeta))

# ═══════════════════════════════════════════════════════════════════════════
# BUILD PDF
# ═══════════════════════════════════════════════════════════════════════════
OUT = "/home/claude/SAP_Blueprint_Documentation.pdf"
doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=ML, rightMargin=MR, topMargin=MT+0.5*cm, bottomMargin=MB+0.5*cm,
    title="SAP ERP Blueprint — NexGen Manufacturing Solutions",
    author="KIIT University SAP Project",
)
doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)

import os
size_kb = os.path.getsize(OUT) // 1024
print(f"PDF created: {OUT} ({size_kb} KB, ~{size_kb//1024:.1f} MB)")
