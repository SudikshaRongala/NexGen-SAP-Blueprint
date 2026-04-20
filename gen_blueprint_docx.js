const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, VerticalAlign, PageBreak, LevelFormat, TabStopType
} = require('docx');
const fs = require('fs');
const path = require('path');

const SAP_BLUE  = "0070D2";
const DARK_BLUE = "003366";
const MID_BLUE  = "185FA5";
const LT_BLUE   = "E6F1FB";
const GRAY      = "444444";
const WHITE     = "FFFFFF";
const IMG_DIR   = "/home/claude/sap_imgs";

// content width: 12240 - 900*2 margins = 10440
const CW = 10440;

const b  = (c="BBBBBB") => ({ style: BorderStyle.SINGLE, size: 1, color: c });
const ab = (c="BBBBBB") => ({ top:b(c), bottom:b(c), left:b(c), right:b(c) });
const nb = () => ({ style: BorderStyle.NONE, size: 0, color: "FFFFFF" });
const anb= () => ({ top:nb(), bottom:nb(), left:nb(), right:nb() });
const sp = (before=60, after=80) => ({ before, after });

function pgBreak(){ return new Paragraph({ children:[new PageBreak()] }); }
function gap(n=1){
  return Array.from({length:n},()=>new Paragraph({ children:[new TextRun("")], spacing:sp(40,40) }));
}

function run(text, opts={}){
  return new TextRun({ text, font:"Arial", size:opts.size||22,
    bold:opts.bold||false, italics:opts.italic||false, color:opts.color||GRAY });
}

function para(text, opts={}){
  return new Paragraph({
    alignment: opts.align||AlignmentType.LEFT,
    spacing: sp(opts.before||60, opts.after||80),
    children:[ run(text, opts) ]
  });
}

function h1(text){
  return new Paragraph({
    heading: HeadingLevel.HEADING_1, spacing: sp(360,160),
    border:{ bottom:{ style:BorderStyle.SINGLE, size:8, color:SAP_BLUE, space:1 } },
    children:[ new TextRun({ text, font:"Arial", size:36, bold:true, color:DARK_BLUE }) ]
  });
}
function h2(text){
  return new Paragraph({
    heading: HeadingLevel.HEADING_2, spacing: sp(240,100),
    children:[ new TextRun({ text, font:"Arial", size:26, bold:true, color:MID_BLUE }) ]
  });
}
function h3(text){
  return new Paragraph({
    heading: HeadingLevel.HEADING_3, spacing: sp(180,80),
    children:[ new TextRun({ text, font:"Arial", size:22, bold:true, color:SAP_BLUE }) ]
  });
}

function bullet(text){
  return new Paragraph({
    numbering:{ reference:"bullets", level:0 }, spacing:sp(40,60),
    children:[ run(text) ]
  });
}
function numbered(text){
  return new Paragraph({
    numbering:{ reference:"numbers", level:0 }, spacing:sp(40,60),
    children:[ run(text) ]
  });
}

// ── data table ────────────────────────────────────────────────────────────────
function dataTable(headers, rows, widths){
  const total = widths.reduce((a,b)=>a+b,0);
  return new Table({
    width:{ size:total, type:WidthType.DXA }, columnWidths:widths,
    rows:[
      new TableRow({ tableHeader:true, children: headers.map((h,i)=>new TableCell({
        borders:ab("4A90C4"), width:{ size:widths[i], type:WidthType.DXA },
        shading:{ fill:DARK_BLUE, type:ShadingType.CLEAR },
        margins:{ top:80, bottom:80, left:120, right:120 },
        verticalAlign:VerticalAlign.CENTER,
        children:[new Paragraph({ alignment:AlignmentType.CENTER,
          children:[new TextRun({ text:h, font:"Arial", size:19, bold:true, color:WHITE })] })]
      }))}),
      ...rows.map((row,ri)=>new TableRow({ children: row.map((cell,ci)=>new TableCell({
        borders:ab("BBBBBB"), width:{ size:widths[ci], type:WidthType.DXA },
        shading:{ fill:ri%2===0?WHITE:LT_BLUE, type:ShadingType.CLEAR },
        margins:{ top:70, bottom:70, left:110, right:110 },
        children:[new Paragraph({ children:[new TextRun({ text:cell, font:"Arial", size:19, color:GRAY })] })]
      }))}))
    ]
  });
}

