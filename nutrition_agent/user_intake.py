"""
User interaction module – collects profile details via a rich CLI interface.
"""
from __future__ import annotations

import re
import sys
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table
from rich import box

from nutrition_agent.config import (
    APP_NAME,
    APP_VERSION,
    DIET_OPTIONS,
    MEDICAL_CONDITIONS,
)

console = Console()


# ────────────────────────── banner ──────────────────────────────────────────

def show_banner() -> None:
    banner = f"""
  ╔══════════════════════════════════════════════════════════╗
  ║       🥗  {APP_NAME}       ║
  ║              Powered by IBM Granite LLM  v{APP_VERSION}          ║
  ║                                                          ║
  ║  Helping you eat smarter, live better – ethically.       ║
  ╚══════════════════════════════════════════════════════════╝
"""
    console.print(Panel(banner, style="bold green"))


# ────────────────────────── validators ──────────────────────────────────────

def _validate_name(name: str) -> Optional[str]:
    name = name.strip()
    if not name or len(name) < 2:
        return None
    if re.search(r"[^a-zA-Z\s\-']", name):
        return None
    return name.title()


def _validate_age(age_str: str) -> Optional[int]:
    try:
        age = int(age_str.strip())
        return age if 5 <= age <= 120 else None
    except ValueError:
        return None


def _validate_city(city: str) -> Optional[str]:
    city = city.strip()
    return city.title() if len(city) >= 2 else None


# ────────────────────────── prompts ─────────────────────────────────────────

def _prompt_name() -> str:
    while True:
        name = Prompt.ask("\n👤 [bold cyan]Your full name[/bold cyan]")
        validated = _validate_name(name)
        if validated:
            return validated
        console.print("  ⚠️  Please enter a valid name (letters only, min 2 chars).", style="yellow")


def _prompt_age() -> int:
    while True:
        age_str = Prompt.ask("🎂 [bold cyan]Your age[/bold cyan] (years)")
        age = _validate_age(age_str)
        if age is not None:
            return age
        console.print("  ⚠️  Please enter a valid age between 5 and 120.", style="yellow")


def _prompt_diet() -> str:
    console.print("\n🥦 [bold cyan]Diet preference:[/bold cyan]")
    for i, opt in enumerate(DIET_OPTIONS, 1):
        console.print(f"   [{i}] {opt}")
    while True:
        choice = Prompt.ask("   Enter number", default="1")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(DIET_OPTIONS):
                return DIET_OPTIONS[idx]
        except ValueError:
            pass
        console.print("  ⚠️  Please enter a valid number.", style="yellow")


def _prompt_medical_history() -> list[str]:
    console.print("\n🏥 [bold cyan]Medical history[/bold cyan] (enter numbers separated by commas):")
    for i, cond in enumerate(MEDICAL_CONDITIONS, 1):
        console.print(f"   [{i:2d}] {cond}")

    while True:
        choices_str = Prompt.ask("   Enter numbers (e.g. 1 or 2,3)", default="1")
        selected = []
        valid = True
        for part in re.split(r"[,\s]+", choices_str.strip()):
            if not part:
                continue
            try:
                idx = int(part) - 1
                if 0 <= idx < len(MEDICAL_CONDITIONS):
                    selected.append(MEDICAL_CONDITIONS[idx])
                else:
                    valid = False
                    break
            except ValueError:
                valid = False
                break

        if valid and selected:
            if "None" in selected:
                return ["None"]
            # Remove "None" if mixed
            return [c for c in selected if c != "None"]
        console.print("  ⚠️  Please enter valid numbers from the list.", style="yellow")


def _prompt_location() -> tuple[str, str]:
    while True:
        city = Prompt.ask("\n🌍 [bold cyan]Your city[/bold cyan]")
        validated_city = _validate_city(city)
        if validated_city:
            break
        console.print("  ⚠️  Please enter a valid city name.", style="yellow")

    country = Prompt.ask("🗺️  [bold cyan]Your country[/bold cyan]")
    return validated_city, country.strip().title()


def _prompt_goal() -> str:
    goals = [
        "General healthy eating",
        "Weight loss",
        "Muscle gain / High protein",
        "Manage diabetes",
        "Lower blood pressure",
        "Improve energy levels",
        "Better digestion",
    ]
    console.print("\n🎯 [bold cyan]Primary health goal:[/bold cyan]")
    for i, g in enumerate(goals, 1):
        console.print(f"   [{i}] {g}")
    while True:
        choice = Prompt.ask("   Enter number", default="1")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(goals):
                return goals[idx]
        except ValueError:
            pass
        console.print("  ⚠️  Please enter a valid number.", style="yellow")


# ────────────────────────── main collector ──────────────────────────────────

def collect_user_profile() -> dict:
    """Interactive CLI to collect full user profile. Returns profile dict."""
    show_banner()

    console.print(
        "\n[bold green]Welcome! I'm NutritionAgent, your personal AI nutritionist.[/bold green]\n"
        "I'll ask you a few quick questions to build your customised nutrition plan.\n"
        "[dim]All information is used only to generate your plan and is not stored.[/dim]\n"
    )

    name    = _prompt_name()
    age     = _prompt_age()
    diet    = _prompt_diet()
    medical = _prompt_medical_history()
    city, country = _prompt_location()
    goal    = _prompt_goal()

    profile = {
        "name": name,
        "age": age,
        "diet_preference": diet,
        "medical_history": medical,
        "city": city,
        "country": country,
        "goal": goal,
    }

    # ── confirmation table ───────────────────────────────────────────────────
    table = Table(title="📋 Your Profile Summary", box=box.ROUNDED, style="cyan")
    table.add_column("Field", style="bold")
    table.add_column("Value")
    for k, v in profile.items():
        display_val = ", ".join(v) if isinstance(v, list) else str(v)
        table.add_row(k.replace("_", " ").title(), display_val)

    console.print()
    console.print(table)
    console.print()

    if not Confirm.ask("✅ [bold]Looks good? Generate your nutrition plan now?[/bold]", default=True):
        console.print("No problem! Run the app again when you're ready. 👋", style="yellow")
        sys.exit(0)

    return profile
