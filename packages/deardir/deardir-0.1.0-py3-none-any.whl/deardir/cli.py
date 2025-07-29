import argparse
import asyncio
from pathlib import Path
from deardir import DearDir


def main():
    parser = argparse.ArgumentParser(description="Validate and optionally fix directory structure")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # `check` subcommand
    check_parser = subparsers.add_parser("check", help="Check directory structure")
    check_parser.add_argument("path", type=Path, help="Root path to validate")
    check_parser.add_argument("--schema", type=Path, required=True, help="Path to schema file")
    check_parser.add_argument("--create", action="store_true", help="Create missing files/folders")

    # `watch` subcommand
    watch_parser = subparsers.add_parser("watch", help="Live watch mode (async)")
    watch_parser.add_argument("path", type=Path, help="Root path to watch")
    watch_parser.add_argument("--schema", type=Path, required=True, help="Path to schema file")
    watch_parser.add_argument("--interval", type=int, default=10, help="Validation interval in seconds")
    watch_parser.add_argument("--duration", type=int, help="Total time in seconds (optional)")
    watch_parser.add_argument("--create", action="store_true", help="Create missing files/folders")

    args = parser.parse_args()

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
        asyncio.run(dd.live(interval=args.interval, duration=args.duration))