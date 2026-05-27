# AIMS Troubleshooting

## CheckConnection Returns NOK

| Cause | Resolution |
|-------|------------|
| Machine not registered in AIMS360 | Register machine in MongoDB with correct name, `_Input` and `_Output` channels |
| Case mismatch (`Test3` vs `test3`) | Verify exact case matches between simulator config and AIMS registration — it is case-sensitive |
| Machine not in active/online state | Toggle machine to active in AIMS360 UI |
| Only `_Input` channel registered | Both `MachineName_Input` AND `MachineName_Output` must exist; simulator checks both |
| IMOS name mismatch | Verify `imosName` in JSON job file matches the machine's IMOS mapping in AIMS |

### Diagnosing from the Log

```
# Good — both machines OK, proceeds to CreateConnection
CheckConnection(AIMS_Test, AIMS_Test_Input)   → OK  ✅
CheckConnection(Machine_1, Machine_1_Input)   → OK  ✅
CheckConnection(AIMS_Test, AIMS_Test_Output)  → OK  ✅
CheckConnection(Machine_1, Machine_1_Output)  → OK  ✅

# Bad — aborts on first NOK, never reaches Output check
CheckConnection(AIMS_Test, AIMS_Test_Input)   → OK  ✅
CheckConnection(Test3, Test3_Input)           → NOK ❌
CloseConnection(Test3, Test3_Input, 0, "BatchId from state is null...")
```

The error `BatchId from state is null. Please create the connection first!` on
`CloseConnection` always means the `CheckConnection` that preceded it failed.

---

## JAF Imports Successfully But Simulator Fails

This is a common source of confusion. The JAF import and the simulator
connection are **separate systems**:

- **JAF import** uses the FileDrop folder watch — only checks file structure
  and JobID uniqueness. Success here only means the job data is in AIMS.
- **Simulator connection** requires machine registration — a completely separate
  configuration. The job can exist in AIMS while the machine is still unknown.
- **The JSON job file** does not contain connection credentials. Machine name,
  IP, and port come from the simulator executable's own configuration.

**Checklist when JAF imports but simulator fails:**
1. Is the machine registered in AIMS360 (MongoDB)?
2. Are both `_Input` and `_Output` channels registered?
3. Does the `imosName` in the JSON file match the machine's IMOS mapping?
4. Is the machine in active/online state in the AIMS360 UI?

---

## JCF Parser Issues

| Issue | Resolution |
|-------|------------|
| `customer_id` shows hash/checksum (e.g. `588e973a`) | Expected for some AIMS configs. Field may not be a traditional customer ID. |
| File not picked up by watcher | Verify extension is exactly `.jcf` — watcher filters strictly by extension |
| `ParseError` on a JCF line | File moves to `jcf_error\` folder; check `jcf_converter.log` for line position and raw content |
| `.jaf` files in FileDrop not being processed | Correct — watcher ignores `.jaf` files by design. Safe to share the folder. |
| Script runs but CSV not updating | Check `WATCH_FOLDER` path is correct; verify `.jcf` files are landing there and not a subdirectory |

---

## DocSecure / Automate Integration Issues

| Issue | Resolution |
|-------|------------|
| `export` folder missing | Manually create `C:\ProgramData\Quadient\Docsecure\DocsecureAdapter\export` |
| JCF/JRF not appearing in export folder | Verify DocSecure Manager Files Settings paths match the `export` folder exactly |
| JAF not being picked up by AIMS | Confirm Automate AGG DS remote location **AIMS hot folder** points to `jaf-input`, not `export` |
| AIMS360 machine not found | Check MongoDB directly — the AIMS360 UI may not show all machine config details |

---

## AIMS360 MongoDB Inspection

When AIMS360 UI doesn't reveal enough, query MongoDB directly:

```javascript
// Connect via MongoDB Compass (localhost, default port 27017)
// or mongosh

show dbs          // list databases
use aims360       // or whatever the AIMS360 db is named
show collections  // find machine-related collections

// Find a working machine to use as a template
db.machines.find({ name: "AIMS_Test" }).pretty()

// Check all registered machines
db.machines.find({}, { name: 1, inputChannel: 1, outputChannel: 1 })
```

---

## Key Lessons Learned

1. **Register both channels** — `_Input` and `_Output` are both required. Missing `_Output` is an easy mistake because the simulator only shows `_Input` failure in the abort message.

2. **AIMS and AIMS360 are different products** — Classic AIMS uses SQL Server; AIMS360 uses MongoDB. Don't apply SQL-based troubleshooting to AIMS360.

3. **The FileDrop folder is shared** — `.jaf`, `.json`, and `.jcf` files all share the same FileDrop path. The JCF watcher only processes `.jcf` files; the others are safe.

4. **Simulator config is in the executable** — If the simulator is a single packaged `.exe`, run `strings.exe` (Sysinternals) on it to extract config key names and hardcoded paths.
