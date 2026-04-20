from PIL import Image, ImageDraw, ImageFont
import os

# Fonts
SANS      = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO      = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

def fnt(path, size):
    try:    return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

# SAP color palette
SAP_BLUE   = (0,   112, 210)
DARK_BLUE  = (0,   51,  102)
MID_BLUE   = (24,  95,  165)
LIGHT_BLUE = (230, 241, 251)
HEADER_BG  = (0,   70,  127)
MENU_BG    = (240, 244, 248)
WHITE      = (255, 255, 255)
GRAY_BG    = (245, 245, 245)
GRAY_LIGHT = (230, 230, 230)
GRAY_DARK  = (100, 100, 100)
BLACK      = (20,  20,  20)
GREEN      = (0,   140, 70)
ORANGE     = (232, 160, 0)
RED        = (200, 50,  50)
BORDER     = (180, 180, 180)

OUT = "/home/claude/sap_imgs"
os.makedirs(OUT, exist_ok=True)

W, H = 1100, 700

# ─── common SAP chrome ────────────────────────────────────────────────────────
def sap_shell(draw, img, tcode, title, subtitle=""):
    # title bar
    draw.rectangle([0,0,W,36], fill=DARK_BLUE)
    draw.text((12,8), f"SAP Easy Access  —  {tcode}", font=fnt(SANS_BOLD,14), fill=WHITE)
    draw.text((W-200,10), "NexGen / NGMS / EN", font=fnt(SANS,11), fill=(180,210,240))

    # menu bar
    draw.rectangle([0,36,W,58], fill=MENU_BG)
    for i,m in enumerate(["System","Edit","Favorites","Extras","Help"]):
        x = 12 + i*90
        draw.text((x,41), m, font=fnt(SANS,12), fill=DARK_BLUE)

    # toolbar
    draw.rectangle([0,58,W,82], fill=(250,250,252))
    draw.line([0,82,W,82], fill=BORDER, width=1)
    for i,lbl in enumerate(["Back","Exit","Cancel","Print","Find","Save"]):
        bx = 12+i*68
        draw.rectangle([bx,62,bx+58,78], outline=BORDER, width=1)
        draw.text((bx+6,64), lbl, font=fnt(SANS,10), fill=GRAY_DARK)

    # tcode box
    draw.rectangle([W-130,62,W-12,78], outline=BORDER, width=1)
    draw.text((W-126,64), f"T-Code: {tcode}", font=fnt(MONO,10), fill=DARK_BLUE)

    # content header band
    draw.rectangle([0,82,W,118], fill=HEADER_BG)
    draw.text((16,88), title, font=fnt(SANS_BOLD,17), fill=WHITE)
    if subtitle:
        draw.text((16,106), subtitle, font=fnt(SANS,11), fill=(180,210,240))

    # status bar
    draw.rectangle([0,H-24,W,H], fill=MENU_BG)
    draw.line([0,H-24,W,H-24], fill=BORDER, width=1)
    draw.text((10,H-18), "System ready  |  Client 800  |  NexGen Manufacturing Solutions Pvt. Ltd.", font=fnt(SANS,10), fill=GRAY_DARK)

def field_row(draw, x, y, label, value, w_label=220, w_value=320, required=False):
    draw.text((x, y+3), label + ("*" if required else ""), font=fnt(SANS,12), fill=GRAY_DARK)
    draw.rectangle([x+w_label, y, x+w_label+w_value, y+20], outline=BORDER, fill=WHITE, width=1)
    draw.text((x+w_label+6, y+3), value, font=fnt(SANS,12), fill=BLACK)
    return y+28

def section_label(draw, x, y, text):
    draw.rectangle([x,y,W-x,y+22], fill=LIGHT_BLUE)
    draw.text((x+8,y+4), text, font=fnt(SANS_BOLD,12), fill=DARK_BLUE)
    return y+30

