# AIMS Integrations

## Quadient Automate + DocSecure Integration

When Automate (Impress) is the OMS, AIMS hooks in via the **DocSecure Adapter**.

### Configuration Steps

**Step 1 — Automate: AGG DS Remote Location Settings**

- Enable **Use AIMS** checkbox
- Set **AIMS hot folder** → `C:\ProgramData\Quadient\Docsecure\DocsecureAdapter\jaf-input`
- Set **AIMS export hot folder** → `C:\ProgramData\Quadient\Docsecure\DocsecureAdapter\export`

**Step 2 — DocSecure Manager → General Settings → Files Settings**

- JAF File → `jaf-input` folder
- JCF File → `export` folder
- JRF File → `export` folder

**Step 3 — Verify Folder Structure**

```
C:\ProgramData\Quadient\Docsecure\DocsecureAdapter\
├── jaf-input\    ← JAF files placed here by Automate
└── export\       ← JCF and JRF output (CREATE MANUALLY if missing)
```

> ⚠️ The `export` folder must be created manually. AIMS will not auto-create it.
> If JCF/JRF files are not appearing, this is the first thing to check.

---

## Power BI Integration — JCF → CSV Pipeline

A Python script watches the FileDrop folder for new `.jcf` files, parses the
fixed-width format, and appends to a master CSV for Power BI refresh.

### Script: `scripts/jcf_to_csv.py`

**Default Configuration**

| Setting | Value |
|---------|-------|
| `WATCH_FOLDER` | `C:\Program Files (x86)\AIMS\AIMS\FileDrop` |
| `OUTPUT_CSV` | `.\output\aims_jobs.csv` |
| `PROCESSED_FOLDER` | `.\jcf_processed` |
| `ERROR_FOLDER` | `.\jcf_error` |
| `POLL_INTERVAL` | 10 seconds |

**Folder Structure (create alongside the script)**

```
jcf_input\        ← drop .jcf files here (or point to FileDrop)
output\           ← aims_jobs.csv lives here — point Power BI here
jcf_processed\    ← parsed JCFs moved here automatically
jcf_error\        ← failed JCFs moved here for inspection
jcf_converter.log ← parse log
```

**Running the Script**

```bat
:: Continuous mode — watches every 10 seconds
run_jcf_converter.bat

:: One-shot — process all .jcf files currently in folder
run_jcf_once.bat
```

**Power BI Setup**

1. Get Data → Text/CSV
2. Point at `output\aims_jobs.csv`
3. Each refresh re-reads the CSV with all newly appended JCFs

> ⚠️ The `customer_id` field may contain a hash/checksum value (`588e973a`)
> rather than a traditional ID. This varies by AIMS configuration and job type.
> Verify behavior with production JCF files before building reports on this field.

---

## OMS Integration v2.0 — Default Job Configuration (AIMS500)

This is the default job configuration profile for Impress Automate integration on a standard AIMS500 install. No customization is required — all settings align with Impress Automate defaults. The only site-specific value is the **file sharing location** (FileDrop path).

### Configuration Name
`OMS Integration v2.0`

### Active / Inactive Tabs

| Tab | Status | Notes |
|-----|--------|-------|
| Job Allocation File (JAF) | ✓ Active | v2.0 extended layout (250-char User Fields) |
| Job Reprint File (JRF) | ✓ Active | Same layout as JAF |
| Job Complete File (JCF) | ✓ Active | Same layout as JAF + Result header variants |
| JUF | ✗ Disabled | Suffix `.juf`; body fields partially defined but inactive |
| JPF | ✗ Disabled | Suffix `.jpf`; 60-second interval, Create Unique File mode |
| Job Settings | ✓ Active | Default settings |
| Scan Settings | ✗ Not configured | All positions set to 0 |
| Housekeeping Routines | ✗ Disabled | No auto-close or auto-delete timers |
| General Settings | ✓ Active | Default settings |
| DEP Settings | ✗ Disabled | Dynamic Envelope Printer not in use |
| Trigger File | ✗ Disabled | |
| Customer Portal Settings | ✓ Active | Points to FileDrop; exposes full JAF Header + Body fields |

### File Path (Site-Specific)

Default FileDrop path: `C:\Program Files (x86)\AIMS\AIMS\FileDrop`

This is the only value that may differ between installations. The Customer Portal Settings and any active file tabs reference this path.

### v2.0 vs Standard Format

The key difference between OMS Integration v2.0 and the standard AIMS v5.1 spec is the **User Field size**:

| Format | User Field 1–3 Length |
|--------|----------------------|
| Standard v5.1 | 50 characters |
| OMS Integration v2.0 | **250 characters** |

See `aims-file-formats.md` for the complete JAF/JCF field layout.

---

## OMS Compatibility

AIMS accepts JAFs from a variety of output management systems:

| OMS | Notes |
|-----|-------|
| Quadient Inspire | Native integration |
| Quadient Impress Automate | Via DocSecure Adapter (see above) |
| Ricoh ProcessDirector | Compatible |
| Pitney Bowes / BlueCrest / FP Mailing | Via AIMS-1000 external loop — bridges their MRDF format |

---

## Power Automate / Microsoft Stack Notes

> Quadient has authorized **Microsoft Copilot** as the AI model within its
> environment. External AI APIs (including direct Claude API calls) are not
> authorized for production use inside Quadient systems.

For automation within the Microsoft stack, use:

- **Power Automate** — flows for file watching, SharePoint updates, email triage
- **Copilot Studio** — for conversational/agent patterns within M365
- **Adaptive Cards in Teams** — for approval-based review workflows
- **Power Apps** — for form-based triggering when Power Automate inputs are insufficient

This knowledge base is maintained externally (Claude Code / Claude.ai) and used
to inform tooling built within authorized systems.