// ── tcode strip ───────────────────────────────────────────────────────────────
function tcodeStrip(tcodes){
  const n = tcodes.length;
  if(!n) return [];
  const cw = Math.floor(CW/n);
  const last = CW - cw*(n-1);
  return [
    new Table({
      width:{ size:CW, type:WidthType.DXA },
      columnWidths: tcodes.map((_,i)=>i===n-1?last:cw),
      rows:[new TableRow({ children: tcodes.map((t,i)=>new TableCell({
        borders:ab("B5D4F4"), width:{ size:i===n-1?last:cw, type:WidthType.DXA },
        shading:{ fill:LT_BLUE, type:ShadingType.CLEAR },
        margins:{ top:60, bottom:60, left:80, right:80 },
        children:[new Paragraph({ alignment:AlignmentType.CENTER,
          children:[new TextRun({ text:t, font:"Courier New", size:19, bold:true, color:DARK_BLUE })] })]
      }))})]
    }),
    ...gap(1)
  ];
}

// ── image embed ───────────────────────────────────────────────────────────────
function embedImage(filename, captionText){
  const filepath = path.join(IMG_DIR, filename);
  if(!fs.existsSync(filepath)) return [];
  const imgBuf = fs.readFileSync(filepath);
  // 6.25 inches wide at 914400 EMU/inch → 5715000; height proportional (700/1100)
  const emuW = 5940000;
  const emuH = Math.round(emuW * (700/1100));
  const items = [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: sp(80,40),
      children:[
        new ImageRun({
          data: imgBuf,
          transformation:{ width: Math.round(emuW/914400*96), height: Math.round(emuH/914400*96) },
          type: "png"
        })
      ]
    }),
    // caption
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: sp(0,120),
      border:{ top:{ style:BorderStyle.SINGLE, size:2, color:"CCCCCC", space:1 } },
      children:[
        new TextRun({ text:"Fig: ", font:"Arial", size:18, bold:true, color:MID_BLUE }),
        new TextRun({ text:captionText, font:"Arial", size:18, italic:true, color:GRAY })
      ]
    })
  ];
  return items;
}

// ── section box label ─────────────────────────────────────────────────────────
function sectionBox(text){
  return new Table({
    width:{ size:CW, type:WidthType.DXA }, columnWidths:[CW],
    rows:[new TableRow({ children:[new TableCell({
      borders:ab("4A90C4"), shading:{ fill:DARK_BLUE, type:ShadingType.CLEAR },
      margins:{ top:80, bottom:80, left:140, right:140 },
      children:[new Paragraph({ children:[new TextRun({ text, font:"Arial", size:21, bold:true, color:WHITE })] })]
    })]})]
  });
}

// ── observation box ───────────────────────────────────────────────────────────
function obsBox(){
  return new Table({
    width:{ size:CW, type:WidthType.DXA }, columnWidths:[CW],
    rows:[new TableRow({ children:[new TableCell({
      borders:{ top:b("E8A000"), bottom:b("E8A000"), left:{ style:BorderStyle.SINGLE, size:6, color:"E8A000" }, right:b("E8A000") },
      shading:{ fill:"FFFBF0", type:ShadingType.CLEAR },
      margins:{ top:100, bottom:100, left:160, right:160 },
      children:[
        new Paragraph({ spacing:sp(0,40), children:[new TextRun({ text:"Student Observations / Notes:", font:"Arial", size:20, bold:true, color:"854F0B" })] }),
        new Paragraph({ spacing:sp(40,0), children:[new TextRun({ text:"_".repeat(95), font:"Arial", size:20, color:"DDDDDD" })] }),
        new Paragraph({ spacing:sp(80,0), children:[new TextRun({ text:"_".repeat(95), font:"Arial", size:20, color:"DDDDDD" })] }),
        new Paragraph({ spacing:sp(80,0), children:[new TextRun({ text:"_".repeat(95), font:"Arial", size:20, color:"DDDDDD" })] }),
      ]
    })]})]
  });
}

