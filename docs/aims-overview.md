# AIMS System Overview

## What is AIMS?

AIMS (Automated Insertion Management System) is Quadient's closed-loop mail
integrity platform. It validates every mailpiece in a production run against a
pre-generated job file, ensuring no piece is missed, duplicated, or mis-inserted.

## What AIMS Does

- Imports a Job Allocation File (JAF) into a SQL/MongoDB database before a run begins
- Communicates in real time with IMOS (inserter firmware) during each scan
- Validates each piece: is it expected? has it already been processed?
- Detects missing, duplicate, and unmatched documents
- Generates reprint files (JRF) and records completion data (JCF)
- Provides browser-based job tracking accessible from anywhere on the network

---

## License Tiers

| Tier | Description |
|------|-------------|
| **AIMS-100** (Audit Trail) | No JAF required. Generates audit records on the fly as inserters run. Best for traceability without strict closed-loop verification. |
| **AIMS-500** (Closed-Loop Verification) | Full closed-loop. JAF is mandatory. Inserter must confirm each piece against the job file before processing. |
| **AIMS-1000** (External Loop) | Includes an interface-mapping module to bridge other vendor MRDF formats (Pitney Bowes, BlueCrest, etc.) into AIMS and export back. |

---

## AIMS vs AIMS360

| | AIMS (Classic) | AIMS360 |
|--|----------------|---------|
| **Database** | SQL Server | MongoDB |
| **Architecture** | Desktop-oriented, traditional install | Modern, browser-based UI |
| **Communication** | File-based via FileDrop folder | REST/JSON with inserter simulator |
| **Machine registration** | SQL Server tables | MongoDB collections |

> ⚠️ **Important:** Machine registration in AIMS360 is in MongoDB, not SQL Server.
> Use MongoDB Compass or `mongosh` to inspect and create machine records.

---

## Compatible Inserter Models

AIMS supports Quadient folder inserters running IMOS firmware, including:

- DS-160 / DS-180i
- DS-200
- DS-700 *(model used in simulator configuration)*
- DS-1200
