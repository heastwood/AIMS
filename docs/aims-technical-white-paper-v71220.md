# AIMS Technical White Paper v7.12.2.0 Reference Guide

This document is a structured reference of the AIMS Technical White Paper v7.12.2.0 (April 2025), authored by Rick DeJager. It is intended for use during AIMS implementation planning, IT security reviews, and support calls.

---

## Summary

AIMS (Automated Insertion Management System) extends the functionality of IMOS-driven Folder Inserters, enabling real-time management and analysis of insertion job runs. It is delivered as a turnkey solution on a Quadient-supplied Dell PC and integrates with Output Management Systems (OMS) via file exchange. This reference covers planning, networking, authentication, file formats, security, SQL, remote support, licensed features, and FAQs.

---

## 1. Project Planning Process

- The AIMS Technical White Paper guides customer IT Admin and Project Managers through IT requirements.
- Used as a reference for completing the **AIMS Site Survey**, which captures customer preferences.
- Site Survey drives the **AIMS Implementation Plan (SOW)** including who, what, where, and when.

---

## 2. What is AIMS?

- Extends IMOS (Intelligent Mail Operating System) Folder Inserters (Professional, Production, and Office level).
- Current version: **AIMS v7.12.2.0**
- Delivered as a **Turnkey Solution** — software pre-loaded on a Quadient-supplied Dell PC.

### Standard Kit Includes

| Component | Details |
|-----------|---------|
| AIMS Dell PC (Standard) | Dell OptiPlex 7010 SFF, Intel Core i5-13500, 8GB DDR4, 512GB NVMe SSD, TPM, dual GbE NICs |
| OS | MS Windows 10 IoT Enterprise LTSC 2019 (v1809, Build 17763.1637) — supported until Jan 2029 |
| Monitor | Touchscreen |
| Scanner | Motorola barcode scanner |
| Switch | NetGear 5-port Gigabit switch |
| Cables | Assorted data cables |

> **Note:** QTL plans to upgrade to MS Win 10 LTSC 2021 21H2 in 2025. No current plans for Windows 11.

### AIMS Components

- **IMOS** — runs the Folder Inserter
- **SQL Express 2019** — AIMS databases (IVSMain, neopost__aims, per-job DBs)
- **IIS** — browser-based client front-end
- **OMS interfaces** — for JAF/JRF/JCF file exchange
- **PostgreSQL 14** — installed by default in v7.12.2.0 but should be **deselected** unless PowerBI AIMS license is purchased (v8 feature)

---

## 3. Network Configuration

### Dual NIC Setup

The AIMS DataStation PC uses **two Network Interface Cards**:

| NIC | Purpose | Details |
|-----|---------|---------|
| NIC 1 | Folder Inserter segment | Private dedicated LAN or Static VLAN; static IPs, no gateway |
| NIC 2 | Customer domain/network | DHCP reserved or static IP; file exchange with OMS and browser access |

> Cross-talk between the two NICs is **NOT** set up.

### IP Addressing (Folder Inserter Segment)

| Device | IP Address |
|--------|-----------|
| AIMS PC | 192.168.2.1 / 255.255.255.0 |
| First IMOS PC | 192.168.2.2 / 255.255.255.0 |
| Additional machines | Increment numerically |

### File Exchange via OMS Connection

| File | Description |
|------|-------------|
| JAF | Job Allocation File — checklist for mail run (Verification Mode) |
| JRF | Job Reprint File |
| JCF | Job Complete File |
| JGF | Job Good Envelopes File (optional/custom) |
| JPF | Job Progress File (optional/custom) |

---

## 4. AIMS Closed Loop Workflow (Verification Mode)

1. **OMS prints** documents and creates JAF file with 2D DataMatrix barcodes (10-digit JobID + 10-digit MailpieceID).
2. **AIMS imports JAF** — checks structure/format/duplicate JobID, imports into SQL database.
3. **Documents run on Folder Inserter** — real-time barcode reading and integrity checking. Handshake required.
4. **Failed mailpieces** — can optionally be Hand Mailed using the AIMS scanner. Can be disabled for Touch n Toss.
5. **JRF generated** — AIMS requests reprints from OMS for unresolved mailpieces.
6. **JCF generated** — AIMS informs OMS job is closed once all mailpieces are resolved.

> See Appendix 3 for JAF, JRF, JCF file format details.

---

## 5. User Authentication

Three authentication methods are available, selected during AIMS installer setup:

### Method 1: AIMS User Account Authentication (Default)