# ════════════════════════════════════════════════════════════════════════════
# 1. SAP LOGON SCREEN
# ════════════════════════════════════════════════════════════════════════════
def img_logon():
    img = Image.new("RGB",(W,H), WHITE)
    d   = ImageDraw.Draw(img)
    d.rectangle([0,0,W,H], fill=(240,244,248))

    # banner
    d.rectangle([0,0,W,90], fill=DARK_BLUE)
    d.text((24,16), "SAP", font=fnt(SANS_BOLD,40), fill=WHITE)
    d.text((100,28), "Logon", font=fnt(SANS,22), fill=(130,180,230))
    d.text((W-220,34), "Version: SAP S/4HANA 2023", font=fnt(SANS,11), fill=(150,190,230))

    # login card
    cx,cy,cw,ch = 320,130,460,400
    d.rectangle([cx,cy,cx+cw,cy+ch], fill=WHITE, outline=BORDER, width=1)

    d.rectangle([cx,cy,cx+cw,cy+44], fill=HEADER_BG)
    d.text((cx+16,cy+12), "NexGen Manufacturing Solutions — SAP S/4HANA", font=fnt(SANS_BOLD,12), fill=WHITE)

    y = cy+64
    for label, val, pw in [("Client","800",False),("User","NGMS_USR01",False),("Password","••••••••••",True),("Language","EN",False)]:
        d.text((cx+24,y), label, font=fnt(SANS_BOLD,12), fill=GRAY_DARK)
        d.rectangle([cx+130,y-2,cx+cw-24,y+22], fill=WHITE, outline=BORDER, width=1)
        d.text((cx+138,y+2), val, font=fnt(MONO,12), fill=BLACK if not pw else GRAY_DARK)
        y+=44

    # logon button
    d.rectangle([cx+cw-130,cy+ch-54,cx+cw-24,cy+ch-28], fill=SAP_BLUE)
    d.text((cx+cw-104,cy+ch-50), "Log On", font=fnt(SANS_BOLD,13), fill=WHITE)

    # system info box
    d.rectangle([cx,cy+ch+16,cx+cw,cy+ch+90], fill=GRAY_BG, outline=BORDER, width=1)
    for i,(k,v) in enumerate([("System","PRD — NexGen SAP S/4HANA"),("Host","sap-hana-server-01.ngms.in"),("IP","10.0.1.45"),("DB","HANA 2.0 SP07")]):
        d.text((cx+16, cy+ch+24+i*16), f"{k}:  {v}", font=fnt(SANS,11), fill=GRAY_DARK)

    d.rectangle([0,H-28,W,H], fill=DARK_BLUE)
    d.text((12,H-20), "SAP S/4HANA 2023  |  © NexGen Manufacturing Solutions Pvt. Ltd.", font=fnt(SANS,10), fill=(160,200,240))
    img.save(f"{OUT}/01_logon.png")
    print("01_logon.png done")

# ════════════════════════════════════════════════════════════════════════════
# 2. OX02 — COMPANY CODE
# ════════════════════════════════════════════════════════════════════════════
def img_ox02():
    img = Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(img)
    sap_shell(d,img,"OX02","Edit Company Code Data","Define organizational unit for financial accounting")
    y=136
    y=section_label(d,12,y,"Company Code — General Data")
    y=field_row(d,20,y,"Company Code",      "NGMS",   required=True)
    y=field_row(d,20,y,"Company Name",      "NexGen Manufacturing Solutions Pvt. Ltd.", required=True)
    y=field_row(d,20,y,"City",              "Hyderabad")
    y=field_row(d,20,y,"Country",           "IN  — India", required=True)
    y=field_row(d,20,y,"Currency",          "INR  — Indian Rupee", required=True)
    y=field_row(d,20,y,"Language",          "EN  — English", required=True)
    y+=12
    y=section_label(d,12,y,"Address & Tax Details")
    y=field_row(d,20,y,"Street / P.O. Box", "Plot 42, HITEC City")
    y=field_row(d,20,y,"Postal Code / City","500081  /  Hyderabad")
    y=field_row(d,20,y,"Region",            "TG  — Telangana")
    y=field_row(d,20,y,"GSTIN",             "36AABCN1234M1ZX")
    y=field_row(d,20,y,"CIN",               "U28999TG2020PTC140123")
    y+=16
    d.rectangle([20,y,280,y+26], fill=SAP_BLUE)
    d.text((60,y+5),"Save (Ctrl+S)", font=fnt(SANS_BOLD,13), fill=WHITE)
    img.save(f"{OUT}/02_ox02_company_code.png"); print("02_ox02 done")

# ════════════════════════════════════════════════════════════════════════════
# 3. OX10 — PLANT DEFINITION
# ════════════════════════════════════════════════════════════════════════════
def img_ox10():
    img=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(img)
    sap_shell(d,img,"OX10","Plants — Overview & Definition","Logistics organizational unit | Company Code NGMS")
    # table header
    y=130
    cols=[(20,120,"Plant"),(140,200,"Name"),(340,120,"Company Code"),(460,100,"Country"),(560,200,"City"),(760,120,"State")]
    d.rectangle([12,y,W-12,y+24], fill=DARK_BLUE)
    for x,w,lbl in cols:
        d.text((x+6,y+5),lbl,font=fnt(SANS_BOLD,11),fill=WHITE)
    y+=24
    rows=[
        ("HYD1","Hyderabad Main Plant","NGMS","IN","Hyderabad","TG"),
        ("PUN1","Pune Manufacturing Plant","NGMS","IN","Pune","MH"),
        ("CHE1","Chennai Depot","NGMS","IN","Chennai","TN"),
    ]
    for ri,(pl,name,cc,cty,city,st) in enumerate(rows):
        bg=LIGHT_BLUE if ri%2==0 else WHITE
        d.rectangle([12,y,W-12,y+22],fill=bg)
        for (x,w,_),val in zip(cols,[pl,name,cc,cty,city,st]):
            d.text((x+6,y+4),val,font=fnt(SANS,12),fill=BLACK)
        y+=22
    # detail for HYD1
    y+=20
    y=section_label(d,12,y,"Selected Plant Detail — HYD1  (Hyderabad Main Plant)")
    y=field_row(d,20,y,"Plant","HYD1",required=True)
    y=field_row(d,20,y,"Name 1","Hyderabad Main Plant",required=True)
    y=field_row(d,20,y,"Company Code","NGMS — NexGen Manufacturing Solutions",required=True)
    y=field_row(d,20,y,"Factory Calendar","IN — India Factory Calendar")
    y=field_row(d,20,y,"Valuation Area","HYD1 — Plant Level Valuation")
    img.save(f"{OUT}/03_ox10_plant.png"); print("03_ox10 done")

