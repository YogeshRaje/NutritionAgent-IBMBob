"""
Main entry point for the Nutrition Agentic AI application.
Run: python main.py
"""
from __future__ import annotations

import sys
from rich.console import Console

console = Console()


def main() -> None:
    # ── lazy imports so env is loaded before anything hits ibm sdk ──────────
    from nutrition_agent.config import IBM_API_KEY, IBM_PROJECT_ID
    from nutrition_agent.user_intake import collect_user_profile
    from nutrition_agent.plan_generator import generate_and_display_plan

    # ── preflight credential check ───────────────────────────────────────────
    if not IBM_API_KEY or not IBM_PROJECT_ID:
        console.print(
            "[bold red]❌ IBM credentials missing.[/bold red]\n"
            "Please set IBM_API_KEY and IBM_PROJECT_ID in your .env file.\n"
            "See README.md for setup instructions.",
            style="red",
        )
        sys.exit(1)

    try:
        profile = collect_user_profile()
        generate_and_display_plan(profile)
    except KeyboardInterrupt:
        console.print("\n\n👋 Session cancelled. Goodbye!", style="yellow")
        sys.exit(0)
    except Exception as exc:
        console.print(f"\n[bold red]❌ Unexpected error:[/bold red] {exc}", style="red")
        console.print("Please check your internet connection and IBM credentials.", style="dim")
        sys.exit(1)


if __name__ == "__main__":
    main()