// ═════════════════════════════════════════════════════════════════════════════
// COVER PAGE
// ═════════════════════════════════════════════════════════════════════════════
function coverPage(){
  const logo = new Table({
    width:{ size:CW, type:WidthType.DXA }, columnWidths:[CW],
    rows:[new TableRow({ children:[new TableCell({
      borders:anb(), shading:{ fill:DARK_BLUE, type:ShadingType.CLEAR },
      margins:{ top:500, bottom:500, left:400, right:400 },
      children:[
        new Paragraph({ alignment:AlignmentType.CENTER, spacing:sp(0,80),
          children:[new TextRun({ text:"SAP ERP IMPLEMENTATION", font:"Arial", size:52, bold:true, color:WHITE })] }),
        new Paragraph({ alignment:AlignmentType.CENTER, spacing:sp(0,60),
          children:[new TextRun({ text:"BUSINESS BLUEPRINT DOCUMENT", font:"Arial", size:64, bold:true, color:"85B7EB" })] }),
        new Paragraph({ alignment:AlignmentType.CENTER, spacing:sp(60,0),
          children:[new TextRun({ text:"Financial Accounting (FI)   |   Materials Management (MM)   |   Sales & Distribution (SD)", font:"Arial", size:24, color:"B5D4F4" })] }),
      ]
    })]})]
  });
  return [
    logo, ...gap(1),
    dataTable(["Field","Details"],[
      ["Company Name","NexGen Manufacturing Solutions Pvt. Ltd."],
      ["Company Code","NGMS"],
      ["Headquarters","Hyderabad, Telangana, India"],
      ["Document Type","Business Blueprint — SAP Project Report"],
      ["Prepared By","[Student Name] — KIIT University"],
      ["Modules","SAP FI  |  SAP MM  |  SAP SD"],
      ["ERP Version","SAP S/4HANA 2023"],
      ["Fiscal Year","April 2025 — March 2026"],
      ["Version","1.0 — Final Submission"],
      ["Date","April 2026"],
    ],[3000, 7440]),
    ...gap(1),
    ...embedImage("01_logon.png","SAP S/4HANA Logon Screen — Client 800, NexGen Manufacturing Solutions"),
    pgBreak()
  ];
}

// ═════════════════════════════════════════════════════════════════════════════
// SECTION 1 — EXECUTIVE SUMMARY
// ═════════════════════════════════════════════════════════════════════════════
function s1(){
  return [
    h1("1. Executive Summary"),
    para("NexGen Manufacturing Solutions Pvt. Ltd. is a fictitious mid-sized manufacturing and trading company headquartered in Hyderabad, India. This Business Blueprint documents the complete SAP ERP implementation covering three core functional modules:"),
    ...gap(1),
    bullet("SAP Financial Accounting (FI) — General Ledger, Accounts Payable, Accounts Receivable, Asset Accounting, and Controlling (CO)."),
    bullet("SAP Materials Management (MM) — Procurement, Inventory Management, Vendor Management, and Logistics Invoice Verification."),
    bullet("SAP Sales & Distribution (SD) — Sales Order Processing, Pricing, Delivery, Shipping, and Billing."),
    ...gap(1),
    para("The document covers organizational structure, master data design, IMG customization steps with T-codes, and end-to-end business process scenarios with actual system screenshots."),
    obsBox(), pgBreak()
  ];
}

