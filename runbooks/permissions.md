# Permissions / access denied

Use this when the incident is **Access is denied**, **401**, **403**, **login works but the page fails**, or SQL **229 / 230 / 262**. This file is a **layer picker**, not a second catalog.

Do not paste passwords, connection strings, or PAN. See `pci_do_not_paste_pan.md`.

## Support next steps (incident copilot)

1. Capture the **exact** message: Windows, IIS substatus, SQL number, or API `errorCode`.
2. Decide the layer (one primary):
   - Browser/IIS status **401.x / 403.x** → IIS / NTFS. Catalog: `iis_codes.md`.
   - **Okta, SSO, OAuth, JWT, E0000xxx** → `okta_auth.md`.
   - SQL **229, 230, 262**, `permission was denied on the object` → `sql_errors_0_to_999.md`.
   - Third-party HTTP **401 vs 403**, API key, vendor portal → `vendor_api.md`.
   - App menu / role inside the banking app (user can log in, cannot see a function) → application role, not OS.
3. Always name the **account that is running**: end user, IIS app-pool identity, SQL login, or service account. Mixing those up is the usual miss.

## Layer 1 — Windows / NTFS / share

Symptoms: 401.3, 403.1–403.3, “Access is denied” on a file, cert, log folder, or share.

Check:

- NTFS ACL on the site root, `bin`, config folder, log folder, cert private key.
- App-pool identity (ApplicationPoolIdentity vs domain service account).
- IUSR / IIS_IUSRS only if that identity is actually in use.
- Share permissions if the content is on a UNC path (share **and** NTFS).

Next: icacls on the path, effective access for the **app-pool account**, IIS log `sc-win32-status` (5 = access denied).

## Layer 2 — IIS / process identity

Symptoms: 403.1 execute, 403.2 read, 403.3 write, 403.19 token rights, 500.19 config, 503.0 pool stopped.

Check:

- IIS site / folder **Handler** and **Authorization** (not only NTFS).
- App pool started; identity can log on as a service.
- `web.config` locked sections (500.19) vs a true ACL miss (401.3).

Catalog: `iis_codes.md`.

## Layer 3 — SQL Server

Symptoms: Msg **229** object permission, **230** column permission, **262** database permission, “The user does not have permission to perform this action” (297).

Check:

- Login exists and is **enabled**; mapped **user** in the right database (login ≠ user).
- `GRANT` / `DENY` / role membership on the proc, table, or schema. Orphaned user after restore.
- App uses a SQL login vs Windows group vs app-pool account (`IIS APPPOOL\name`).

Catalog: `sql_errors_0_to_999.md`. Do not dump a live `sp_helprotect` result with customer names into the copilot.

## Layer 4 — Application role

Symptoms: SSO succeeds, then “you are not authorized” **inside** the app (Q2-like portal, FX desk, admin menu).

Check:

- App role / entitlement, not NTFS.
- Group membership in the IdP **and** the app’s own user table.
- If Okta says success and IIS is 200, it is not a Windows permission problem.

## Layer 5 — API / OAuth scopes

Symptoms: HTTP 401 (no/invalid token) vs 403 (token valid, scope or policy denied).

- 401 + Okta → `okta_auth.md` (E0000004, E0000011, E0000006).
- 401/403 from a **vendor** URL → `vendor_api.md`.
- Do not treat every 401 as NTFS.

## Quick split

| You see | Go to |
|---|---|
| 401.3, 403.1–403.3, NTFS, IUSR | `iis_codes.md` + Layer 1 |
| 401.1 / 401.2, logon failed | `iis_codes.md`; if SSO, `okta_auth.md` |
| Okta `errorCode`, MFA, expired password | `okta_auth.md` |
| SQL 229 / 230 / 262 | `sql_errors_0_to_999.md` |
| Vendor 401/403/timeout | `vendor_api.md` |
| Logged in, missing menu / button | Layer 4 application role |