# ════════════════════════════════════════════════════════════════════════════
# 4. FS00 — G/L ACCOUNT
# ════════════════════════════════════════════════════════════════════════════
def img_fs00():
    img=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(img)
    sap_shell(d,img,"FS00","Edit G/L Account Centrally","Chart of Accounts: NGCA | Company Code: NGMS")
    y=130
    # tabs
    for i,tab in enumerate(["Type/Description","Control Data","Create/Bank/Interest","Key Word / Translation","Information (C/A)"]):
        bg=WHITE if i==0 else MENU_BG
        tw=len(tab)*8+16
        d.rectangle([12+i*175,y,12+i*175+170,y+22],fill=bg,outline=BORDER,width=1)
        d.text((12+i*175+8,y+5),tab,font=fnt(SANS,10),fill=DARK_BLUE if i==0 else GRAY_DARK)
    y+=30
    d.rectangle([12,y-4,W-12,y+14],fill=LIGHT_BLUE)
    d.text((18,y),f"G/L Account: 400000     Chart of Accounts: NGCA",font=fnt(SANS_BOLD,12),fill=DARK_BLUE)
    y+=22
    y=section_label(d,12,y,"Type and Description")
    y=field_row(d,20,y,"Account Group",     "REVENUE — Revenue Accounts",required=True)
    y=field_row(d,20,y,"P&L Statement Acct","✓  (Income Statement Account)")
    y=field_row(d,20,y,"Short Text",        "Domestic Sales Revenue",required=True)
    y=field_row(d,20,y,"G/L Account Long Text","Sales Revenue — Domestic (India)",required=True)
    y+=10
    y=section_label(d,12,y,"Company Code Data — NGMS")
    y=field_row(d,20,y,"Account Currency",  "INR — Indian Rupee")
    y=field_row(d,20,y,"Tax Category",      "V  — Output Tax (GST)")
    y=field_row(d,20,y,"Recon. Account for","—  (Not a reconciliation account)")
    y=field_row(d,20,y,"Line Item Display", "✓  Active")
    y=field_row(d,20,y,"Sort Key",          "001 — Posting Date")
    y+=16
    d.rectangle([20,y,200,y+26],fill=SAP_BLUE)
    d.text((42,y+5),"Save",font=fnt(SANS_BOLD,13),fill=WHITE)
    img.save(f"{OUT}/04_fs00_gl.png"); print("04_fs00 done")

# ════════════════════════════════════════════════════════════════════════════
# 5. MM01 — MATERIAL MASTER
# ════════════════════════════════════════════════════════════════════════════
def img_mm01():
    img=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(img)
    sap_shell(d,img,"MM01","Create Material — Basic Data 1","Material: MAT-001 | Industry Sector: M — Mechanical Engineering")
    y=130
    # org level bar
    d.rectangle([12,y,W-12,y+26],fill=GRAY_BG,outline=BORDER,width=1)
    for x,lbl,val in [(20,"Plant:","HYD1"),(160,"Sales Org:","SO01"),(300,"Dist Channel:","DC01"),(440,"Stor Location:","SL01")]:
        d.text((x,y+6),lbl,font=fnt(SANS_BOLD,11),fill=GRAY_DARK)
        d.text((x+len(lbl)*7+4,y+6),val,font=fnt(SANS,11),fill=DARK_BLUE)
    y+=34
    # view tabs
    for i,v in enumerate(["Basic Data 1","Basic Data 2","Purchasing","MRP 1","MRP 2","Accounting 1","Sales Org 1"]):
        bg=LIGHT_BLUE if i==0 else MENU_BG
        d.rectangle([12+i*138,y,12+i*138+134,y+22],fill=bg,outline=BORDER,width=1)
        d.text((16+i*138,y+5),v,font=fnt(SANS,10),fill=DARK_BLUE if i==0 else GRAY_DARK)
    y+=30
    y=field_row(d,20,y,"Material Number",   "MAT-001",required=True,w_value=260)
    y=field_row(d,20,y,"Material Desc.",    "Precision Steel Shaft",required=True,w_value=360)
    y=field_row(d,20,y,"Base Unit of Meas.","EA  — Each",required=True,w_value=200)
    y=field_row(d,20,y,"Material Type",     "ROH — Raw Material",required=True,w_value=240)
    y=field_row(d,20,y,"Industry Sector",   "M  — Mechanical Engineering",w_value=260)
    y=field_row(d,20,y,"Material Group",    "MG01 — Steel Components",w_value=260)
    y+=10
    y=section_label(d,12,y,"Dimensions / Weight")
    y=field_row(d,20,y,"Gross Weight",      "2.500  KG",w_value=160)
    y=field_row(d,20,y,"Net Weight",        "2.450  KG",w_value=160)
    y=field_row(d,20,y,"Volume",            "0.003  M3",w_value=160)
    img.save(f"{OUT}/05_mm01_material.png"); print("05_mm01 done")

