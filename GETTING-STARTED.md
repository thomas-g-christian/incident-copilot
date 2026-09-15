# Getting started: PyCharm and the xAI API key

Python IDE for this project: **PyCharm** (Professional or Community).  
C# later: Jetbrains Rider 2026.2.

A Grok *chat* login (grok.com or this TUI) is **not** an API key. The incident copilot calls `https://api.x.ai/v1` and needs a **console API key plus prepaid credits**.

Official docs (check if screens move): [Quickstart](https://docs.x.ai/developers/quickstart) · [API Keys](https://console.x.ai/team/default/api-keys) · [Models](https://docs.x.ai/developers/models)

**Status:** CLI and evals are done (**8/10 → 10/10**). Use a venv at the repo root (`.venv`). Next: [PLAN.md](PLAN.md) C#.

---

## 1. Create an xAI account

1. Open [https://console.x.ai](https://console.x.ai/login?mode=sign-up).
2. Sign up (or sign in) with the account you want billed. X/xAI login is typical.
3. Complete any email or phone verification the console asks for.
4. You should land on the xAI **Console** (not grok.com chat).

If you only have grok.com working, you still need this console step.

---

## 2. Add credits (required for live calls)

API usage is prepaid. A key with **$0 balance** will fail.

1. In the console, open **Billing** / **Credits** (wording may be “Start building” or a credit balance).
2. Add a small amount. **$5–$10** is enough for Weeks 1–2 evals (10 cases, a few reruns).
3. Confirm the balance is not zero before you generate the key.

Do not buy a huge pack. This project is a handful of short prompts.

---

## 3. Generate `XAI_API_KEY`

1. Open [API Keys](https://console.x.ai/team/default/api-keys).
2. Click **Create API key** (or **New key**).
3. Name it something you will recognize, e.g. `incident-copilot-dev`.
4. Copy the key **immediately**. The console often shows the full secret **once**.
5. Store it in a password manager as well as the local `.env` below.

The value looks like a long token (often starting with `xai-`). Treat it like a password.

If you lose it, **revoke** that key in the console and create a new one. Do not paste old keys into chat, email, GitHub, or screenshots.

---

## 4. Put the key in the cloned folder

From the repository root (PowerShell):

```powershell
copy .env.example .env
```

Then edit `.env` so it has one line, no quotes, no spaces around `=`:

```
XAI_API_KEY=paste_the_key_here_no_quotes
```

Confirm Git will not stage it:

```powershell
git check-ignore -v .env
```

You want a hit on `.gitignore`.

**Never** commit `.env`. **Never** put the key in source files. Prefer one key per project so it is easy to revoke.

---

## 5. Open the project in PyCharm

1. Start **PyCharm**.
2. **File → Open** and choose the cloned `incident-copilot` folder (the folder, not a single file).
3. Trust the project if PyCharm asks.
4. **File → Settings → Project → Python Interpreter**
   - Use the project venv: `<repo>\.venv`
   - Python 3.13 or 3.14 is fine.
5. Mark `python` as Sources Root (**right-click `python` → Mark Directory as → Sources Root**).
6. Load the env file for Run/Debug via `python-dotenv` (`load_dotenv()` from the repo-root `.env`). That is already in `python/app.py`.

Do not check “Share” on run configurations that contain the key.

When you run a script, the console should see `XAI_API_KEY`. A missing key looks like `401` / `Unauthorized` / `api_key` errors, not a Python syntax error.

---

## 6. Prove the key works

From the repo root, with the venv active:

```powershell
python -m pip install -r requirements.txt
python python/hello_grok.py
```

`hello_grok.py` loads `.env` from the repository root. Do not hardcode the key.

Confirm the current model name on [Models](https://docs.x.ai/developers/models) if `grok-4.6` 404s.

**Done when:** the run prints a short hello. Then `python python/app.py --incident samples/sql_timeout.txt` and `python python/eval.py`.

---

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| 401 / invalid API key | Typo, extra quotes, old revoked key, `.env` not loaded |
| 402 / credits / billing | Balance is $0 — add credits in console |
| 404 model | Model id changed — check docs.x.ai/developers/models |
| Key in GitHub | Revoke it **now** in the console, make a new key, `git filter` is not enough if it was pushed — rotate |
| PyCharm “no module …” | Interpreter is not the repo-root `.venv` |
