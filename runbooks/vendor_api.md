# Vendor API / third-party HTTP

Use this when the app calls an **external** vendor (hosted Q2, FX, payment, IdP token endpoint that is not our IIS site). IIS and Okta catalogs do not cover vendor SLAs, retries, or their 401 vs 403.

Do not paste API keys, client secrets, PAN, or full auth headers. See `pci_do_not_paste_pan.md`.

## Support next steps (incident copilot)

1. Capture: URL host (not full signed URL), HTTP method, **status**, time, correlation / request id, our app name.
2. Split **401 vs 403 vs 408/504 vs 429 vs 5xx**.
3. Confirm whether **our** IIS returned the error or we are **forwarding** a vendor body (ARR/proxy 502.x → also `iis_codes.md`).
4. Check cert expiry, clock skew, and whether the vendor status page / change window matches the timestamp.
5. Retry only if the verb is safe (GET) and we are not already in a retry storm. Honor `Retry-After` on 429.
6. If the body is Okta-shaped (`errorCode` E0000…) → `okta_auth.md`, not this file.

## 401 Unauthorized (not allowed to authenticate / no valid creds)

Meaning: missing, expired, or wrong **credential or token**. Not “you’re in, but forbidden.”

Check:

- Token/API key present; Authorization scheme (Bearer vs Basic).
- Clock skew (JWT `exp` / `nbf`).
- Client id belongs to **this** vendor environment (test vs prod).
- Password/secret rotation; Okta token: `okta_auth.md` E0000011 / E0000004.

Next: Fiddler/Postman against a **non-prod** endpoint with a redacted header; compare `WWW-Authenticate`.

## 403 Forbidden (authenticated, not allowed)

Meaning: identity is known; **scope, IP, or policy** denied the call.

Check:

- OAuth scopes / entitlements.
- Vendor IP allow list (our NAT/egress changed).
- MFA / policy (if IdP): `okta_auth.md` E0000057, E0000006.
- IIS 403.x on **our** site is not a vendor 403 — `permissions.md` / `iis_codes.md`.

## Timeouts (408, 504, client timeout, “task was canceled”)

Split:

| Kind | Where it died | Next |
|---|---|---|
| Connection timeout | TCP/TLS never completed | DNS, firewall, vendor VIP, cert |
| Request/command timeout | Connected; no response in N seconds | Vendor slowness; our HttpClient timeout; SQL behind **us** (`sql_timeout.md`) |
| IIS 408 | Client too slow sending the request | `iis_codes.md` |
| 504 / 502.3 ARR | We waited on a backend | Backend pool, vendor latency, ARR timeout |

Do not raise our timeout to hide a vendor outage. Log start/stop timestamps and the vendor request id.

## 429 Too Many Requests

Stop bursts. Back off. Record `Retry-After`. Vendor rate limits are not IIS Dynamic IP Restriction (those are 401.501 / 403.501 in `iis_codes.md`).

## 5xx from vendor

Our job: prove we sent a valid request, capture the vendor id, open/join the vendor ticket. Do not loop retries on 500s.

## What to log (safe)

- Timestamp UTC, host, method, status, duration, our correlation id, vendor request id.
- Not: token, cookie, PAN, full query string if it can hold account numbers.

## Pointers

- Our site status/substatus → `iis_codes.md`
- Okta/SSO token → `okta_auth.md`
- Access denied layer picker → `permissions.md`
- App waiting on SQL → `sql_timeout.md`