# ════════════════════════════════════════════════════════════════════════════
# 6. ME21N — PURCHASE ORDER
# ════════════════════════════════════════════════════════════════════════════
def img_me21n():
    img=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(img)
    sap_shell(d,img,"ME21N","Create Purchase Order","Standard PO | Vendor: VEND-001  Bharat Steel Suppliers")
    y=130
    d.rectangle([12,y,W-12,y+26],fill=GRAY_BG,outline=BORDER,width=1)
    d.text((20,y+6),"Doc. Type: NB — Standard PO     PO Date: 15.04.2026     Purch. Org: PO01     Purch. Group: PG01     Company Code: NGMS",font=fnt(SANS,11),fill=BLACK)
    y+=34
    # vendor header
    y=section_label(d,12,y,"Vendor / Header Data")
    y=field_row(d,20,y,"Vendor",            "VEND-001  —  Bharat Steel Suppliers, Mumbai",required=True)
    y=field_row(d,20,y,"Payment Terms",     "ZN30  —  Net 30 Days")
    y=field_row(d,20,y,"Delivery Terms",    "DDP  —  Delivered Duty Paid")
    y=field_row(d,20,y,"Currency",          "INR  —  Indian Rupee")
    y+=10
    # line items
    y=section_label(d,12,y,"Line Items")
    hcols=[(12,50,"Itm"),(62,140,"Material"),(202,220,"Short Text"),(422,80,"Qty"),(502,60,"UoM"),(562,110,"Deliv. Date"),(672,130,"Net Price"),(802,80,"Plant"),(882,100,"Stor. Loc.")]
    d.rectangle([12,y,W-12,y+22],fill=DARK_BLUE)
    for x,w,lbl in hcols:
        d.text((x+4,y+4),lbl,font=fnt(SANS_BOLD,10),fill=WHITE)
    y+=22
    items=[("10","MAT-001","Precision Steel Shaft","100","EA","30.04.2026","2,500.00","HYD1","SL01"),
           ("20","MAT-002","Electronic Control Unit","50","EA","30.04.2026","8,750.00","HYD1","SL01")]
    for ri,row in enumerate(items):
        bg=LIGHT_BLUE if ri%2==0 else WHITE
        d.rectangle([12,y,W-12,y+20],fill=bg)
        for (x,w,_),val in zip(hcols,row):
            d.text((x+4,y+3),val,font=fnt(SANS,10),fill=BLACK)
        y+=20
    y+=16
    d.text((W-300,y),"Net Order Value:  INR  6,87,500.00",font=fnt(SANS_BOLD,13),fill=DARK_BLUE)
    y+=20
    d.text((W-300,y),"Tax (GST 18%):   INR  1,23,750.00",font=fnt(SANS,12),fill=GRAY_DARK)
    y+=20
    d.text((W-300,y),"Total PO Value:   INR  8,11,250.00",font=fnt(SANS_BOLD,14),fill=SAP_BLUE)
    img.save(f"{OUT}/06_me21n_po.png"); print("06_me21n done")

# ════════════════════════════════════════════════════════════════════════════
# 7. MIGO — GOODS RECEIPT
# ════════════════════════════════════════════════════════════════════════════
def img_migo():
    img=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(img)
    sap_shell(d,img,"MIGO","Goods Receipt — Purchase Order","Movement Type: 101 | Plant: HYD1")
    y=130
    d.rectangle([12,y,W-12,y+26],fill=GRAY_BG,outline=BORDER,width=1)
    d.text((20,y+6),"Goods Receipt      Purchase Order      Movement Type: 101 — GR for PO",font=fnt(SANS,11),fill=BLACK)
    y+=34
    y=section_label(d,12,y,"Document Header")
    y=field_row(d,20,y,"Document Date",     "19.04.2026",required=True)
    y=field_row(d,20,y,"Posting Date",      "19.04.2026",required=True)
    y=field_row(d,20,y,"Reference (PO No.)","4500000001",required=True)
    y=field_row(d,20,y,"Bill of Lading",    "BL-2026-0419-001")
    y=field_row(d,20,y,"Header Text",       "GR against PO 4500000001 — Bharat Steel")
    y+=10
    y=section_label(d,12,y,"Line Items (Movement Type 101)")
    hcols=[(12,50,"Itm"),(62,150,"Material"),(212,200,"Material Description"),(412,70,"Qty"),(482,60,"UoM"),(542,90,"Plant"),(632,100,"Stor. Loc."),(732,80,"Batch"),(812,80,"OK")]
    d.rectangle([12,y,W-12,y+22],fill=DARK_BLUE)
    for x,w,lbl in hcols:
        d.text((x+4,y+4),lbl,font=fnt(SANS_BOLD,10),fill=WHITE)
    y+=22
    for ri,(itm,mat,desc,qty,uom,plant,sl,batch,ok) in enumerate([
        ("1","MAT-001","Precision Steel Shaft","100","EA","HYD1","SL01","","✓"),
        ("2","MAT-002","Electronic Control Unit","50","EA","HYD1","SL01","","✓"),
    ]):
        bg=LIGHT_BLUE if ri%2==0 else WHITE
        d.rectangle([12,y,W-12,y+20],fill=bg)
        for (x,w,_),val in zip(hcols,[itm,mat,desc,qty,uom,plant,sl,batch,ok]):
            color=GREEN if val=="✓" else BLACK
            d.text((x+4,y+3),val,font=fnt(SANS,10),fill=color)
        y+=20
    y+=20
    d.rectangle([20,y,160,y+26],fill=SAP_BLUE)
    d.text((42,y+5),"Post (F6)",font=fnt(SANS_BOLD,13),fill=WHITE)
    d.rectangle([180,y,320,y+26],fill=MENU_BG,outline=BORDER,width=1)
    d.text((200,y+5),"Check (F5)",font=fnt(SANS,13),fill=DARK_BLUE)
    img.save(f"{OUT}/07_migo_gr.png"); print("07_migo done")

