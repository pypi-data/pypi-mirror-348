import argparse
import asyncio
from pathlib import Path
from deardir import DearDir
import toml


def get_version():
    pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
    data = toml.load(pyproject_path)
    return data["tool"]["poetry"]["version"]


def main():
    parser = argparse.ArgumentParser(
        description="Validate and optionally fix a directory structure based on a schema.",
        epilog=(
            "Examples:\n"
            "  deardir check C:\\Projects\\myapp --schema schema.yaml\n"
            "  deardir watch ./mydir --schema schema.yaml --interval 5"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"deardir {get_version()}",
        help="Show the version and exit"
    )

    subparsers = parser.add_subparsers(dest="command", metavar="{check,watch}")

    # `check` subcommand
    check_parser = subparsers.add_parser(
        "check",
        help="Check directory structure against a schema",
        description="Validate directory contents and optionally create missing files/folders.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    check_parser.add_argument(
        "path", type=Path, help="Root path to validate (e.g. ./myproject)"
    )
    check_parser.add_argument(
        "--schema", type=Path, required=True, help="Path to schema YAML file"
    )
    check_parser.add_argument(
        "--create", action="store_true", help="Create missing files/folders if they don't exist"
    )

    # `watch` subcommand
    watch_parser = subparsers.add_parser(
        "watch",
        help="Continuously watch a directory for structure compliance",
        description="Watch the directory and re-validate it at regular intervals.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    watch_parser.add_argument("path", type=Path, help="Root path to watch")
    watch_parser.add_argument("--schema", type=Path, required=True, help="Path to schema YAML file")
    watch_parser.add_argument("--interval", type=int, default=10, help="Time between checks in seconds")
    watch_parser.add_argument("--duration", type=int, help="Optional total time to run (seconds)")
    watch_parser.add_argument("--create", action="store_true", help="Create missing files/folders if needed")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    dd = DearDir(root_paths=[args.path], schema=args.schema)
    dd.create_missing = args.create

    if args.command == "check":
        dd.validate()

        if dd.missing:
            print("\nMissing paths:")
            for p in sorted(dd.missing):
                print(f"  - {p}")
        else:
            print("✅ All paths are valid.")

        if dd.created:
            print("\nCreated paths:")
            for p in sorted(dd.created):
                print(f"  ↳ {p}")

    elif args.command == "watch":
        print("Live monitoring started. Press Ctrl+C to stop.")
        asyncio.run(dd.live(interval=args.interval, duration=args.duration))
        