- Built into AIMS software.
- Supports access from IMOS Folder Inserter browsers.
- Username/password assigned by AIMS administrator.
- Password policies: Days to Expiry, Minimum Length, Reuse Block, Capital Letter, Special Character.
- Access roles include: Administrator, Allow Reprint Job, Allow Complete Job, Allow Delete Job, Allow Reset Job, Allow Create Reports, Allow Mark Late Divert, Allow Mark Hand Mailed, Allow Mark Removed, Allow Mark Returned, Allow Search, Allow Login.

### Method 2: AD Users Authentication (SSO)

- Requires AIMS PC to be joined to the customer domain.
- AIMS administrator adds domain\username for each user.
- Passwords managed by Active Directory.
- SSO login after domain logon.
- **Does NOT allow access from IMOS Folder Inserter browsers.**

### Method 3: AD Groups Authentication (SSO)

- Fully managed from customer AD environment.
- Customer IT creates AD groups (typically Admin and Operators).
- **Important:** Admin users must also be members of the Operators group.
- SSO login after domain logon.
- **Does NOT allow access from IMOS Folder Inserter browsers.**

---

## 6. Captcha Security

- Added in AIMS v7 — provides an additional layer of login security.
- Restricts penetration attempts on the login screen.

---

## 7. AIMS Service Account

| Item | Detail |
|------|--------|
| Account type | Local or domain account |
| Domain account required when | File exchange, auto reporting, or backup is on a network drive |
| Default local account | Network Service |
| Local Security Policy | Must be added with "Logon as a Service" rights |
| Services controlled | QuadientIO (port 2002), QuadientEnterprise (port 2003) |
| SQL Server (AIMS) service | Optionally set to service account; defaults to Network Service |
| Password expiry | Can be expiring or non-expiring; customer IT manages changes via AIMS installer |

### Required Folder Permissions

Full Control, Modify, Read & Execute, List, Read, Write — required for:
- FileDrop folder
- Export folder
- Backup folder
- Auto Report folder
- Archive JCF folder

---

## 8. Sensitive Data & Housekeeping

- AIMS does not require sensitive HI or PCI data in the JAF.
- OMS creates non-sensitive 10-digit JobID and 10-digit MailpieceID.
- Optional JAF fields: Recipient Name, Address, Customer ID, 3 User Defined Fields (50 chars each).

### Housekeeping Settings (OMS Configuration)

| Setting | Description |
|---------|-------------|
| Auto Close Processed Job | Closes jobs where all pieces are read but some unresolved |
| Auto Close Finished Job | Closes fully resolved jobs — typically 5–15 minutes |
| Auto Close Open Job | Closes unclosed jobs with some processing |
| Auto Delete Unused Job | Deletes JAF-imported jobs never run on inserter |
| Auto Delete Closed Job | Typically 480 minutes (8 hours) — removes job DB and sensitive data |

> Extending Auto Delete Closed Job timing supports Search & Returned Mail licenses.

---

## 9. FileDrop & Export Folders

| Path | Purpose |
|------|---------|
| `C:\ProgramData\Quadient\AIMS\FileDrop` | OMS drops JAF files here |
| `C:\ProgramData\Quadient\AIMS\FileDrop\Imported` | Successfully imported JAF files moved here |
| `C:\ProgramData\Quadient\AIMS\FileDrop\Error` | Failed JAF files moved here with `.err` file |
| `C:\ProgramData\Quadient\AIMS\FileDrop\Export` | AIMS drops JRF and JCF files here |

- Network paths must be in UNC format: `\\domain\computername\sharedfolder\resource`
- AIMS Service Account requires Full Control on all shared folder locations.

---

## 10. Archive JCF File (Optional)

- Creates a copy of the JCF for audit/historical purposes.
- Suggested default local path: `C:\ProgramData\Quadient\FileDrop\ArchiveJCF`
- Network paths must be UNC format.
- AIMS Service Account requires Full Control.

---

## 11. Auto Report Creation (Optional)

Reports created automatically when a job is closed:

| Report Type | Output |
|-------------|--------|
| Job Summary (Status, Postal, Activity) | PDF |
| Job Summary | CSV |
| Job Detail | PDF only |

- Reports are hard-coded — not customizable.
- Suggested local path: `C:\ProgramData\Quadient\FileDrop\Reports`
- For network paths: AIMS Service Account must also be added to IIS > Application Pool > Advanced Settings > Identity.
- Filename format: `JobDetail` or `JobSummary` + 10-digit JobID + GUID

---

## 12. AIMS SQL Backup