# ════════════════════════════════════════════════════════════════════════════
# 8. MIRO — INVOICE VERIFICATION
# ════════════════════════════════════════════════════════════════════════════
def img_miro():
    img=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(img)
    sap_shell(d,img,"MIRO","Enter Incoming Invoice","Logistics Invoice Verification | Company Code: NGMS")
    y=130
    d.rectangle([12,y,W-12,y+26],fill=GRAY_BG,outline=BORDER,width=1)
    d.text((20,y+6),"Transaction: Invoice  |  Company Code: NGMS  |  Reference PO: 4500000001",font=fnt(SANS,11),fill=BLACK)
    y+=34
    y=section_label(d,12,y,"Invoice Header")
    y=field_row(d,20,y,"Invoice Date",      "18.04.2026",required=True)
    y=field_row(d,20,y,"Posting Date",      "19.04.2026",required=True)
    y=field_row(d,20,y,"Reference",         "INV-BSS-2026-0874",required=True)
    y=field_row(d,20,y,"Amount",            "6,87,500.00",required=True)
    y=field_row(d,20,y,"Tax Amount",        "1,23,750.00")
    y=field_row(d,20,y,"Currency",          "INR — Indian Rupee")
    y=field_row(d,20,y,"Vendor",            "VEND-001 — Bharat Steel Suppliers, Mumbai")
    y+=10
    y=section_label(d,12,y,"PO Reference — Line Items")
    hcols=[(12,50,"Itm"),(62,180,"Short Text"),(242,80,"PO Qty"),(322,80,"GR Qty"),(402,80,"Inv. Qty"),(482,110,"Amount (INR)"),(592,80,"Tax Code"),(672,100,"G/L Account")]
    d.rectangle([12,y,W-12,y+22],fill=DARK_BLUE)
    for x,w,lbl in hcols:
        d.text((x+4,y+4),lbl,font=fnt(SANS_BOLD,10),fill=WHITE)
    y+=22
    for ri,(itm,desc,poq,grq,iq,amt,tax,gl) in enumerate([
        ("1","Precision Steel Shaft","100","100","100","2,50,000","V0","130500"),
        ("2","Electronic Control Unit","50","50","50","4,37,500","V0","130500"),
    ]):
        bg=LIGHT_BLUE if ri%2==0 else WHITE
        d.rectangle([12,y,W-12,y+20],fill=bg)
        for (x,w,_),val in zip(hcols,[itm,desc,poq,grq,iq,amt,tax,gl]):
            d.text((x+4,y+3),val,font=fnt(SANS,10),fill=BLACK)
        y+=20
    y+=12
    # balance indicator
    d.rectangle([W-200,y,W-12,y+26],fill=GREEN)
    d.text((W-184,y+5),"Balance: 0.00 ✓",font=fnt(SANS_BOLD,12),fill=WHITE)
    img.save(f"{OUT}/08_miro_invoice.png"); print("08_miro done")

