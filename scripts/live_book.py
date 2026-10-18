#!/usr/bin/env python3
"""Serve the TeachBook with automatic rebuilds during local development."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = ROOT / "book"
BUILD_DIR = BOOK_DIR / "_build" / "html"


def ensure_tool(name: str) -> None:
    """Exit with a helpful message if *name* is not available on PATH."""
    if shutil.which(name):
        return
    print(f"Missing required command: {name}", file=sys.stderr)
    print("Install dependencies with `pip install -r requirements-dev.txt`.", file=sys.stderr)
    sys.exit(1)


def build_book() -> None:
    """Run the TeachBooks build, keeping the server alive on failure."""
    print("Rebuilding TeachBook…", flush=True)
    try:
        subprocess.run(
            ["teachbooks", "build", "book"],
            cwd=ROOT,
            check=True,
        )
        print("Build completed.", flush=True)
    except subprocess.CalledProcessError as exc:
        print("Build failed, see details above. Watching for more changes…", file=sys.stderr)
        if exc.returncode == 127:
            print("Ensure the virtual environment is activated and TeachBooks is installed.", file=sys.stderr)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Serve the book with live reload and automatic rebuilds.",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Interface to bind the development server.")
    parser.add_argument("--port", type=int, default=8000, help="Port for the development server.")
    parser.add_argument(
        "--open-browser",
        action="store_true",
        help="Open the default web browser once the server is ready.",
    )
    return parser.parse_args()


def should_ignore(path: str) -> bool:
    """Return True when the path points to generated artifacts we should skip."""
    normalized = path.replace("\\", "/")
    if "/_build/" in normalized or normalized.endswith("/_build"):
        return True
    ignored_suffixes = (".log", ".tmp", ".swp", ".swo", "~")
    return normalized.endswith(ignored_suffixes)


def main() -> None:
    args = parse_args()

    ensure_tool("teachbooks")
    try:
        from livereload import Server
    except ImportError as exc:  # pragma: no cover - triggered only in misconfigured envs
        print("Could not import livereload. Install dev dependencies first.", file=sys.stderr)
        raise SystemExit(1) from exc

    if not BOOK_DIR.exists():
        print(f"Expected book directory at {BOOK_DIR}", file=sys.stderr)
        sys.exit(1)

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    build_book()

    server = Server()
    # Rebuild when any book content or configuration changes.
    server.watch(str(BOOK_DIR / "**" / "*"), build_book, ignore=should_ignore)
    server.watch(str(ROOT / "requirements.txt"), build_book)

    print(
        "Serving built HTML from "
        f"{BUILD_DIR}\nOpen http://{args.host}:{args.port} in your browser.",
        flush=True,
    )

    serve_kwargs = {
        "root": str(BUILD_DIR),
        "host": args.host,
        "port": args.port,
        "restart_delay": 1,
    }
    if args.open_browser:
        serve_kwargs["open_url_delay"] = 1

    server.serve(**serve_kwargs)


if __name__ == "__main__":
    main()
