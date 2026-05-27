# AIMS Technical Reference Guide (v7.12.2.0)

AIMS (Automated Insertion Management System) is a Quadient turnkey solution that extends the functionality of IMOS-driven Folder Inserters, enabling real-time management and analysis of insertion job runs. This reference guide consolidates the full technical whitepaper content—covering hardware specifications, network architecture, authentication methods, file formats, security configurations, and licensed features—into a single quick-reference document for use during implementation, troubleshooting, and support calls.

---

## System Overview

- **Current Version:** AIMS v7.12.2.0 (document date: April 7, 2025)
- **Delivery Model:** Turnkey solution — software pre-loaded and licensed on a supplied Dell PC
- **Core Components:** IMOS (Folder Inserter OS), SQL Express 2019, IIS (browser-based front-end), OMS interfaces
- **Default OS:** MS Windows 10 IoT Enterprise LTSC 2019 (v1809, Build 17763.1637, supported until Jan 2029)
- **Planned OS Upgrade:** MS Windows 10 LTSC 2021 21H2 (sometime in 2025); no current plans for Windows 11
- **Support Contact (2nd Level):** dlneoACCTechnicalSupport@quadient.com (DHSCC, Kennesaw, GA)

---

## Hardware Specifications

### Standard AIMS PC — Dell OptiPlex 7010 SFF

| Component | Specification |
|---|---|
| Processor | 13th Gen Intel Core i5-13500, 6+8 Cores, 2.5–4.9 GHz |
| RAM | 8 GB DDR4 3200 |
| Storage | 512 GB M.2 PCIe NVMe SSD |
| Security | TPM Enabled |
| Graphics | Intel Integrated (HDMI or DisplayPort) |
| Network | Two GB Ethernet Cards (Integrated + Additional) |
| OS | MS Windows 10 IoT Enterprise LTSC 2019 |
| Warranty | Next Business Day (NBD) from Dell |

### High-Volume Configuration (3+ DS1200s)

| Component | Specification |
|---|---|
| Processor | Intel Xeon 4.5 GHz Turbo, 6 Core |
| RAM | 16 GB RDIMM |
| Storage | 1 TB SSD x4 in RAID 10 |

### Kit Contents
- AIMS Dell PC (Standard or Extra)
- Touchscreen monitor
- Motorola barcode scanner
- NetGear 5-port Gigabit switch
- Assorted data cables

### Disaster Recovery
- **Cold Swap DR PC Part Number:** DSAIMSDRPC-ONLY
- DR PC is set up identically to live PC; AIMS backup merged at installation time
- Can be operated as a Hot Swap for continuous security update application

---

## Network Architecture

The AIMS DataStation PC has **two NICs**:

### NIC 1 — Folder Inserter Segment (Private/Dedicated LAN or Static VLAN)

| Parameter | Value |
|---|---|
| AIMS PC IP | 192.168.2.1 / 255.255.255.0 |
| First Inserter IMOS PC IP | 192.168.2.2 / 255.255.255.0 |
| Subsequent Machines | Increment numerically |
| Gateway | Not defined |
| Cross-talk to NIC 2 | Not configured |

### NIC 2 — Customer Domain/Network Segment
- LAN or VLAN; recommend DHCP reserved or static IP
- Used for OMS file exchange (JAF, JRF, JCF, JGF, JPF) and client browser access to AIMS

### Static VLAN Stipulations
- IMOS PCs **cannot** have AD user management, Security software, or Group Policies applied
- **No** Windows OS security or feature upgrades on IMOS PCs
- Switch management by customer IT is acceptable under these conditions

---

## Communication Ports

### IMOS ↔ AIMS (Internal Folder Inserter Segment)

| Port | Direction | Purpose |
|---|---|---|
| 2002 (TCP) | Inbound/Outbound | IMOS ↔ AIMS communication |
| 2003 (TCP) | Inbound/Outbound | Internal AIMS communication |
| 2004 (TCP) | Inbound/Outbound | Internal AIMS communication |
| 2005 (TCP) | Inbound/Outbound | AIMS Time Service |
| 2006 (TCP) | Inbound/Outbound | IMOS to AIMS Event Log Transfer |
| 2007 (TCP) | Inbound/Outbound | AIMS Internode Relay |

### AIMS ↔ Customer Domain

| Port | Direction | Purpose |
|---|---|---|
| 53 (TCP) | Inbound/Outbound | DNS |
| 80 (TCP) | Inbound/Outbound | HTTP — AIMS Client |
| 88 (TCP) | Inbound/Outbound | Kerberos (Windows Authentication) |
| 135–139 (TCP) | Inbound/Outbound | File Sharing with OMS |
| 443 (TCP) | Inbound/Outbound | SSL (if implemented) |
| 445 (TCP) | Inbound/Outbound | Windows Shares |
| 3389 (TCP/UDP) | Inbound/Outbound | Remote Desktop (optional) |
| 8200 (TCP/UDP) | Inbound/Outbound | Bomgar Remote Support |
| 13008 (TCP) | Inbound/Outbound | DEP Printer (if purchased) |