# ════════════════════════════════════════════════════════════════════════════
# 9. VA01 — SALES ORDER
# ════════════════════════════════════════════════════════════════════════════
def img_va01():
    img=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(img)
    sap_shell(d,img,"VA01","Create Sales Order — Standard Order (OR)","Sales Area: SO01 / DC01 / DV01")
    y=130
    d.rectangle([12,y,W-12,y+26],fill=GRAY_BG,outline=BORDER,width=1)
    d.text((20,y+6),"Order Type: OR — Standard Order  |  Sales Org: SO01  |  Dist. Channel: DC01  |  Division: DV01",font=fnt(SANS,11),fill=BLACK)
    y+=34
    y=section_label(d,12,y,"Order Header")
    y=field_row(d,20,y,"Sold-To Party",     "CUST-001 — AutoTech Industries, Chennai",required=True)
    y=field_row(d,20,y,"Ship-To Party",     "CUST-001 — AutoTech Industries, Chennai")
    y=field_row(d,20,y,"Customer PO No.",   "ATIL-PO-2026-0423",required=True)
    y=field_row(d,20,y,"Customer PO Date",  "17.04.2026")
    y=field_row(d,20,y,"Req. Delivery Date","30.04.2026",required=True)
    y=field_row(d,20,y,"Pricing Date",      "19.04.2026")
    y+=10
    y=section_label(d,12,y,"Line Items")
    hcols=[(12,50,"Itm"),(62,120,"Material"),(182,200,"Description"),(382,70,"Qty"),(452,60,"UoM"),(512,130,"Net Price"),(642,110,"Amount (INR)"),(752,100,"Plant"),(852,100,"Sched. Dt.")]
    d.rectangle([12,y,W-12,y+22],fill=DARK_BLUE)
    for x,w,lbl in hcols:
        d.text((x+4,y+4),lbl,font=fnt(SANS_BOLD,10),fill=WHITE)
    y+=22
    for ri,(itm,mat,desc,qty,uom,price,amt,plant,dt) in enumerate([
        ("10","MAT-003","Assembled Gear Box","200","EA","12,500.00","25,00,000","HYD1","30.04.2026"),
    ]):
        d.rectangle([12,y,W-12,y+20],fill=LIGHT_BLUE if ri%2==0 else WHITE)
        for (x,w,_),val in zip(hcols,[itm,mat,desc,qty,uom,price,amt,plant,dt]):
            d.text((x+4,y+3),val,font=fnt(SANS,10),fill=BLACK)
        y+=20
    y+=16
    d.text((W-320,y),"Net Value:    INR  25,00,000.00",font=fnt(SANS_BOLD,12),fill=DARK_BLUE)
    y+=18; d.text((W-320,y),"GST (18%):   INR   4,50,000.00",font=fnt(SANS,11),fill=GRAY_DARK)
    y+=18; d.text((W-320,y),"Total Value: INR  29,50,000.00",font=fnt(SANS_BOLD,14),fill=SAP_BLUE)
    img.save(f"{OUT}/09_va01_so.png"); print("09_va01 done")

# ════════════════════════════════════════════════════════════════════════════
# 10. VF01 — BILLING DOCUMENT
# ════════════════════════════════════════════════════════════════════════════
def img_vf01():
    img=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(img)
    sap_shell(d,img,"VF01","Billing Document — Invoice (F2)","Customer: CUST-001 — AutoTech Industries | Company Code: NGMS")
    y=130
    d.rectangle([12,y,W-12,y+26],fill=GRAY_BG,outline=BORDER,width=1)
    d.text((20,y+6),"Billing Type: F2 — Invoice  |  Billing Date: 19.04.2026  |  Ref. Delivery: 80000001",font=fnt(SANS,11),fill=BLACK)
    y+=34
    y=section_label(d,12,y,"Billing Header")
    y=field_row(d,20,y,"Payer",             "CUST-001 — AutoTech Industries, Chennai",required=True)
    y=field_row(d,20,y,"Sales Organization","SO01 — India Sales Organization")
    y=field_row(d,20,y,"Billing Date",      "19.04.2026")
    y=field_row(d,20,y,"Payment Terms",     "ZN30 — Net 30 Days")
    y=field_row(d,20,y,"Incoterms",         "DDP — Delivered Duty Paid")
    y+=10
    y=section_label(d,12,y,"Pricing Summary")
    pricing=[
        ("PR00","Basic Price","25,00,000.00","ERL"),
        ("K007","Customer Discount 2%","-50,000.00","ERS"),
        ("MWST","GST Output Tax 18%","4,41,000.00","MWS"),
        ("KF00","Freight Charges","15,000.00","ERF"),
    ]
    for i,(ct,desc,amt,ak) in enumerate(pricing):
        bg=LIGHT_BLUE if i%2==0 else WHITE
        d.rectangle([20,y,W-20,y+20],fill=bg)
        d.text((26,y+3),ct,font=fnt(MONO,10),fill=DARK_BLUE)
        d.text((120,y+3),desc,font=fnt(SANS,11),fill=BLACK)
        d.text((W-250,y+3),amt,font=fnt(SANS,11),fill=BLACK)
        d.text((W-100,y+3),ak,font=fnt(MONO,10),fill=GRAY_DARK)
        y+=20
    y+=12
    d.rectangle([W-300,y,W-12,y+28],fill=DARK_BLUE)
    d.text((W-288,y+6),"Total Invoice Amount:  INR 29,06,000.00",font=fnt(SANS_BOLD,12),fill=WHITE)
    y+=40
    # FI document link
    d.rectangle([20,y,W-20,y+24],fill=(240,255,240),outline=(0,140,70),width=1)
    d.text((28,y+5),"FI Document Generated:  1800000001  |  Dr Customer A/c CUST-001  |  Cr Revenue A/c 400000  |  Cr GST Output 220000",font=fnt(SANS,11),fill=GREEN)
    img.save(f"{OUT}/10_vf01_billing.png"); print("10_vf01 done")