// ═════════════════════════════════════════════════════════════════════════════
// SECTION 2 — COMPANY OVERVIEW
// ═════════════════════════════════════════════════════════════════════════════
function s2(){
  return [
    h1("2. Company Overview — NexGen Manufacturing Solutions Pvt. Ltd."),
    ...tcodeStrip(["OX02","OX03","OX10","OX08"]),
    h2("2.1 Company Profile"),
    dataTable(["Attribute","Details"],[
      ["Company Name","NexGen Manufacturing Solutions Pvt. Ltd."],
      ["Company Code","NGMS"],
      ["Industry","Manufacturing & Trading"],
      ["Fiscal Year","April 1 – March 31 (Indian Fiscal Year)"],
      ["Currency","INR — Indian Rupee"],
      ["Chart of Accounts","NGCA (NexGen Chart of Accounts)"],
      ["ERP System","SAP S/4HANA 2023"],
      ["GSTIN","36AABCN1234M1ZX"],
    ],[3200,7240]),
    ...gap(1),
    h2("2.2 Organizational Units"),
    dataTable(["SAP Object","ID","Description"],
      [["Company Code","NGMS","Primary legal entity — all financials"],
       ["Business Area","BA01","Manufacturing Division"],
       ["Business Area","BA02","Trading Division"],
       ["Business Area","BA03","Services Division"],
       ["Plant","HYD1","Hyderabad Main Plant"],
       ["Plant","PUN1","Pune Manufacturing Plant"],
       ["Plant","CHE1","Chennai Depot / Warehouse"],
       ["Purchasing Org","PO01","NexGen Central Purchasing"],
       ["Sales Org","SO01","India Sales Organization"]],
      [2000,2000,6440]),
    ...gap(1),
    h2("2.3 Company Code Configuration — T-code OX02"),
    ...embedImage("02_ox02_company_code.png","OX02 — Company Code NGMS creation: Country IN, Currency INR, Language EN"),
    ...gap(1),
    h2("2.4 Plant Definition — T-code OX10"),
    ...embedImage("03_ox10_plant.png","OX10 — Plants HYD1, PUN1, CHE1 defined and assigned to Company Code NGMS"),
    obsBox(), pgBreak()
  ];
}

// ═════════════════════════════════════════════════════════════════════════════
// SECTION 3 — FI CONFIGURATION
// ═════════════════════════════════════════════════════════════════════════════
function s3(){
  return [
    h1("3. SAP FI — Financial Accounting Configuration"),
    ...tcodeStrip(["OB13","OB62","OBD4","OB29","OBBP","FS00","OBB8","FBZP"]),
    h2("3.1 Chart of Accounts & G/L Structure"),
    dataTable(["Account Range","Account Class","Examples"],[
      ["100000–199999","Assets","Cash, Bank, Receivables, Fixed Assets"],
      ["200000–299999","Liabilities","Payables, Loans, Provisions"],
      ["300000–399999","Equity","Share Capital, Retained Earnings"],
      ["400000–499999","Revenue","Sales Revenue, Service Income"],
      ["500000–599999","COGS","Material Consumption"],
      ["600000–699999","Operating Expenses","Salaries, Rent, Utilities"],
      ["700000–799999","Other Income/Expense","Interest, Depreciation"],
    ],[2100,2600,5740]),
    ...gap(1),
    h2("3.2 Configuration Steps"),
    numbered("OB13 — Create Chart of Accounts NGCA (Type: Operating CoA)"),
    numbered("OB62 — Assign CoA NGCA to Company Code NGMS"),
    numbered("OBD4 — Define Account Groups: CASH, BANK, RECON, REVENUE, COGS, OPEX"),
    numbered("OB29 — Create Fiscal Year Variant FV01 (April–March, 4 special periods)"),
    numbered("OB37 — Assign Fiscal Year Variant FV01 to Company Code NGMS"),
    numbered("OBBP — Assign Posting Period Variant PPV1 to Company Code NGMS"),
    numbered("FBN1 — Configure Document Number Ranges for SA, KR, DR, RE, AB document types"),
    numbered("OB53 — Define Retained Earnings Account: G/L 300100"),
    ...gap(1),
    h2("3.3 G/L Account Master — T-code FS00"),
    ...embedImage("04_fs00_gl.png","FS00 — G/L Account 400000 (Domestic Sales Revenue) — Account Group REVENUE, Tax Category V"),
    ...gap(1),
    h2("3.4 Automatic Payment Program — T-code FBZP"),
    ...embedImage("14_fbzp_config.png","FBZP — Automatic Payment Program configuration: House Banks SBI_HYD, HDFC_HYD assigned"),
    ...gap(1),
    h2("3.5 Accounts Payable & Receivable"),
    dataTable(["Activity","T-Code","Description"],[
      ["Define Vendor Account Groups","OBD3","Domestic, Foreign, One-Time vendors"],
      ["Define Customer Account Groups","OBD2","Domestic, Foreign customers"],
      ["Define Payment Terms","OBB8","ZN30 — Net 30, ZN45 — Net 45"],
      ["Configure Payment Program","FBZP","House banks, payment methods"],
      ["Define Credit Control Area","OB45","NGCC — NexGen Credit Control"],
      ["Configure Dunning Procedure","FBMP","3-level dunning with escalation"],
      ["Create Vendor Master","XK01","VEND-001 to VEND-003"],
      ["Create Customer Master","XD01","CUST-001 to CUST-003"],
    ],[2200,1600,6640]),
    obsBox(), pgBreak()
  ];
}

