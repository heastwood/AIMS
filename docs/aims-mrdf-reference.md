# MRDF vs JAF Reference

## What is an MRDF?

A **Mail Run Data File (MRDF)** is an industry-standard concept: one record per
mailpiece, used in high-volume mail production to ensure every document ends up
in the correct envelope. It is the backbone of **File-Based Processing (FBP)**
and closed-loop integrity.

The MRDF is generated alongside the print file as documents are electronically
sorted and postal-sorted. Each page carries a barcode with a piece ID; the
inserter scans that barcode, looks up the matching record in the MRDF, and uses
those instructions to assemble the mailpiece.

---

## Quadient Terminology Mapping

| Industry Term | Quadient AIMS Equivalent |
|---------------|--------------------------|
| MRDF (Mail Run Data File) | JAF (Job Allocation File) |
| File-Based Processing (FBP) | Closed-Loop Verification (AIMS-500) |
| Mailpiece ID / Piece Record | MailPieceID (10-digit) |
| Job / Run ID | JobID (10-digit) |
| Reprint / Divert file | JRF (Job Reprint File) |
| Completion / Audit file | JCF (Job Complete File) |

---

## How Quadient's JAF Differs from a Classic MRDF

| Aspect | Classic MRDF | Quadient JAF |
|--------|-------------|--------------|
| Storage | Flat file (fixed-width or CSV) | SQL database (imported from flat file) |
| PII in file | Often includes full name, address | IDs only — PII stays in OMS |
| Access | Static file on inserter PC | Browser-based, queryable via SQL |
| Reprint tracking | Manual or separate system | Automatic JRF generation |
| Multi-vendor | Vendor-specific formats | AIMS-1000 bridges other vendor formats |

---

## Federal MRDF Spec (Reference)

The U.S. federal government MRDF specification uses **fixed-width 701-character
records**, one per mailpiece. This is the format Pitney Bowes/BlueCrest
implementations are based on.

| Position | Length | Field |
|----------|--------|-------|
| 1–5 | 5 | Job ID |
| 6–11 | 6 | Piece ID |
| 12–13 | 2 | Total Pages |
| 14–22 | 1 each | Select Feeders 2–10 (0=no feed, 1=feed) |
| 23–26 | 1 each | Vertical Stackers 1–4 |
| 27 | 1 | Sealer outsort |
| 28–29 | 1 each | Meter 1 & 2 |
| 30–69 | 40 | Customer Name |
| 70–309 | 40 each | Address Lines 1–6 |
| 310–320 | 11 | ZIP+4+2 |
| 321–520 | 40 each | Return Name + Address |
| 521–536 | 16 | Account ID |
| 537–580 | 44 | Input File Name |
| 581–645 | 65 | IMBC (Intelligent Mail Barcode) codes |
| 646–657 | — | Service Type & Serial ID |
| 690–700 | — | Vendor ID, Code Name, Total Documents |

---

## Practical Takeaway

If you're integrating with AIMS, you're producing a **JAF**, not an MRDF — but
the design thinking is the same: one record per mailpiece, keyed by
JobID + MailPieceID, with feeder/stacker/sealer instructions.

The key differences:
- Keep PII out of the JAF (AIMS doesn't need it)
- Drop the file into a watched folder for SQL ingestion rather than streaming directly
- Use AIMS-1000 if you need to bridge an existing MRDF-format pipeline into Quadient hardware