- Automated utility within AIMS software.
- **Databases backed up:** IVSMain, neopost__aims, active jobs, postgredb (if BI licensed).
- Backups are **incremental and compressed**.
- **Retention:** 10 days (oldest folder deleted on day 11).
- Backup structure: dated folder (main DBs + active jobs), Stale folder, Closed folder.
- Backups run during **non-production hours** — all machines must show disconnected.
- Default path: `C:\ProgramData\Quadient\AIMS\Backup`
- Customer is responsible for backing up AIMS backup files per Quadient T&Cs.

---

## 13. IT Security Options

### Anti-Virus / Anti-Malware

- Windows Defender AV installed on Quadient turnkey PC.
- Customer AV may be installed — can slow job processing.
- Request: **Turn off Live File Checking Mode**.

**Folder exclusions required:**
- `C:\ProgramData\Quadient\AIMS`
- `C:\Program Files\Windows Defender`
- `C:\Program Files (x86)\Windows Defender`

**Process exclusions required:**
- `C:\Program Files (x86)\AIMS\Services\QuadientIO.exe`
- `C:\Program Files (x86)\AIMS\Services\Enterprise\Quadiententerprise.exe`
- `MsMpEng.exe`

**Windows Task Scheduler:** AV scans must be set to non-production hours.

### HDD Encryption

- Dell PC is TPM compliant.
- **MS Bitlocker** is certified to work with AIMS.
- Other encryption software may be used — subject to test.

### IIS Encryption

- IIS can be encrypted with a customer-supplied SSL certificate.
- Certificate must be trusted by all user workstation browsers.

### Customer OS Image

Supported OS versions:

| OS | Version | Build | Support End |
|----|---------|-------|------------|
| MS Windows 10 IoT Enterprise LTSC 2019 | V1809 | 17763.1637 | 2029-01-09 |
| MS Windows 10 Enterprise LTSC | V21H2 | 19044.1566 | 2032-01-13 (IoT only) |

- Most Windows 10 Pro/Enterprise versions likely work (subject to test).
- Re-imaging requires Quadient to reinstall prerequisites, AIMS software, and licensing.
- Typically completed in one remote session of 2–3 hours.

### Virtual Server Requirements

| Spec | Requirement |
|------|-------------|
| OS | MS Windows Server 2022 Datacenter 64-bit or later |
| Processor | 4 vCPUs, 2.3 GHz Intel Broadwell E5-2686v4 or above (Hyper-V or VMware) |
| RAM | 16 GB or above |
| Storage | 500 GB local |
| NICs | 2 ports (Intel Pro/1000 GT or equivalent) |
| SQL | Instance Name must be "AIMS"; SQL Express 2019 or Standard |

- AIMS VE implementations managed by DHSCC staff only via remote support.
- VE must be **dedicated to AIMS** (hardware can be shared but resources must be dedicated).
- Recommend within LAN — not WAN — due to real-time communication requirements.
- Only AIMS v7 and above can be used on a Virtual Server.

---

## 14. Firewall / Required Ports

### IMOS PC Ports

| Port | Direction | Reason |
|------|-----------|--------|
| 2002 (TCP) | Inbound/Outbound | IMOS ↔ AIMS communication |

### AIMS DataStation Ports

| Port | Direction | Reason |
|------|-----------|--------|
| 2002 (TCP) | Inbound/Outbound | IMOS ↔ AIMS communication |
| 2003 (TCP) | Inbound/Outbound | Internal AIMS communication |
| 2004 (TCP) | Inbound/Outbound | Internal AIMS communication |
| 2005 (TCP) | Inbound/Outbound | AIMS Time Service |
| 2006 (TCP) | Inbound/Outbound | IMOS to AIMS Event Log Transfer |
| 2007 (TCP) | Inbound/Outbound | AIMS Internode Relay |

### Customer Domain / Client Access Ports

| Port | Direction | Reason |
|------|-----------|--------|
| 53 (TCP) | Inbound/Outbound | DNS |
| 80 (TCP) | Inbound/Outbound | HTTP for AIMS Client |
| 88 (TCP) | Inbound/Outbound | Kerberos (Windows Auth) |
| 135–139 (TCP) | Inbound/Outbound | File Sharing with OMS |
| 443 (TCP) | Inbound/Outbound | SSL (if implemented) |
| 445 (TCP) | Inbound/Outbound | Windows Shares |
| 3389 (TCP/UDP) | Inbound/Outbound | Remote Desktop (Optional) |
| 8200 (TCP/UDP) | Inbound/Outbound | Bomgar Remote Desktop |
| 13008 (TCP) | Inbound/Outbound | DEP Printer (if purchased) |

### Impress Automate Ports

