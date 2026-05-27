# AIMS System Architecture

## End-to-End Workflow

The production flow moves through these stages in order:

1. **OMS generates a JAF** and drops it into the AIMS watched folder (FileDrop or jaf-input)
2. **AIMS validates** file structure, checks for duplicate JobIDs, and imports into its database
3. **Job runs** on a Quadient folder inserter controlled by IMOS firmware
4. **Inserter scans** each piece barcode and queries AIMS in real time
5. **AIMS validates**: is this piece in the JAF? Has it been processed already?
6. **AIMS generates** JCF (completion) and JRF (reprint) files at job end

---

## Network Design

AIMS uses a two-network design for performance and security:

| Network Segment | Purpose & Rules |
|-----------------|-----------------|
| **IMOS Network** (isolated VLAN) | Dedicated segment for inserter PCs. **No antivirus, no Windows Update, no security software, no group policies permitted.** Minimizes latency during live scanning. |
| **Main Network** | AIMS server, browser UI, SQL/MongoDB, OMS (Automate/Impress). Standard IT network rules apply. |

---

## Key File Paths

### Classic AIMS

| Path | Purpose |
|------|---------|
| `C:\Program Files (x86)\AIMS\AIMS\FileDrop` | Watched folder for JAF input and JCF output. Both file types share this folder. The JCF watcher filters by `.jcf` extension only — `.jaf` files are ignored. |

### DocSecure Adapter (used with Automate/Impress)

| Path | Purpose |
|------|---------|
| `C:\ProgramData\Quadient\Docsecure\DocsecureAdapter\jaf-input` | JAF input folder — Automate drops files here via AGG DS remote location setting |
| `C:\ProgramData\Quadient\Docsecure\DocsecureAdapter\export` | JCF and JRF output — **must be created manually if missing; AIMS will not auto-create it** |

---

## File Type Summary

| Extension | Name | Direction |
|-----------|------|-----------|
| `.jaf` | Job Allocation File | Input → AIMS |
| `.json` | JSON Job File (AIMS360 simulator) | Input → AIMS |
| `.jcf` | Job Complete File | Output ← AIMS |
| `.jrf` | Job Reprint File | Output ← AIMS |
