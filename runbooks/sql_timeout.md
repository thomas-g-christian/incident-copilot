# SQL timeout / blocking

Use this when the incident is a **timeout**, **blocking**, **lock wait**, `Execution Timeout Expired`, `OLE DB wait`, or IIS **408** on a page that hits SQL. Error **numbers 0–999** live in `sql_errors_0_to_999.md`; this file is the **wait/timeout playbook** (including 1205 deadlock, which is outside 0–999).

Do not paste PAN, full result sets, or connection strings with passwords. See `pci_do_not_paste_pan.md`.

## Support next steps (incident copilot)

1. Split **connection timeout** vs **command/query timeout** vs **lock blocking** vs **deadlock**.
2. Capture: app name, UTC time, duration, error text, whether IIS returned 500 or 408 (`iis_codes.md`).
3. On the instance (if you have rights): blocking session, wait type, login, host. Do not dump customer rows.
4. If the message is Msg **102, 137, 207, 208, 229, 515, 547** it is **not** a timeout — use `sql_errors_0_to_999.md`.
5. If the HTTP client timed out talking to a **vendor**, use `vendor_api.md`.

## Connection timeout

Symptoms: “unable to connect”, network-related or instance-specific error, connection timeout (often ~15s default).

Check: SQL Browser/TCP 1433, DNS, firewall, instance down, connection string `Data Source`, TLS. Not a query plan problem.

## Command / execution timeout

Symptoms: `Execution Timeout Expired`; `Timeout expired. The timeout period elapsed prior to completion of the operation`. App `CommandTimeout` (often 30s) fired.

Check:

- Query actually ran longer than the app timeout (blocking or a bad plan).
- Raising the timeout hides the cause; find the waiter first.

## Blocking / lock wait

Symptoms: session waiting on `LCK_*`; `head blocker`; app hung then timed out.

Next (read-only, no customer data):

```sql
-- who is waiting, who is blocking (no row payloads)
SELECT r.session_id, r.status, r.wait_type, r.wait_time, r.blocking_session_id,
       r.command, t.text
FROM sys.dm_exec_requests r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE r.blocking_session_id <> 0 OR r.session_id IN
      (SELECT blocking_session_id FROM sys.dm_exec_requests WHERE blocking_session_id <> 0);
```

Do not kill a session until the blocker is identified and the change window allows it.

## Deadlock (1205)

Symptoms: Msg 1205, transaction was deadlocked. Not in the 0–999 catalog.

Next: deadlock graph from error log / extended events; retry is normal for the **victim**; fix if it repeats (order of updates, indexes).

## IIS 408 vs SQL

IIS **408** = client did not finish sending the request in time (`iis_codes.md`). If the **browser** waited on our page and SQL was blocked, you usually see **500** + SQL timeout in the app log, not 408.

## Pointers

- Error **number** 0–999 → `sql_errors_0_to_999.md`
- Permission 229/230/262 → `permissions.md` Layer 3
- Outbound HTTP timeout → `vendor_api.md`
