"""Live check that Grok API works. Key stays in the project-root .env file."""

import os
from pathlib import Path

from dotenv import load_dotenv
from xai_sdk import Client
from xai_sdk.chat import user

# This file lives in python/. The .env file lives at the repository root.
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

api_key = os.getenv("XAI_API_KEY")
if not api_key:
    raise SystemExit(
        "XAI_API_KEY is missing.\n"
        f"Put one line in {ROOT / '.env'}:\n"
        "XAI_API_KEY=your_key_here\n"
        "os.getenv('XAI_API_KEY') is the *name* of the variable, not the secret."
    )

client = Client(api_key=api_key)
chat = client.chat.create(model="grok-4.6")
chat.append(user("Say hello in five words."))
print(chat.sample().content)