| Port | Direction | Reason |
|------|-----------|--------|
| 690 (TCP) | Inbound/Outbound | Impress Automate server ↔ client |
| 515 (TCP) | Inbound/Outbound | LPD input (if used) |
| 443 (TCP) | Inbound/Outbound | Licensing server / HTTPS |
| 9961, 9962, 3042 (TCP) | Inbound/Outbound | Inspire License Manager |
| 5150 (TCP) | Inbound/Outbound | NCOA Link |
| 9100 (TCP) | Inbound/Outbound | Raw print data to server |
| 49152–65535 (any) | Inbound/Outbound | Production engine communication |

---

## 15. Remote Support

- Quadient USA uses **Bomgar** (clientless, attended) for remote support.
- Bomgar is HIPAA and PCI compliant.
- Ports **80, 443, and 8200** must be open for outbound TCP.
- Port 8200 is recommended as a rollover for port 443.
- Internet security software must not block Bomgar executables.
- Customer can provide alternative remote support tool if required.

---

## 16. Frequently Asked Questions

| Question | Answer |
|----------|--------|
| Does AIMS support SSO? | Yes — AD Users or AD Groups |
| Does AIMS support MFA (native)? | No |
| Does AIMS support GMSA? | No |
| Can SQL be on an Enterprise Cluster? | No — SQL must run directly on the AIMS PC |
| Must the SQL version be 2019 Express? | No — SQL 2019 Standard is also supported (customer must supply license) |
| Can AIMS run without IIS? | No |
| Can the private inserter segment be on a Static VLAN? | Yes — with stipulations (no AD/AV/GPO on IMOS PCs, no OS upgrades) |
| Can OS security updates be applied to the AIMS PC? | Yes — managed by customer IT/SCCM/MECM |
| Does AIMS support FTP/SFTP? | No — Windows Shares only; all paths in UNC format |
| Can AIMS run on a Virtual Server? | Yes — Windows Server 2022 Datacenter tested |
| How often is AIMS software updated? | Typically twice per year (minor bug fixes and feature updates) |
| Does Verification Mode support Touch & Toss? | Yes — Hand Mail can be disabled |

### Supported OMS Products (Verification Mode)

- Quadient Inspire (formerly GMC)
- Impress Automate (formerly OMS-500)
- Ricoh Process Director
- Ricoh Hybrid Mail (Planet Press)
- GenTax
- Solimar (Rubika)
- Planet Press (Objectif Lune)

### Supported Mail Production Management Systems

- Kern Mailfactory (Audit KIC Files)
- MRDF (Mail Run Data Files)

### Supported Modes of Operation

| Mode | Machines |
|------|----------|
| Statistical Mode | Quadient IMOS-driven Folder Inserters only |
| Audit Mode | Quadient IMOS-driven Folder Inserters only |
| Verification Mode (Closed/Open Loop) | Quadient Office Level and IMOS-driven Folder Inserters |
| Lookup Mode (File Based) | Quadient IMOS-driven Folder Inserters only |

### Disaster Recovery

- **Quadient Dell PC:** Dell NBD warranty; local service team reinstalls AIMS and restores backup.
- **Cold Swap DR PC:** Part number `DSAIMSDRPC-ONLY` — setup identically to live AIMS PC.
- Can be operated as a Hot Swap for continuous security updates.

### AIMS Support Contact

- **1st Level:** Local service team
- **2nd Level:** DHSCC — dlneoACCTechnicalSupport@quadient.com (Kennesaw, GA)

---

## 17. JAF / JRF / JCF File Formats (Verification Mode)

All files are **UTF-8 Fixed Field Formatted Text Files**.

### JAF (Job Allocation File) — Produced by OMS

- Filename: `{10-digit JobID}.jaf` (e.g., `66F4C71400.jaf`)
- AIMS monitors FileDrop folder every 5 seconds.
- OMS should write file as `.jaf.processing` then rename to `.jaf` when complete.
- Header record (H) + Body records (B) — one line per mailpiece.

**Header record fields (OMS Config v1.5.1):**

| Field | Start | Length | Notes |
|-------|-------|--------|-------|
| Header Marker | 1 | 1 | "H" |
| Job Id | 2 | 10 | Mandatory |
| SLA Date/Time | 12 | 19 | YYYY-MM-DD hh:mm:ss |
| Creation Date/Time | 31 | 19 | YYYY-MM-DD hh:mm:ss |
| Job Name | 50 | 32 | |
| IMOS Job Name | 82 | 20 | |

**Key body record fields:**

