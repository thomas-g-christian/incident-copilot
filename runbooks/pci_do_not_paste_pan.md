# PCI — do not paste PAN (incident copilot gate)

**This copilot is not a PCI evidence store.** Never paste Primary Account Numbers (PAN), full card data, CVV, PINs, passwords, recovery answers, connection-string passwords, or live Okta tokens into the incident text, tickets copied here, or model prompts.

If the user pasted secrets: stop, tell them to **rotate** the credential, and continue with **redacted** symptoms only (error code, HTTP status, timestamp, host, object name without account numbers).

Use this file when the incident mentions PCI, PAN, card data, DSS, or “can I paste the log.”

## Copilot rules

1. Refuse to analyze blobs that look like card numbers, tracks, or auth tokens.
2. Ask for **error number / HTTP status / Okta errorCode / IIS substatus** instead of raw payloads.
3. Point at the right runbook: `okta_auth.md`, `iis_codes.md`, `sql_timeout.md`, `sql_errors_0_to_999.md`, `vendor_api.md`, `permissions.md`.
4. Target system for this lab: **API integration** (vendor + Okta + SQL behind IIS) — not a full QSA program.

## Core runbook phases (org PCI, not the copilot)

a. Scope discovery  
b. Network segmentation  
c. Vulnerability management  
d. Access control  
f. Continuous monitoring  

## Maintenance and evidence (org, not this repo)

a. Quarterly tasks  
b. Annual tasks  
c. Incident response  

Evidence belongs in the bank’s PCI process, not in `evals/` or GitHub. This repo uses **invented** samples only.

## Pointers

- Access control issues → `permissions.md`  
- API vendor / secrets in headers → `vendor_api.md`  
- Okta recovery / password → `okta_auth.md` (still no answers in the prompt)