# ════════════════════════════════════════════════════════════════════════════
# 11. OBYC — ACCOUNT DETERMINATION
# ════════════════════════════════════════════════════════════════════════════
def img_obyc():
    img=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(img)
    sap_shell(d,img,"OBYC","Automatic Account Determination — Configuration","Chart of Accounts: NGCA | Valuation Grouping Code: 0001")
    y=130
    y=section_label(d,12,y,"Transaction / Event Keys — MM Account Determination")
    hcols=[(12,80,"Trans. Key"),(92,220,"Description"),(312,80,"Val. Class"),(392,160,"G/L Account"),(552,250,"Account Description"),(802,130,"Debit / Credit")]
    d.rectangle([12,y,W-12,y+24],fill=DARK_BLUE)
    for x,w,lbl in hcols:
        d.text((x+4,y+5),lbl,font=fnt(SANS_BOLD,10),fill=WHITE)
    y+=24
    rows=[
        ("BSX","Inventory Posting — Stock","3000","130500","Raw Material Stock","Debit / Credit"),
        ("WRX","GR/IR Clearing Account","—","210500","GR/IR Clearing Account","Debit / Credit"),
        ("GBB-VBR","GI — Internal Consumption","3000","500000","Material Consumption","Debit"),
        ("GBB-VNG","Scrapping","3000","600800","Inventory Scrapping Loss","Debit"),
        ("PRD","Price Difference","3000","600900","Price Differences","Debit / Credit"),
        ("KON","Consignment Payables","—","210600","Consignment Payable","Credit"),
    ]
    for ri,row in enumerate(rows):
        bg=LIGHT_BLUE if ri%2==0 else WHITE
        d.rectangle([12,y,W-12,y+22],fill=bg)
        for (x,w,_),val in zip(hcols,row):
            d.text((x+4,y+4),val,font=fnt(MONO if row.index(val)==0 or row.index(val)==2 else SANS,10),fill=BLACK)
        y+=22
    y+=16
    d.rectangle([20,y,W-20,y+26],fill=GRAY_BG,outline=BORDER,width=1)
    d.text((28,y+7),"Note: Account determination is triggered automatically during MM goods movements and invoice verification postings.",font=fnt(SANS,11),fill=GRAY_DARK)
    img.save(f"{OUT}/11_obyc_acctdet.png"); print("11_obyc done")

# ════════════════════════════════════════════════════════════════════════════
# 12. V/08 — PRICING PROCEDURE
# ════════════════════════════════════════════════════════════════════════════
def img_v08():
    img=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(img)
    sap_shell(d,img,"V/08","Pricing Procedure — NGPRC","NexGen Standard Pricing | Sales Org: SO01 | Dist Channel: DC01")
    y=130
    y=section_label(d,12,y,"Pricing Procedure: NGPRC — NexGen Standard Pricing Procedure")
    hcols=[(12,50,"Step"),(62,50,"Cntr"),(112,80,"Cond.Type"),(192,220,"Description"),(412,60,"From"),(472,60,"To"),(532,80,"Req."),(612,80,"AltCBV"),(692,80,"AltCTyp"),(772,100,"Acct Key"),(872,90,"Accruals")]
    d.rectangle([12,y,W-12,y+24],fill=DARK_BLUE)
    for x,w,lbl in hcols:
        d.text((x+4,y+5),lbl,font=fnt(SANS_BOLD,9),fill=WHITE)
    y+=24
    steps=[
        ("10","0","PR00","Basic / List Price","","","R","","","ERL",""),
        ("20","0","K007","Customer Discount %","10","","","","","ERS",""),
        ("30","0","","Net Value (sub-total)","10","20","","2","","",""),
        ("40","0","KF00","Freight Charges","","","","","","ERF",""),
        ("50","0","SKTO","Cash Discount","30","","","","","SKT",""),
        ("60","0","MWST","Output Tax GST 18%","30","","10","","","MWS",""),
        ("70","0","","Total Order Value","30","60","","","","",""),
    ]
    for ri,row in enumerate(steps):
        bg=LIGHT_BLUE if ri%2==0 else WHITE
        if row[2]=="": bg=(255,250,230)
        d.rectangle([12,y,W-12,y+20],fill=bg)
        for ci,((x,w,_),val) in enumerate(zip(hcols,row)):
            clr=SAP_BLUE if ci==2 and val else BLACK
            fon=MONO if ci==2 else SANS
            d.text((x+4,y+3),val,font=fnt(fon,10),fill=clr)
        y+=20
    img.save(f"{OUT}/12_v08_pricing.png"); print("12_v08 done")

