# AIMS IMOS / Simulator Communication

## Overview

The DS Simulator (AIMS360) communicates with AIMS via TCP on **port 8989**
(localhost). The simulator sends a `CheckConnection` handshake for each
registered machine before starting any job processing.

---

## Connection Handshake Protocol

The handshake checks **both Input and Output channels** for every machine before
proceeding to `CreateConnection`. If ANY check returns `NOK`, the simulator
aborts immediately.

### Successful Sequence

```
CheckConnection(AIMS_Test, AIMS_Test_Input)   → OK  ✅
CheckConnection(Machine_1, Machine_1_Input)   → OK  ✅
CheckConnection(AIMS_Test, AIMS_Test_Output)  → OK  ✅
CheckConnection(Machine_1, Machine_1_Output)  → OK  ✅
CreateConnection(Machine_1, Machine_1_Input, ...) → begins processing
```

### Failed Sequence (NOK example)

```
CheckConnection(AIMS_Test, AIMS_Test_Input)   → OK  ✅
CheckConnection(Test3, Test3_Input)           → NOK ❌  (simulator aborts)
CloseConnection(Test3, Test3_Input, 0, "BatchId from state is null...")
```

> ⚠️ The simulator aborts at the **first NOK**. It will never reach
> `CreateConnection`. A missing `_Output` channel causes failure at a later
> point in the sequence than a missing `_Input` channel — but both are fatal.

---

## Machine Registration Requirements

For a machine to pass `CheckConnection`, it must be registered in AIMS with
**both** channels:

| Field | Value Pattern | Example |
|-------|---------------|---------|
| Machine Name | Exact string, case-sensitive | `Machine_1`, `AIMS_Test` |
| Input Channel | `MachineName_Input` | `Machine_1_Input` |
| Output Channel | `MachineName_Output` | `Machine_1_Output` |
| Machine Model | Must match simulator config | `DS.700` |
| IP Address | Loopback for local simulator | `127.0.0.1` |
| Machine Port | Simulator listen port | `13008` |
| AIMS Host Port | AIMS listen port | `8989` |
| Mode | Simulator default | `6` |

> ⚠️ **Case sensitivity:** `Test3`, `test3`, and `TEST3` are treated as
> different machines. The name must exactly match what the simulator announces.

---

## AIMS360 Machine Registration (MongoDB)

Classic AIMS stores machine config in SQL Server. AIMS360 uses **MongoDB**.

### Inspecting Existing Machine Config

```javascript
// Connect via MongoDB Compass or mongosh to localhost
show collections
// Look for: machines, devices, configurations, inserters

// View a working machine's config
db.machines.find({ name: "AIMS_Test" })

// To register a new machine (Test3), duplicate the AIMS_Test document
// and update: name → "Test3", input → "Test3_Input", output → "Test3_Output"
```

### Common Collection Names to Check

- `machines`
- `devices`
- `configurations`
- `inserters`

---

## Simulator JSON Job File

The JSON job file (placed in FileDrop) is **payload data only** — it describes
what to process, not how to connect.

### Key Fields (from sample `31CD77GGBW.json`, 25 mailpieces)

| Field | Value | Notes |
|-------|-------|-------|
| `jobId` | `"31CD77GGBW"` | 10-character alphanumeric Job ID |
| `mailPieceCount` | `25` | Total pieces in this run |
| `imosName` | `"IMOS_006"` | IMOS identifier — must map to a registered machine |
| `imosNameId` | `"SIMU"` | `SIMU` = simulator-generated profile |

Per-piece data includes: feeder selections, weights, stacker instructions.

> ⚠️ The JSON job file does **not** contain machine name, IP, or port.
> Connection identity comes from the simulator executable's configuration,
> not the job file. If the simulator is a single packaged executable,
> use Sysinternals `strings.exe` to extract config key names from the binary.

---

## Simulator Configuration (DS Simulator GUI)

Confirmed fields from the simulator's instance configuration UI:

| Setting | Example Value |
|---------|---------------|
| Machine Name | `Test3` |
| Machine Model | `DS.700` |
| Model (dropdown) | `Office` |
| Operator | `Operator` |
| IP Address | `127.0.0.1` |
| Port | `13008` |
| Mode | `6` |
| AIMS Host | `127.0.0.1:8989` |