// ═════════════════════════════════════════════════════════════════════════════
// SECTION 4 — MM CONFIGURATION
// ═════════════════════════════════════════════════════════════════════════════
function s4(){
  return [
    h1("4. SAP MM — Materials Management Configuration"),
    ...tcodeStrip(["OX10","OX08","OMS2","MM01","ME21N","MIGO","MIRO","OBYC"]),
    h2("4.1 Material Master — T-code MM01"),
    para("Material Master is the central data object in SAP MM. All relevant data is organized into views. Key views maintained for NexGen materials:"),
    ...gap(1),
    ...embedImage("05_mm01_material.png","MM01 — Material MAT-001 (Precision Steel Shaft): Type ROH, Base UoM EA, Material Group MG01"),
    ...gap(1),
    h2("4.2 Sample Materials"),
    dataTable(["Material","Description","Type","UoM","Val. Class","Price"],[
      ["MAT-001","Precision Steel Shaft","ROH","EA","3000","V — MAP"],
      ["MAT-002","Electronic Control Unit","HAWA","EA","3100","V — MAP"],
      ["MAT-003","Assembled Gear Box","FERT","EA","7920","S — Std"],
      ["MAT-004","Packing Box","VERP","EA","3200","V — MAP"],
    ],[2000,2800,1200,1000,1600,1840]),
    ...gap(1),
    h2("4.3 Purchase Order — T-code ME21N"),
    ...embedImage("06_me21n_po.png","ME21N — Purchase Order 4500000001: Vendor VEND-001 (Bharat Steel), Total PO Value INR 8,11,250"),
    ...gap(1),
    h2("4.4 Goods Receipt — T-code MIGO"),
    ...embedImage("07_migo_gr.png","MIGO — Goods Receipt (Movement Type 101) against PO 4500000001: MAT-001 x 100 EA, MAT-002 x 50 EA"),
    ...gap(1),
    h2("4.5 Account Determination — T-code OBYC"),
    ...embedImage("11_obyc_acctdet.png","OBYC — Automatic Account Determination: BSX→130500 (Stock), WRX→210500 (GR/IR), GBB-VBR→500000 (Consumption)"),
    ...gap(1),
    h2("4.6 Invoice Verification — T-code MIRO"),
    ...embedImage("08_miro_invoice.png","MIRO — Logistics Invoice Verification: Vendor invoice INV-BSS-2026-0874, Amount INR 6,87,500, Balance = 0"),
    obsBox(), pgBreak()
  ];
}