# ════════════════════════════════════════════════════════════════════════════
# 13. F110 — AUTOMATIC PAYMENT PROGRAM
# ════════════════════════════════════════════════════════════════════════════
def img_f110():
    img=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(img)
    sap_shell(d,img,"F110","Automatic Payment Transactions: Parameters","Company Code: NGMS | Run Date: 19.04.2026")
    y=130
    # tabs
    for i,tab in enumerate(["Parameters","Free Selection","Additional Log","Printout/Data Medium","Status"]):
        bg=WHITE if i==0 else MENU_BG
        d.rectangle([12+i*180,y,12+i*180+176,y+22],fill=bg,outline=BORDER,width=1)
        d.text((18+i*180,y+5),tab,font=fnt(SANS,11),fill=DARK_BLUE if i==0 else GRAY_DARK)
    y+=30
    y=section_label(d,12,y,"Payment Run Parameters")
    y=field_row(d,20,y,"Run Date",          "19.04.2026",required=True)
    y=field_row(d,20,y,"Identification",    "NGMS_APR26",required=True)
    y+=10
    y=section_label(d,12,y,"Parameters")
    y=field_row(d,20,y,"Company Codes",     "NGMS",required=True)
    y=field_row(d,20,y,"Payment Methods",   "C  — Cheque  |  T  — Bank Transfer",required=True)
    y=field_row(d,20,y,"Next Payment Date", "30.04.2026",required=True)
    y=field_row(d,20,y,"Vendor (From/To)",  "VEND-001     to     VEND-999")
    y+=16
    # status box
    d.rectangle([20,y,W-20,y+80],fill=(240,255,240),outline=(0,140,70),width=1)
    d.text((30,y+8),"Payment Run Status:",font=fnt(SANS_BOLD,12),fill=GREEN)
    d.text((30,y+28),"Parameters have been entered",font=fnt(SANS,11),fill=GREEN)
    d.text((30,y+46),"Proposal run: 18.04.2026 / 14:32  —  Not yet started",font=fnt(SANS,11),fill=GRAY_DARK)
    d.text((30,y+62),"Payment run: Scheduled for 19.04.2026",font=fnt(SANS,11),fill=GRAY_DARK)
    y+=94
    for bx,lbl,bg in [(20,"Save Params",SAP_BLUE),(180,"Proposal",MID_BLUE),(340,"Payment Run",GREEN),(500,"Printout",GRAY_DARK)]:
        d.rectangle([bx,y,bx+140,y+26],fill=bg)
        d.text((bx+14,y+5),lbl,font=fnt(SANS_BOLD,12),fill=WHITE)
    img.save(f"{OUT}/13_f110_payment.png"); print("13_f110 done")

# ════════════════════════════════════════════════════════════════════════════
# 14. FBZP — PAYMENT PROGRAM CONFIG
# ════════════════════════════════════════════════════════════════════════════
def img_fbzp():
    img=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(img)
    sap_shell(d,img,"FBZP","Maintain Payment Program Configuration","Automatic Payment Transactions — Company Code NGMS")
    y=130
    # config buttons
    btns=["All Company Codes","Paying Company Codes","Payment Methods in Country","Payment Methods in Company Code","Bank Determination","House Banks"]
    bw=170; bh=36
    for i,btn in enumerate(btns):
        bx=12+(i%3)*(bw+12); by=y+(i//3)*(bh+10)
        active=i in (0,1,3)
        d.rectangle([bx,by,bx+bw,by+bh],fill=DARK_BLUE if active else MENU_BG,outline=BORDER,width=1)
        d.text((bx+8,by+10),btn,font=fnt(SANS,10),fill=WHITE if active else GRAY_DARK)
    y+=100
    y=section_label(d,12,y,"Paying Company Code — NGMS Configuration")
    y=field_row(d,20,y,"Paying Company Code","NGMS",required=True)
    y=field_row(d,20,y,"Separate Payment","—  (All company codes pay themselves)")
    y=field_row(d,20,y,"Min. Amount for Pmnt","100.00  INR")
    y=field_row(d,20,y,"Bill/Exch. Receivable","—")
    y+=10
    y=section_label(d,12,y,"House Bank Configuration — NGMS")
    hcols=[(12,100,"House Bank"),(112,120,"Bank ID"),(232,200,"Bank Name"),(432,120,"Account ID"),(552,200,"G/L Account"),(752,120,"Currency")]
    d.rectangle([12,y,W-12,y+22],fill=DARK_BLUE)
    for x,w,lbl in hcols:
        d.text((x+4,y+4),lbl,font=fnt(SANS_BOLD,10),fill=WHITE)
    y+=22
    for ri,(hb,bid,bname,aid,gl,ccy) in enumerate([
        ("SBI_HYD","SBI01","State Bank of India — Hyderabad","HYD_CURR","100010","INR"),
        ("HDFC_HYD","HDFC01","HDFC Bank — Hyderabad","HYD_CURR2","100011","INR"),
    ]):
        d.rectangle([12,y,W-12,y+20],fill=LIGHT_BLUE if ri%2==0 else WHITE)
        for (x,w,_),val in zip(hcols,[hb,bid,bname,aid,gl,ccy]):
            d.text((x+4,y+3),val,font=fnt(SANS,10),fill=BLACK)
        y+=20
    img.save(f"{OUT}/14_fbzp_config.png"); print("14_fbzp done")

# run all
img_logon()
img_ox02()
img_ox10()
img_fs00()
img_mm01()
img_me21n()
img_migo()
img_miro()
img_va01()
img_vf01()
img_obyc()
img_v08()
img_f110()
img_fbzp()
print("\nAll images generated in:", OUT)
