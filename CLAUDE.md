# AIMS Knowledge Base — Claude Code Context

This project contains reference documentation, scripts, and sample files for
**Quadient AIMS (Automated Insertion Management System)** — a closed-loop mail
integrity platform used with Quadient folder inserters.

## What is AIMS?
AIMS validates every mailpiece in a production run against a pre-generated job
file (JAF), ensuring no piece is missed, duplicated, or mis-inserted. It
communicates in real time with IMOS (inserter firmware) during scanning.

## Key Docs (read these for context)
| File | Contents |
|------|----------|
| `docs/aims-overview.md` | System overview, license tiers, AIMS vs AIMS360 |
| `docs/aims-architecture.md` | End-to-end workflow, network design, file paths |
| `docs/aims-file-formats.md` | JAF, JCF, JRF field specs and layouts |
| `docs/aims-imos-communication.md` | Handshake protocol, machine registration, MongoDB |
| `docs/aims-integrations.md` | Automate/DocSecure setup, Power BI pipeline, OMS list |
| `docs/aims-troubleshooting.md` | Known issues and fixes |
| `docs/aims-mrdf-reference.md` | Industry MRDF vs Quadient JAF terminology mapping |

## Key Scripts
| File | Purpose |
|------|---------|
| `scripts/jcf_to_csv.py` | Watches FileDrop for .jcf files, parses fixed-width format, appends to CSV |
| `scripts/run_jcf_converter.bat` | Continuous watcher mode |
| `scripts/run_jcf_once.bat` | One-shot parse mode |

## Sample Files
| File | Description |
|------|-------------|
| `samples/sample.jcf` | Anonymized JCF for parser testing |
| `samples/sample.json` | Anonymized AIMS360 simulator JSON job file |

## Important Conventions
- **JobID**: always 10-character alphanumeric (e.g. `31CD77GGBW`)
- **MailPieceID**: always 10-digit numeric
- **FileDrop path (Classic AIMS)**: `C:\Program Files (x86)\AIMS\AIMS\FileDrop`
- **AIMS uses SQL Server; AIMS360 uses MongoDB** — they are different products
- Machine names in AIMS360 are **case-sensitive**
- Every registered machine needs BOTH `_Input` AND `_Output` channels