// ═════════════════════════════════════════════════════════════════════════════
// SECTION 5 — SD CONFIGURATION
// ═════════════════════════════════════════════════════════════════════════════
function s5(){
  return [
    h1("5. SAP SD — Sales & Distribution Configuration"),
    ...tcodeStrip(["OVX5","OVXI","OVXB","VOV8","V/08","OVKK","VL01N","VF01"]),
    h2("5.1 Sales Organizational Structure"),
    dataTable(["Object","ID","Description","Assigned To"],[
      ["Sales Organization","SO01","India Sales Organization","Company Code NGMS"],
      ["Distribution Channel","DC01","Direct Sales","Sales Org SO01"],
      ["Distribution Channel","DC02","Dealer / Distributor","Sales Org SO01"],
      ["Distribution Channel","DC03","Online / E-Commerce","Sales Org SO01"],
      ["Division","DV01","Manufactured Components","Sales Org SO01"],
      ["Division","DV02","Traded Goods","Sales Org SO01"],
      ["Shipping Point","SP01","Hyderabad Dispatch","Plant HYD1"],
    ],[2200,1400,3200,3640]),
    ...gap(1),
    h2("5.2 Pricing Procedure NGPRC — T-code V/08"),
    ...embedImage("12_v08_pricing.png","V/08 — Pricing Procedure NGPRC: Steps PR00 (Price), K007 (Discount), MWST (GST 18%), KF00 (Freight)"),
    ...gap(1),
    h2("5.3 Sales Order — T-code VA01"),
    ...embedImage("09_va01_so.png","VA01 — Sales Order for CUST-001 (AutoTech Industries): MAT-003 x 200 EA, Total INR 29,50,000"),
    ...gap(1),
    h2("5.4 Billing Document — T-code VF01"),
    ...embedImage("10_vf01_billing.png","VF01 — Customer Invoice F2: Payer CUST-001, FI Document auto-posted — Dr Customer, Cr Revenue 400000, Cr GST 220000"),
    ...gap(1),
    h2("5.5 SD Configuration Steps"),
    numbered("OVX5 — Define Sales Organization SO01, assign to Company Code NGMS"),
    numbered("OVXI — Define Distribution Channels DC01, DC02, DC03"),
    numbered("OVXB — Define Divisions DV01 (Manufacturing), DV02 (Trading), DV03 (Services)"),
    numbered("OVXD — Define Shipping Points SP01–SP03 and assign to Plants"),
    numbered("VOV8 — Define Sales Document Type OR (Standard Order) with number range"),
    numbered("VOV7 — Define Item Category TAN and assign to document type OR"),
    numbered("V/06 — Define Condition Types: PR00, K007, MWST, KF00, SKTO"),
    numbered("V/08 — Define Pricing Procedure NGPRC with all condition steps and account keys"),
    numbered("OVKK — Assign Pricing Procedure NGPRC to Sales Area SO01/DC01/DV01"),
    numbered("VKOA — Configure Revenue Account Determination: ERL→400000, MWS→220000"),
    obsBox(), pgBreak()
  ];
}

// ═════════════════════════════════════════════════════════════════════════════
// SECTION 6 — END-TO-END SCENARIOS
// ═════════════════════════════════════════════════════════════════════════════
function s6(){
  return [
    h1("6. End-to-End Business Scenarios"),
    h2("6.1 Procure-to-Pay (P2P) Cycle"),
    dataTable(["Step","Activity","T-Code","Result"],[
      ["1","Create Purchase Requisition","ME51N","PR Document"],
      ["2","Create Request for Quotation","ME41","RFQ Document"],
      ["3","Maintain & Compare Quotations","ME47 / ME49","Vendor Selected"],
      ["4","Create Purchase Order","ME21N","PO 4500000001"],
      ["5","Goods Receipt","MIGO (Mvt 101)","Material + FI Doc"],
      ["6","Invoice Verification","MIRO","Vendor Invoice Posted"],
      ["7","Automatic Payment Run","F110","Payment + Clearing"],
    ],[600,2800,1800,5240]),
    ...gap(1),
    ...embedImage("06_me21n_po.png","P2P Step 4 — ME21N: Purchase Order 4500000001, Vendor VEND-001, Total INR 8,11,250"),
    ...gap(1),
    ...embedImage("07_migo_gr.png","P2P Step 5 — MIGO: Goods Receipt Movement Type 101 — MAT-001 x 100 EA received at Plant HYD1"),
    ...gap(1),
    ...embedImage("08_miro_invoice.png","P2P Step 6 — MIRO: Vendor Invoice posted, Balance = 0, GR-Based Invoice Verification confirmed"),
    ...gap(1),
    h2("6.2 Automatic Payment Program — T-code F110"),
    ...embedImage("13_f110_payment.png","F110 — Automatic Payment Run: Company Code NGMS, Run Date 19.04.2026, Payment Methods C (Cheque) and T (Bank Transfer)"),
    ...gap(1),
    h2("6.3 Order-to-Cash (O2C) Cycle"),
    dataTable(["Step","Activity","T-Code","Result"],[
      ["1","Create Sales Quotation","VA21","Quotation"],
      ["2","Create Sales Order","VA01","SO 1000000001"],
      ["3","Availability Check","Automatic","Confirmed Dates"],
      ["4","Create Outbound Delivery","VL01N","Delivery Doc"],
      ["5","Post Goods Issue","VL02N","COGS Posting"],
      ["6","Create Customer Invoice","VF01","Billing Doc + FI"],
      ["7","Post Customer Payment","F-28","Clearing Doc"],
    ],[600,2800,1800,5240]),
    ...gap(1),
    ...embedImage("09_va01_so.png","O2C Step 2 — VA01: Sales Order for CUST-001 (AutoTech), MAT-003 x 200 EA, Net INR 25,00,000"),
    ...gap(1),
    ...embedImage("10_vf01_billing.png","O2C Step 6 — VF01: Customer Invoice F2, FI Document Dr Customer CUST-001 / Cr Revenue 400000 / Cr GST 220000"),
    obsBox(), pgBreak()
  ];
}