### Impress Automate Ports

| Port | Purpose |
|---|---|
| 515 (TCP) | LPD input |
| 690 (TCP) | Impress Automate server ↔ client |
| 443 (TCP) | HTTPS licensing |
| 9961, 9962, 3042 (TCP) | Inspire License Manager |
| 5150 (TCP) | NCOA Link |
| 9100 (TCP) | Raw print data |
| 49152–65535 (TCP) | Production engine communication |

---

## Closed Loop Workflow (Verification Mode)

1. **OMS** prints documents and creates a **JAF** (Job Allocation File); applies 2D DataMatrix barcode to every page (includes 10-digit JobID + 10-digit MailpieceID + machine controls)
2. **AIMS** monitors FileDrop folder (every 5 seconds), imports JAF into SQL database
3. **Folder Inserter** processes documents; real-time AIMS communication; successful handshake required to run
4. **Failed mailpieces** can optionally be Hand Mailed via supplied scanner (can be disabled for Touch & Toss)
5. **AIMS** generates **JRF** (Job Reprint File) for unresolved mailpieces when folder inserters disconnect
6. **AIMS** generates **JCF** (Job Complete File) upon job closure; job cannot close with unresolved mailpieces

### Supported OMS Systems (major products)
- Quadient Inspire (formerly GMC)
- impress automate (formerly OMS-500)
- Ricoh Process Director
- Ricoh Hybrid Mail (Planet Press)
- GenTax
- Solimar (Rubika)
- Planet Press (Objectif Lune)

### Supported Modes of Operation

| Mode | Supported Machines |
|---|---|
| Statistical Mode | Quadient IMOS-driven Folder Inserters only |
| Audit Mode | Quadient IMOS-driven Folder Inserters only |
| Verification Mode (Open or Closed Loop) | Quadient Office Level and IMOS-driven Folder Inserters |
| Lookup Mode (File Based) | Quadient IMOS-driven Folder Inserters only |

---

## File Formats & Folder Locations

### Default Folder Paths

| Purpose | Default Path |
|---|---|
| FileDrop (JAF input) | `C:\ProgramData\Quadient\AIMS\FileDrop` |
| Imported JAF files | `C:\ProgramData\Quadient\AIMS\FileDrop\Imported` |
| Failed JAF files | `C:\ProgramData\Quadient\AIMS\FileDrop\Error` |
| Export (JRF, JCF output) | `C:\ProgramData\Quadient\AIMS\FileDrop\Export` |
| Archive JCF (optional) | `C:\ProgramData\Quadient\FileDrop\ArchiveJCF` |
| Auto Reports (optional) | `C:\ProgramData\Quadient\FileDrop\Reports` |
| SQL Backup | `C:\ProgramData\Quadient\AIMS\Backup` |

> **Note:** All network paths must be in UNC format: `\\domain\computername\sharedfolder\resource`

### Required Permissions for AIMS Service Account (all file/backup/report locations)
- Full Control, Modify, Read & Execute, List, Read, Write

### JAF File — Key Structure (Verification Mode, OMS Config v1.5.1)

**Header Record:**

| Field | Start | Length | Notes |
|---|---|---|---|
| Header Marker | 1 | 1 | "H" |
| Job ID | 2 | 10 | A-Z a-z 0-9, preceding space |
| SLA Date/Time | 12 | 19 | YYYY-MM-DD hh:mm:ss |
| Creation Date/Time | 31 | 19 | YYYY-MM-DD hh:mm:ss |
| Job Name | 50 | 32 | A-Z a-z 0-9 space |
| IMOS Job Name | 82 | 20 | A-Z a-z 0-9 space |

**Body Record (key fields):**

| Field | Start | Length | Notes |
|---|---|---|---|
| Body Marker | 1 | 1 | "B" |
| Job ID | 2 | 10 | Mandatory |
| Mail Piece ID | 12 | 10 | Mandatory, unique within job |
| Customer ID | 22 | 32 | Optional |
| Total Prime Documents | 54 | 3 | Physical pages of address-bearing portion |
| Feeders 1–16 | 57–72 | 1 each | 1=Yes, 0=No |
| Full Name (DEP) | 85 | 50 | Optional |
| Address Lines 1–4 (DEP) | 185–335 | 50 each | Optional |
| Postal Code (DEP) | 385 | 50 | Optional |
| User Fields 1–3 | 435–535 | 50 each | Optional; may contain sensitive data |
| DEP fields | 1001–3325 | Various | Return address, IMB, image refs |

