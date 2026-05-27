# AIMS Knowledge Base

Reference documentation and tools for **Quadient AIMS (Automated Insertion
Management System)** — a closed-loop mail integrity platform for Quadient folder
inserters.

## Quick Start

If you're using Claude Code, it will read `CLAUDE.md` automatically. Start there.

## Structure

```
aims-knowledge-base/
├── CLAUDE.md                        ← Claude Code project context (read first)
├── README.md                        ← This file
├── docs/
│   ├── aims-overview.md             ← What AIMS is, license tiers, AIMS vs AIMS360
│   ├── aims-architecture.md         ← Workflow, network design, file paths
│   ├── aims-file-formats.md         ← JAF, JCF, JRF specs and field layouts
│   ├── aims-imos-communication.md   ← Handshake protocol, machine registration
│   ├── aims-integrations.md         ← Automate/DocSecure, Power BI, OMS list
│   ├── aims-troubleshooting.md      ← Known issues and fixes
│   └── aims-mrdf-reference.md       ← Industry MRDF vs Quadient JAF mapping
├── scripts/
│   ├── jcf_to_csv.py                ← JCF → CSV parser for Power BI
│   ├── run_jcf_converter.bat        ← Continuous watcher mode
│   └── run_jcf_once.bat             ← One-shot parse mode
└── samples/
    ├── sample.jcf                   ← Anonymized JCF for testing
    └── sample.json                  ← Anonymized AIMS360 simulator job file
```

## Key Concepts at a Glance

| Term | Meaning |
|------|---------|
| JAF | Job Allocation File — input checklist, one record per mailpiece |
| JCF | Job Complete File — output audit, fixed-width, one line per piece |
| JRF | Job Reprint File — subset of pieces that need reprinting |
| IMOS | Integrated Mail Operating System — firmware running on inserter PCs |
| FileDrop | Watched folder at `C:\Program Files (x86)\AIMS\AIMS\FileDrop` |
| CheckConnection | Handshake command sent by simulator to AIMS before each run |

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.0 | May 2026 | Initial KB compiled from Claude.ai Project conversation history |
