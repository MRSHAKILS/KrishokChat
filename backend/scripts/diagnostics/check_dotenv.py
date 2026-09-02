"""Check dotenv loading."""
import os
import pathlib

import dotenv

ROOT = pathlib.Path(r"D:\KrishokChat Advisory System\backend")
project_root = ROOT.parent

print("Loading .env:", project_root / ".env", "exists:", (project_root / ".env").exists())
print("Loading .env.local:", ROOT / ".env.local", "exists:", (ROOT / ".env.local").exists())

dotenv.load_dotenv(project_root / ".env", override=False)
dotenv.load_dotenv(ROOT / ".env.local", override=False)

k1 = os.getenv("GEMINI_API_KEY_1")
print(f"GEMINI_API_KEY_1: {k1[:20] if k1 else 'NOT SET'}")
print(f"OPENROUTER_API_KEY: {os.getenv('OPENROUTER_API_KEY', 'NOT SET')[:20]}")