| Field | Start | Length | Notes |
|-------|-------|--------|-------|
| Body Marker | 1 | 1 | "B" |
| Job Id | 2 | 10 | Mandatory |
| Mail Piece Id | 12 | 10 | Mandatory |
| Customer Id | 22 | 32 | Optional |
| Total Prime Documents | 54 | 3 | Page count of address-bearing part |
| Feeder 1–16 Count | 57–72 | 1 each | 1=Yes, 0=No |
| Full Name / DEP Full Name | 85 | 50 | Optional |
| Address Lines 1–4 | 185–335 | 50 each | Optional |
| Postal Code | 385 | 50 | Optional |
| User Field 1–3 | 435–535 | 50 each | Optional |
| DEP fields | 1001+ | Various | For Dynamic Envelope Printing |

### JRF (Job Reprint File) — Produced by AIMS

- Filename: `{10-digit JobID}.jrf`
- Written as `.jrf.processing` then renamed when complete.
- Contains only mailpieces requiring reprint.

**Disposition Codes (Unresolved):**

| Code | Description |
|------|-------------|
| 00 | Unread |
| 01 | In Process |
| 10 | Failed, Oversized, Voided |

### JCF (Job Complete File) — Produced by AIMS

- Filename: `{10-digit JobID}.jcf`
- Produced only once a job is closed — contains all mailpieces.
- Written as `.jcf.processing` then renamed when complete.

**Disposition Codes (Resolved):**

| Code | Description |
|------|-------------|
| 20 | Diverted (Commanded, Late) |
| 30 | Hand Mailed |
| 40 | Inserted |

---

## 18. AIMS Services & Permissions (Appendix 1)

### Default Accounts

| Service | Default Account |
|---------|----------------|
| IIS Service Account | NT AUTHORITY\NETWORK SERVICE |
| AIMS Service Account | NT AUTHORITY\NETWORK SERVICE |
| SQL Server Service Account | NT AUTHORITY\NETWORK SERVICE |

### SQL Server Roles

| Database | User | Role |
|----------|------|------|
| IVSMain | AimsServices (AIMS SA) | db_datareader |
| IVSMain | AimsWeb (IIS SA) | db_owner, db_datareader, db_datawriter |
| Neopost_AIMS | AimsServices | db_datareader, db_datawriter, db_owner |
| Neopost_AIMS | AimsWeb | db_datareader, db_datawriter |

- All accounts running services require **"Log On As A Service"** rights.
- Subdirectories inherit permissions.
- Files must be **created** or **copied** (not moved/cut) into directories to inherit correct permissions.

---

## 19. Licensed Features (Appendix 10)

| Feature | Description |
|---------|-------------|
| Search | Find mailpieces across open jobs (up to 1000 results) |
| Late Divert File Import | OMS supplies .ldf file to flag mailpieces for late divert |
| Partially Processed File Import | Import JAF files already partly processed by another system |
| Sub Job Reporting | Track document types within merged jobs using User Field 1–3 |
| Bulk By Hand | Mass update mailpieces to Hand Mailed, Voided, or Returned |
| Returned Mail | Record and report mailpieces returned from postal stream |
| Multi-Job Support | Run multiple jobs consecutively without stopping inserter |
| Multi-Site Support | Not currently recommended — enhanced version coming |

---

## 20. AIMS On-Board vs AIMS-500

| Feature | AIMS On-Board | AIMS-500 |
|---------|--------------|----------|
| Installation | Installed on IMOS PC (Lite version) | Separate DataStation PC |
| Availability | DS180i, DS200i, DS600i, G4i only | All supported inserters |
| Modes | Statistics only (no Audit out of box) | Statistics, Audit, Verification, Lookup |
| External access | NOT possible — IMOS PC must not connect to network | Yes — via customer domain NIC |
| Multi-machine | No — isolated per machine | Yes |
| Auto Reporting paths | Locked (cannot edit) | Configurable |
| Housekeeping | Locked (cannot edit) | Configurable |

---

## 21. Operating System Reference (Appendix 11)

| Component | Current OS | Support End |
|-----------|-----------|------------|
| AIMS DataStation PC | MS Win 10 IoT Enterprise LTSC 2019 | Jan 2029 |
| IMOS PC (DS180i, DS700iQ, DS1200G4i) | MS Win 10 IoT Enterprise LTSC 2019 | Jan 2029 |
| FlexMail (DEP) | MS Win 10 Professional (transitioning to LTSC 2021) | Oct 2025 (Pro) |

> **Note:** Quadient does not allow customers to re-image IMOS or FlexMail PCs, nor provide their own hardware for those components. Windows 11 LTSC 2024 was released September 2024; Quadient has no current timeline to adopt it.

---

*Document Version 7.12.2.0 — April 7, 2025 | © 2025 Quadient, Inc.*
*Proprietary and confidential — not for reproduction without written consent.*
