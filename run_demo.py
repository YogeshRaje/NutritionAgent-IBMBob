"""
run_demo.py  –  Simulates a complete run.bat session non-interactively.
Run:  python run_demo.py
"""
import sys, time, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, ".")

# ── Banner (same as run.bat) ──────────────────────────────────────────────────
print()
print("=" * 62)
print("  NutritionAgent - IBM Granite LLM  |  Powered by IBM Bob")
print("=" * 62)
print()

# ── Step 1: Check Python ──────────────────────────────────────────────────────
import platform
print(f"[SETUP] Python version   : {platform.python_version()}")

# ── Step 2: Load .env & check credentials ────────────────────────────────────
from dotenv import load_dotenv
load_dotenv()
from nutrition_agent.config import IBM_API_KEY, IBM_PROJECT_ID, IBM_REGION, MODEL_ID, APP_NAME, APP_VERSION

if not IBM_API_KEY or not IBM_PROJECT_ID:
    print("[ERROR] .env credentials missing. Add IBM_API_KEY and IBM_PROJECT_ID.")
    sys.exit(1)

print(f"[SETUP] .env loaded      : credentials found")
print(f"[SETUP] Application      : {APP_NAME} v{APP_VERSION}")
print(f"[SETUP] IBM Granite Model: {MODEL_ID}")
print(f"[SETUP] IBM Region       : {IBM_REGION}")
print()

# ── Step 3: Simulated interactive intake ─────────────────────────────────────
print("-" * 62)
print("  USER INTAKE  (simulated interactive session)")
print("-" * 62)

profile = {
    "name"             : "Sneha Patil",
    "age"              : 29,
    "diet_preference"  : "Vegan",
    "medical_history"  : ["None"],
    "city"             : "Nashik",
    "country"          : "India",
    "goal"             : "Weight loss",
}

rows = [
    ("Full Name",         profile["name"]),
    ("Age",               str(profile["age"]) + " years"),
    ("Diet Preference",   profile["diet_preference"]),
    ("Medical History",   ", ".join(profile["medical_history"])),
    ("City",              profile["city"]),
    ("Country",           profile["country"]),
    ("Health Goal",       profile["goal"]),
]

print()
for label, value in rows:
    print(f"  {label:<20} : {value}")

print()
print("  [Profile confirmed] Generating your nutrition plan...")
print()

# ── Step 4: Guardrail check ───────────────────────────────────────────────────
print("[GUARD] Testing input guardrails...")
from nutrition_agent.llm_client import NutritionLLMClient

# Instantiate with mocked model just for guardrail test
from unittest.mock import patch, MagicMock
with patch("nutrition_agent.llm_client.APIClient"), \
     patch("nutrition_agent.llm_client.ModelInference"):
    _gc = NutritionLLMClient()
    safe_chk   = _gc._input_guardrail("What healthy foods help manage weight?")
    unsafe_chk = _gc._input_guardrail("I want a starvation diet plan")

print(f"  Safe prompt    blocked? {'NO  (correct - allowed through)' if safe_chk is None else 'YES (unexpected)'}")
print(f"  Harmful prompt blocked? {'YES (correct - BLOCKED)' if unsafe_chk else 'NO  (guardrail FAILED)'}")
print()

# ── Step 5: Connect to IBM Granite ───────────────────────────────────────────
print("[INFO]  Connecting to IBM watsonx.ai...")
client = NutritionLLMClient()
print("[INFO]  IBM Granite client initialised OK")
print()

# ── Step 6: Generate plan ─────────────────────────────────────────────────────
print("[INFO]  Generating personalised nutrition plan.")
print("[INFO]  Calling IBM Granite API – please wait (20-90 seconds)...")
print()

start = time.time()
plan = client.generate_nutrition_plan(profile)
elapsed = time.time() - start

print(f"[INFO]  Plan generated in {elapsed:.1f}s  ({len(plan):,} characters)")
print()

# ── Step 7: Save to .md ───────────────────────────────────────────────────────
from nutrition_agent.plan_generator import save_plan
filepath = save_plan(profile, plan)
print(f"[INFO]  Plan saved to: {filepath}")
print()

# ── Step 8: Display full plan ─────────────────────────────────────────────────
print("=" * 62)
print("  GENERATED NUTRITION PLAN — IBM Granite AI Output")
print("=" * 62)
print(plan)
print()
print("=" * 62)
print("  Session complete.")
print(f"  Your plan is saved at: {filepath}")
print("=" * 62)
