# SAP ERP Business Blueprint — NexGen Manufacturing Solutions Pvt. Ltd.

> **KIIT University | SAP Capstone Project | 2026**

## Project Overview

This repository contains the complete SAP ERP Business Blueprint for **NexGen Manufacturing Solutions Pvt. Ltd.** — a fictitious mid-sized manufacturing and trading company. The project covers end-to-end configuration and documentation for three SAP functional modules:

| Module | Coverage |
|--------|----------|
| **SAP FI** | Chart of Accounts, G/L, AP, AR, Asset Accounting, Controlling |
| **SAP MM** | Procurement, Material Master, Inventory, Account Determination |
| **SAP SD** | Sales Orders, Pricing, Delivery, Billing, Revenue Accounting |

---

## Company Details

| Field | Value |
|-------|-------|
| Company Name | NexGen Manufacturing Solutions Pvt. Ltd. |
| Company Code | NGMS |
| Client | 800 |
| HQ | Hyderabad, Telangana, India |
| Fiscal Year | April – March |
| Currency | INR |
| ERP | SAP S/4HANA 2023 |

---

## Repository Structure

```
NexGen_SAP_Blueprint/
├── README.md                          ← This file
├── docs/
│   ├── SAP_Blueprint_Report.docx      ← Full Word document blueprint
│   └── SAP_Blueprint_Documentation.pdf← 5-page submission PDF
├── screenshots/                        ← 14 generated SAP screenshots
│   ├── 01_logon.png
│   ├── 02_ox02_company_code.png
│   ├── 03_ox10_plant.png
│   ├── 04_fs00_gl.png
│   ├── 05_mm01_material.png
│   ├── 06_me21n_po.png
│   ├── 07_migo_gr.png
│   ├── 08_miro_invoice.png
│   ├── 09_va01_so.png
│   ├── 10_vf01_billing.png
│   ├── 11_obyc_acctdet.png
│   ├── 12_v08_pricing.png
│   ├── 13_f110_payment.png
│   └── 14_fbzp_config.png
├── config/
│   ├── organizational_structure.md    ← All SAP org units
│   ├── master_data.md                 ← G/L, Material, Vendor, Customer
│   └── tcodes_reference.md           ← Complete T-code list
└── scripts/
    ├── gen_sap_images.py              ← Generates all SAP screenshots
    ├── gen_blueprint_docx.js          ← Generates Word document
    └── gen_pdf_documentation.py       ← Generates PDF submission
```

---

## Modules Configured

### SAP FI — Financial Accounting
- **OB13** — Chart of Accounts NGCA (7 account classes, 100000–799999)
- **OB29** — Fiscal Year Variant FV01 (April–March, 4 special periods)
- **FS00** — G/L Accounts including Revenue (400000), Stock (130500), GR/IR (210500)
- **FBZP** — Automatic Payment Program with house banks SBI_HYD, HDFC_HYD
- **OBD3/OBD2** — Vendor & Customer Account Groups
- **OB45/FBMP** — Credit Control Area & Dunning Procedure

### SAP MM — Materials Management
- **OX10/OX08** — Plants HYD1, PUN1, CHE1 | Purchasing Org PO01
- **MM01** — Material Master: MAT-001 (ROH), MAT-002 (HAWA), MAT-003 (FERT), MAT-004 (VERP)
- **ME21N** — Purchase Orders with release strategy
- **MIGO** — Goods Receipt (Movement Type 101, 201, 261, 301)
- **MIRO** — Logistics Invoice Verification (GR-based)
- **OBYC** — Automatic Account Determination (BSX, WRX, GBB, PRD)

### SAP SD — Sales & Distribution
- **OVX5** — Sales Organization SO01 | 3 Distribution Channels | 3 Divisions
- **V/08** — Pricing Procedure NGPRC (PR00, K007, MWST 18%, KF00, SKTO)
- **VA01** — Standard Sales Order (Type OR)
- **VL01N/VL02N** — Outbound Delivery & Post Goods Issue
- **VF01** — Customer Invoice (Billing Type F2)
- **VKOA** — Revenue Account Determination

---

## End-to-End Business Scenarios

### Procure-to-Pay (P2P)
```
ME51N (PR) → ME41 (RFQ) → ME47 (Quotation) → ME49 (Compare)
→ ME21N (PO) → MIGO (GR, Mvt 101) → MIRO (Invoice) → F110 (Payment)
```

### Order-to-Cash (O2C)
```
VA21 (Quotation) → VA01 (Sales Order) → VL01N (Delivery)
→ VL02N (Post GI) → VF01 (Invoice) → F-28 (Payment)
```

### Record-to-Report (R2R)
```
MIGO/MIRO (Post transactions) → MR11 (Clear GR/IR)
→ AFAB (Depreciation) → KSV5 (Cost Allocation) → F.01 (Financial Statements)
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| ERP Platform | SAP S/4HANA 2023 |
| Database | SAP HANA 2.0 SP07 |
| Language | ABAP 7.5 |
| Config Tool | SPRO / IMG |
| UI | SAP GUI 8.0 |
| Doc Generation | Python (Pillow, ReportLab), Node.js (docx) |

---

## Student Details

| Field | Value |
|-------|-------|
| Name | Sudiksha Rao Rongla |
| Roll Number | 2306154 |
| Batch/Program | SAP Data Analytics — KIIT University |
| Submitted | April 2026 |

---

## License

This project is submitted for academic evaluation at KIIT University. All SAP content is for educational purposes only.