> **File naming:** `XXXXXXXXXX.jaf` (10-digit JobID). AIMS polls every 5 seconds. Recommended: write as `.jaf.processing` then rename to `.jaf` when complete.

### JRF (Job Reprint File) — Key Structure

**Body Record:**

| Field | Start | Length | Notes |
|---|---|---|---|
| Body Marker | 1 | 1 | "B" |
| Job ID | 2 | 10 | |
| Mail Piece ID | 12 | 10 | |
| Disposition Code | 22 | 2 | 00=Unread, 01=In Process, 10=Failed/Oversized/Voided |
| Timestamp | 24 | 19 | Date/Time processed or 19 spaces if unprocessed |
| Customer ID | 43 | 32 | |

### JCF (Job Complete File) — Key Disposition Codes

| Code | Description | Classification |
|---|---|---|
| 00 | Unread | Unresolved |
| 01 | In Process | Unresolved |
| 10 | Failed / Oversized / Voided | Unresolved |
| 20 | Diverted (Commanded or Late) | Diverted |
| 30 | Hand Mailed | Resolved |
| 40 | Inserted | Resolved |

> JCF is only produced once a job is **closed** in AIMS.

### File Naming Convention for Auto Reports
- Format: `JobDetail` or `JobSummary` + 10-digit JobID + GUID
- GUID prevents overwriting of files with same JobID

---

## User Authentication

Three methods selectable at install time via AIMS installer:

### 1. AIMS User Account Authentication (Default)
- Built-in; supports access from IMOS Folder Inserter browsers
- Admin assigns usernames, passwords, and access scope
- Password options: expiry days, minimum length, reuse block, capital/special character requirements
- Typically used when AIMS PC is not domain-joined

### 2. Active Directory Users (SSO)
- Requires AIMS PC joined to customer domain
- Admin enters `domain\username` in AIMS for each user
- Passwords managed via customer AD
- **Does NOT allow access from IMOS Folder Inserter browsers**

### 3. Active Directory Groups (SSO)
- Fully managed from customer AD environment
- Typically two groups: Admins and Operators
- **Important:** Admin users must also be members of the Operators group
- **Does NOT allow access from IMOS Folder Inserter browsers**

### AIMS User Permission Matrix

| Permission | Typical Role |
|---|---|
| Is Administrator | Administrator |
| Allow Reprint Job | Operator |
| Allow Complete Job | Administrator/Supervisor (Verification); Operator (Audit/Stats) |
| Allow Delete Job | Administrator/Supervisor |
| Allow Reset Job | Administrator/Supervisor |
| Allow Create Reports | Operator |
| Allow Mark Late Divert | Operator |
| Allow Mark Hand Mailed | Operator |
| Allow Mark Removed | Operator |
| Allow Mark Returned | Operator (requires Returned Mail license) |
| Allow Search | Operator (requires Search license) |
| Allow Login | All users |

> **Captcha** added to login in AIMS v7+ for additional security.

---

## AIMS Service Account

### Key Requirements
- Local account: acceptable if all file exchange is on the AIMS PC itself (default: Network Service)
- Domain account: **required** when file exchange, reporting, or backup uses a network drive
- Must be granted **"Log On as a Service"** rights in Local Security Policy
- Must be added to IIS Application Pool > Advanced Settings > Identity when using network paths for reports

### Services Using AIMS Service Account

| Service | TCP Port |
|---|---|
| QuadientIO | 2002 |
| QuadientEnterprise | 2003 |
| SQL Server (AIMS) | Default (Network Service unless changed) |

### SQL Roles Summary

| Database | Account | Role |
|---|---|---|
| IVSMain | AIMS Service Account | db_datareader |
| IVSMain | IIS Service Account | db_owner, db_datareader, db_datawriter |
| Neopost_AIMS | AIMS Service Account | db_owner, db_datareader, db_datawriter |
| Job Template | AIMS Service Account | db_owner, db_backupoperator, db_datareader, db_datawriter |

---

## SQL Configuration

- **Required Instance Name:** `AIMS` (hard requirement; cannot use external SQL cluster)
- **Default Version:** SQL Express 2019 (installed by AIMS installer v7+)
- **Optional:** SQL 2019 Standard (customer must supply license; instance name must still be `AIMS`)
- **PostgreSQL 14:** Installed by default with v7.12.2.0 — **recommend deselecting** during install (reserved for future PowerBI license in v8)
- **External links into AIMS SQL:** Not supported
- **SQL on separate cluster/farm:** Not supported — real-time communication requires SQL on local AIMS PC

### SQL Backup

| Backup Feature | Detail |
|---|---|
| Databases backed up | IVSMain, neopost__aims, active jobs, postgredb (if licensed) |
| Retention | 10 days (oldest folder deleted on day 11) |
| Incremental | Yes, compressed |
| Timing | Must run during non-production hours; all machines must show disconnected |