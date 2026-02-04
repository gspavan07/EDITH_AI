"""CLI entrypoint for EDITH."""

from __future__ import annotations

import argparse
from pathlib import Path


def _prompt_choice(prompt: str, choices: list[str]) -> str:
    choices_display = "/".join(choices)
    while True:
        value = input(f"{prompt} ({choices_display}): ").strip()
        if value in choices:
            return value
        print(f"Please choose one of: {choices_display}")


def _prompt_text(prompt: str) -> str:
    return input(f"{prompt}: ").strip()


def _write_config(config_path: Path, data: dict) -> None:
    lines = ["# EDITH configuration", ""]
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{key}:")
            for sub_key, sub_value in value.items():
                lines.append(f"  {sub_key}: {sub_value}")
        elif isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {value}")
    config_path.write_text("\n".join(lines) + "\n")


def setup_command(config_dir: Path) -> None:
    print("EDITH setup wizard")
    provider = _prompt_choice("Select LLM provider", ["OpenAI", "Gemini", "Groq"])
    model = _prompt_text("Select model")
    modes = _prompt_text("Choose interaction modes (comma-separated)").split(",")
    modes = [mode.strip() for mode in modes if mode.strip()]
    enable_local = _prompt_choice("Enable local MCP servers", ["yes", "no"]) == "yes"
    enable_remote = _prompt_choice("Enable remote MCP servers", ["yes", "no"]) == "yes"
    api_key = _prompt_text("Enter API key (stored locally)")

    config_data = {
        "llm": {"provider": provider, "model": model},
        "interaction_modes": modes,
        "mcp": {"local_enabled": enable_local, "remote_enabled": enable_remote},
        "secrets": {"api_key": api_key},
    }

    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "config.yaml"
    _write_config(config_path, config_data)
    print(f"Configuration written to {config_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="EDITH CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    setup_parser = subparsers.add_parser("setup", help="Run EDITH setup")
    setup_parser.add_argument("--config-dir", default="config", help="Config directory")

    args = parser.parse_args()

    if args.command == "setup":
        setup_command(Path(args.config_dir))


if __name__ == "__main__":
    main()