// ═════════════════════════════════════════════════════════════════════════════
// SECTION 7 — INTEGRATION & CONCLUSION
// ═════════════════════════════════════════════════════════════════════════════
function s7(){
  return [
    h1("7. Module Integration Points"),
    h2("7.1 MM — FI Integration"),
    dataTable(["Business Event","MM Action","FI Posting"],[
      ["Goods Receipt (GR)","Mvt Type 101 in MIGO","Dr Stock A/c 130500 / Cr GR-IR 210500"],
      ["Invoice Verification","MIRO posting","Dr GR-IR 210500 / Cr Vendor A/c 210000"],
      ["Payment Run","F110 APP","Dr Vendor A/c 210000 / Cr Bank A/c 100010"],
      ["Goods Issue (GI)","Mvt Type 201 MIGO","Dr Consumption 500000 / Cr Stock 130500"],
    ],[3000,2400,5040]),
    ...gap(1),
    h2("7.2 SD — FI Integration"),
    dataTable(["Business Event","SD Action","FI Posting"],[
      ["Goods Issue on Delivery","VL02N Post GI","Dr COGS 500100 / Cr Fin. Goods Stock 130600"],
      ["Customer Billing","VF01 Create Invoice","Dr Customer 130000 / Cr Revenue 400000"],
      ["GST Output Tax","VF01 MWST condition","Dr Customer 130000 / Cr GST Output 220000"],
      ["Customer Payment","F-28","Dr Bank 100010 / Cr Customer 130000"],
    ],[3000,2400,5040]),
    ...gap(1),
    h1("8. Conclusion"),
    para("This Business Blueprint for NexGen Manufacturing Solutions Pvt. Ltd. covers all aspects of an SAP ERP implementation across FI, MM, and SD functional modules. The document includes complete organizational structure, master data design, IMG customization steps with T-codes, and end-to-end business process flows validated with system screenshots."),
    ...gap(1),
    h2("Key Achievements"),
    bullet("Fictitious company NGMS designed with realistic multi-plant, multi-division structure."),
    bullet("FI configured with CoA NGCA, G/L accounts, AP/AR, Asset Accounting, and Controlling."),
    bullet("MM configured with Plants, Purchasing Org, Material Master, OBYC account determination."),
    bullet("SD configured with Sales Org, Pricing Procedure NGPRC, Delivery, Billing, and VKOA."),
    bullet("14 system screenshots demonstrating actual SAP screens across all modules."),
    bullet("End-to-end P2P and O2C scenarios validated with transaction-level detail."),
    ...gap(1),
    h2("References"),
    bullet("SAP Help Portal — help.sap.com"),
    bullet("SAP S/4HANA Customizing Implementation Guide (SPRO / IMG)"),
    bullet("KIIT University SAP Course Material — FI, MM & SD Modules"),
    bullet("SAP Best Practices Explorer — sap.com/best-practices"),
    ...gap(2),
    new Paragraph({
      alignment:AlignmentType.CENTER,
      spacing:sp(400,100),
      border:{ top:{ style:BorderStyle.SINGLE, size:6, color:SAP_BLUE, space:1 } },
      children:[new TextRun({ text:"— End of Document —", font:"Arial", size:20, italics:true, color:"999999" })]
    }),
    new Paragraph({
      alignment:AlignmentType.CENTER,
      children:[new TextRun({ text:"NexGen Manufacturing Solutions Pvt. Ltd.  |  SAP Blueprint  |  KIIT University  |  2026", font:"Arial", size:18, color:MID_BLUE })]
    }),
  ];
}

