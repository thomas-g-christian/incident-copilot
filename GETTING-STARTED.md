# Getting started: PyCharm and the xAI API key

Python IDE for this project: **PyCharm** (Professional or Community).  
C# later: Jetbrains Rider 2026.2.

A Grok *chat* login (grok.com or this TUI) is **not** an API key. The incident copilot calls `https://api.x.ai/v1` and needs a **console API key plus prepaid credits**.

Official docs (check if screens move): [Quickstart](https://docs.x.ai/developers/quickstart) · [API Keys](https://console.x.ai/team/default/api-keys) · [Models](https://docs.x.ai/developers/models)

**Status:** Hour 1 and Week 1 CLI are done. Live Grok call works (`python/hello_grok.py` and `python/app.py --incident samples/sql_timeout.txt`). Interpreter: `.\.venv`. Next: [PLAN.md](PLAN.md) Week 2 evals.

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

## 4. Put the key in this folder (Windows)

In PowerShell:

```powershell
cd .
@"
XAI_API_KEY=paste_the_key_here_no_quotes
"@ | Set-Content -Path .env -Encoding utf8
```

Replace `paste_the_key_here_no_quotes` with the real key. No spaces around `=`.

Check that `.gitignore` lists `.env` (it already does). Confirm Git will not stage it:

```powershell
git check-ignore -v .env
```

You want a hit on `.gitignore`. If `git` is not on PATH, use `C:\Program Files\Git\cmd\git.exe`.

Also create a dummy for the repo (no secret):

```powershell
@"
XAI_API_KEY=
"@ | Set-Content -Path .env.example -Encoding utf8
```

**Never** commit `.env`. **Never** put the key in source files.

You can reuse the same key later in `grok-python-lab\.env` if you want that lab live too. Prefer one key per project if you like easy revoke.

---

## 5. Open the project in PyCharm

1. Start **PyCharm**.
2. **File → Open** and choose `.` (the folder, not a single file).
3. Trust the project if PyCharm asks.
4. **File → Settings → Project → Python Interpreter**
   - Use the project venv PyCharm created: `.\.venv`
   - Python 3.13 or 3.14 is fine.
5. Mark `python` as Sources Root when that package exists (**right-click `python` → Mark Directory as → Sources Root**).
6. Load the env file for Run/Debug:
   - **Run → Edit Configurations → Edit configuration templates → Python**
   - Enable **EnvFile** if you have the EnvFile plugin, pointing at `.\.env`  
   - **or** in the configuration **Environment variables**, click the folder icon and load from `.env`  
   - **or** in code use `python-dotenv` (`load_dotenv()` from the project root `.env`).

PyCharm Community: no EnvFile plugin required if you use `python-dotenv` in `app.py`. That is the simplest path.

7. Do not check “Share” on run configurations that contain the key.

When you run a script, the console should see `XAI_API_KEY`. A missing key looks like `401` / `Unauthorized` / `api_key` errors, not a Python syntax error.

---

## 6. Prove the key works (before Week 1 app code)

After the venv exists, in PyCharm’s terminal (venv should be active):

```powershell
cd .
python -m pip install openai python-dotenv
```

Run `python/hello_grok.py` from this project. It loads `.\.env` (one folder above the script). Do not hardcode the key.

Confirm the current model name on [Models](https://docs.x.ai/developers/models) if `grok-4.6` 404s.

**Done when:** PyCharm run prints a short hello. **This is complete.** Then go to [PLAN.md](PLAN.md) Week 1 remaining items.

---

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| 401 / invalid API key | Typo, extra quotes, old revoked key, `.env` not loaded |
| 402 / credits / billing | Balance is $0 — add credits in console |
| 404 model | Model id changed — check docs.x.ai/developers/models |
| Key in GitHub | Revoke it **now** in the console, make a new key, `git filter` is not enough if it was pushed — rotate |
| PyCharm “no module …” | Interpreter is not `.\.venv` |