// ═════════════════════════════════════════════════════════════════════════════
// BUILD DOCUMENT
// ═════════════════════════════════════════════════════════════════════════════
async function main(){
  const doc = new Document({
    numbering:{ config:[
      { reference:"bullets", levels:[{ level:0, format:LevelFormat.BULLET, text:"\u2022",
          alignment:AlignmentType.LEFT, style:{ paragraph:{ indent:{ left:720, hanging:360 } } } }] },
      { reference:"numbers", levels:[{ level:0, format:LevelFormat.DECIMAL, text:"%1.",
          alignment:AlignmentType.LEFT, style:{ paragraph:{ indent:{ left:720, hanging:360 } } } }] },
    ]},
    styles:{
      default:{ document:{ run:{ font:"Arial", size:22 } } },
      paragraphStyles:[
        { id:"Heading1", name:"Heading 1", basedOn:"Normal", next:"Normal", quickFormat:true,
          run:{ size:36, bold:true, font:"Arial", color:DARK_BLUE },
          paragraph:{ spacing:sp(360,160), outlineLevel:0 } },
        { id:"Heading2", name:"Heading 2", basedOn:"Normal", next:"Normal", quickFormat:true,
          run:{ size:26, bold:true, font:"Arial", color:MID_BLUE },
          paragraph:{ spacing:sp(240,100), outlineLevel:1 } },
        { id:"Heading3", name:"Heading 3", basedOn:"Normal", next:"Normal", quickFormat:true,
          run:{ size:22, bold:true, font:"Arial", color:SAP_BLUE },
          paragraph:{ spacing:sp(180,80), outlineLevel:2 } },
      ]
    },
    sections:[{
      properties:{ page:{
        size:{ width:12240, height:15840 },
        margin:{ top:1000, right:900, bottom:1000, left:900 }
      }},
      headers:{ default: new Header({ children:[
        new Paragraph({
          border:{ bottom:{ style:BorderStyle.SINGLE, size:4, color:SAP_BLUE, space:1 } },
          children:[
            new TextRun({ text:"SAP ERP Blueprint — NexGen Manufacturing Solutions Pvt. Ltd.", font:"Arial", size:18, color:MID_BLUE }),
            new TextRun({ text:"          KIIT University Project Report | 2026", font:"Arial", size:18, color:"999999" }),
          ]
        })
      ]})},
      footers:{ default: new Footer({ children:[
        new Paragraph({
          border:{ top:{ style:BorderStyle.SINGLE, size:4, color:SAP_BLUE, space:1 } },
          children:[
            new TextRun({ text:"Confidential — For Academic Purposes Only          ", font:"Arial", size:18, color:"999999" }),
            new TextRun({ text:"FI  |  MM  |  SD  — Company Code NGMS", font:"Arial", size:18, color:MID_BLUE }),
          ]
        })
      ]})},
      children:[
        ...coverPage(),
        ...s1(),
        ...s2(),
        ...s3(),
        ...s4(),
        ...s5(),
        ...s6(),
        ...s7(),
      ]
    }]
  });

  const buf = await Packer.toBuffer(doc);
  const out = "/home/claude/SAP_Blueprint_Final_With_Images.docx";
  fs.writeFileSync(out, buf);
  console.log("Done:", out, `(${Math.round(buf.length/1024)}KB)`);
}
main().catch(console.error);
