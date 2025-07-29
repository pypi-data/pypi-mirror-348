#!/usr/bin/env python3
import argparse
import json
import os
import random
import re
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from rich.console import Console

from draftmk.version import __version__

console = Console()


def check_prerequisites():
    required = ["docker", "docker-compose"]
    for cmd in required:
        if not shutil.which(cmd):
            console.print(
                f"[bold red][X] Required command '{cmd}' not found. Please install it and try again.[/bold red]"
            )
            sys.exit(1)


def find_open_port(used_ports):
    while True:
        port = random.randint(3000, 3999)
        if port in used_ports:
            continue
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", port))
                used_ports.add(port)
                return port
            except OSError:
                continue


def generate_env(env_path, repo_name=None):
    repo_name = repo_name or Path.cwd().name
    if Path(env_path).exists():
        console.print(
            "[bold yellow][!][/bold yellow] .env already exists. Skipping generation."
        )
        return False
    used = set()
    fp = find_open_port(used)
    bp = find_open_port(used)
    pp = find_open_port(used)

    with open(env_path, "w") as f:
        f.write(f"FRONTEND_PORT={fp}\n")
        f.write(f"BACKEND_PORT={bp}\n")
        f.write(f"PREVIEW_PORT={pp}\n")
        f.write("GITHUB_TOKEN=\n")
        f.write(f"GITHUB_REPO={repo_name}\n")
        f.write("GITHUB_BRANCH=main\n")
        f.write(f"VITE_API_BASE_URL=http://localhost:{bp}\n")
        f.write(f"VITE_DOCS_PREVIEW_BASE_URL=http://localhost:{pp}\n")
        f.write("VITE_ENVIRONMENT=production\n")
    return True


def init_project(target_dir=".", no_git=False, repo_name=None):
    check_prerequisites()
    target = Path(target_dir)
    if target.exists() and any(target.iterdir()):
        console.print(
            f"[bold cyan][?][/bold cyan] [bold]Directory {target} is not empty. Continue?[/bold] [dim](default: no)[/dim]",
            end=" ",
        )
        confirm = input().strip().lower()
        if confirm not in ("y", "yes"):
            console.print("[bold red][X] Aborting initialization.[/bold red]")
            return
    console.print(
        f"\n[bold cyan]Initializing DraftMk project in: [bold]{target.resolve()}[/bold][/bold cyan]"
    )
    (target / ".draftmk/config").mkdir(parents=True, exist_ok=True)

    # Create default mkdocs config files for internal and public
    internal_config = target / ".draftmk/config/mkdocs.internal.yml"
    public_config = target / ".draftmk/config/mkdocs.public.yml"

    base_config = """site_name: "Internal Documentation"
site_description: "Comprehensive internal & public documentation"
site_author: "Your Team"
site_url: "https://example.com/"
repo_name: "your-org/your-repo"
repo_url: "https://github.com/your-org/your-repo"
copyright: "© 2025 DraftMk"

docs_dir: /app/docs
#site_dir: /app/site/internal

theme:
  name: material
  #custom_dir: /app/overrides
  features:
    - navigation.instant
    - navigation.tabs
    - navigation.sections
    - navigation.indexes
    - navigation.top
    - navigation.tracking
    - toc.integrate
    - toc.follow
    - content.code.annotate
    - content.code.copy
    - content.tooltips
    - search.suggest
    - search.highlight
    - search.share
    - announce.dismiss
    - content.tabs.link
  palette:
    - scheme: default
      primary: blue
      accent: blue
      toggle:
        icon: material/weather-night
        name: Switch to dark mode
    - scheme: slate
      primary: blue
      accent: blue
      toggle:
        icon: material/weather-sunny
        name: Switch to light mode
  font:
    text: Roboto
    code: Roboto Mono

markdown_extensions:
  - abbr
  - admonition
  - attr_list
  - def_list
  - footnotes
  - md_in_html
  - toc:
      permalink: false
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.betterem:
      smart_enable: all
  - pymdownx.caret
  - pymdownx.details
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.keys
  - pymdownx.mark
  - pymdownx.smartsymbols
  - pymdownx.snippets
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - pymdownx.tilde

plugins:
  - search:
      lang: en
      separator: '[\\s\\-]+'
  - minify:
      minify_html: true
  - tags
  - redirects
  - role-filter:
      allowed_roles:
        - public
        - internal

extra:
  generator: false

#extra_css:
#  - assets/css/custom.css

#extra_javascript:
#  - assets/js/iframe-sync.js

nav:
- "Welcome": "index.md"
"""

    if not internal_config.exists():
        internal_config.write_text(base_config)
        console.print("[bold green][+][/bold green] Created mkdocs.internal.yml.")

    if not public_config.exists():
        public_config.write_text(
            base_config.replace("Internal Documentation", "Public Documentation")
            .replace(
                'site_url: "https://example.com/"',
                'site_url: "https://example.com/public"',
            )
            .replace("#site_dir: /app/site/internal", "#site_dir: /app/site/public")
            .replace("        - internal", "")
        )
        console.print("[bold green][+][/bold green] Created mkdocs.public.yml.")

    (target / ".draftmk/site/public").mkdir(parents=True, exist_ok=True)
    (target / ".draftmk/site/internal").mkdir(parents=True, exist_ok=True)
    (target / ".draftmk/logs").mkdir(parents=True, exist_ok=True)
    # Create docs/index.md with starter content
    docs_path = target / "docs"
    docs_path.mkdir(parents=True, exist_ok=True)
    index_file = docs_path / "index.md"
    if not index_file.exists():
        index_file.write_text(
            "---\ntitle: Welcome\nrole: public\n---\n\n# Welcome to MkDocs + DraftMk\n\nThis is your documentation homepage. Edit `docs/index.md` to get started.\n"
        )
        console.print(
            "[bold green][+][/bold green] Created docs/index.md with starter content."
        )
    if generate_env(target / ".env", repo_name=repo_name):
        console.print("[bold green][+][/bold green] .env file created.")
    console.print("[bold green][+][/bold green] Project directories initialized.")

    # Ask user if they want to initialize a git repo
    if not no_git and not (target / ".git").exists():
        console.print(
            "[bold cyan][?][/bold cyan] [bold]Would you like to initialize a Git repository?[/bold] [dim](default: yes)[/dim]",
            end=" ",
        )
        choice = input().strip().lower()
        if choice in ("", "y", "yes"):
            try:
                subprocess.run(
                    ["git", "init", "-b", "main"],
                    cwd=target,
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                if (target / ".git").exists():
                    console.print(
                        f"[bold green][+][/bold green] Git repository initialized on branch [bold cyan]'main'[/bold cyan]."
                    )
                else:
                    console.print(
                        f"[bold red][X][/bold red] Failed to initialize Git repository."
                    )
            except Exception as e:
                console.print(
                    f"[bold yellow][!][/bold yellow] Could not initialize Git repository: {e}"
                )

    # Download docker-compose.yml if it doesn't exist
    compose_url = "https://gist.githubusercontent.com/jonmatum/5175f2de585958b6466d7b328057f62c/raw/docker-compose.yml"
    compose_file = target / "docker-compose.yml"
    if not compose_file.exists():
        console.print(
            "[bold cyan]Downloading docker-compose.yml from GitHub Gist...[/bold cyan]"
        )
        try:
            urllib.request.urlretrieve(compose_url, compose_file)
            console.print("[bold green][+][/bold green] docker-compose.yml downloaded.")
        except Exception as e:
            console.print(
                f"[bold red][X] Failed to download docker-compose.yml: {e}[/bold red]"
            )


def preview(open_browser=False):
    check_prerequisites()

    print("\033c", end="")  # Clear terminal screen

    console.print("[bold cyan][?][/bold cyan] Pulling latest images...")
    subprocess.run(["docker-compose", "--env-file", ".env", "pull"])

    try:
        with open(".env") as f:
            lines = f.readlines()
        port = next(
            (
                line.split("=")[1].strip()
                for line in lines
                if line.startswith("FRONTEND_PORT=")
            ),
            "80",
        )
        url = f"http://localhost:{port}"
    except Exception:
        url = "http://localhost"

    console.print("\n[bold green][+][/bold green] DraftMk Preview is starting...")
    console.print(f"Access your frontend at: {url}")
    if open_browser:
        from webbrowser import open as open_url

        console.print("[bold cyan]Opening browser automatically...[/bold cyan]")
        open_url(url)

    console.print(
        "[bold cyan]Services are starting with logs below (press Ctrl+C to stop)[/bold cyan]\n"
    )

    subprocess.run(
        [
            "docker-compose",
            "--env-file",
            ".env",
            "up",
            "--build",
            "--remove-orphans",
            "--force-recreate",
        ]
    )


def view():
    check_prerequisites()
    if not os.path.exists(".env"):
        console.print(
            "[bold red][X] .env file not found. Please run 'draftmk init' or 'draftmk up' first.[/bold red]"
        )
        return
    try:
        from webbrowser import open as open_url

        with open(".env") as f:
            lines = f.readlines()
        port = next(
            (
                line.split("=")[1].strip()
                for line in lines
                if line.startswith("FRONTEND_PORT=")
            ),
            "80",
        )
        url = f"http://localhost:{port}"
        console.print(f"[bold cyan]Opening browser at {url}[/bold cyan]")
        open_url(url)
    except Exception as e:
        console.print(f"[bold yellow][!][/bold yellow] Failed to open browser: {e}")


def logs():
    log_path = ".draftmk/logs/draftmk.log"
    if not os.path.exists(log_path):
        console.print("[bold cyan]No log file found yet.[/bold cyan]")
        return
    console.print("[bold cyan]Showing last 50 lines from log:[/bold cyan]")
    subprocess.run(["tail", "-n", "50", log_path])


def stop():
    check_prerequisites()
    console.print("[bold cyan]Stopping DraftMk services...[/bold cyan]")
    subprocess.run(["docker-compose", "--env-file", ".env", "down"])


def up():
    if not Path(".env").exists():
        console.print("[bold yellow].env not found, running init...[/bold yellow]")
        init_project(no_git=True)
    preview(open_browser=True)


def status():
    check_prerequisites()
    console.print("[bold yellow]Checking DraftMk service status...\n[/bold yellow]")
    subprocess.run(["docker-compose", "--env-file", ".env", "ps"])


def check_latest_version():
    try:
        with urllib.request.urlopen(
            "https://pypi.org/pypi/draftmk/json", timeout=2
        ) as res:
            data = json.load(res)
            latest = data["info"]["version"]
            if latest != __version__:
                console.print(
                    f"\n[bold yellow][!][/bold yellow] A new version of draftmk is available: {latest} (you have {__version__})"
                )
                console.print(
                    "    [bold yellow]pip install --upgrade draftmk[/bold yellow]\n"
                )
    except Exception:
        pass  # Fail silently if no internet or PyPI unreachable


def main():
    check_latest_version()
    parser = argparse.ArgumentParser(
        description=(
            "DraftMk CLI — Automate and preview MkDocs documentation workflows with Docker.\n\n"
            "Examples:\n"
            "  draftmk init my-docs\n"
            "  draftmk init --no-git --repo <org>/<repo>\n"
            "  draftmk up\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser(
        "init",
        help="Initialize project (supports --no-git and --repo for CI)",
        description="Initialize project (supports --no-git and --repo for CI)",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    init_parser.add_argument("target", nargs="?", default=".", help="Target directory")
    # Group for init options
    group = init_parser.add_argument_group("init options")
    group.add_argument(
        "--no-git", action="store_true", help="Skip Git repository initialization"
    )
    group.add_argument(
        "--repo", metavar="REPO", help="Repository name for .env (overrides default)"
    )

    preview_parser = subparsers.add_parser(
        "preview", help="Start DraftMk services and follow logs"
    )
    preview_parser.add_argument(
        "--open", action="store_true", help="Open frontend in browser after start"
    )
    subparsers.add_parser("view", help="Open frontend preview in default browser")
    subparsers.add_parser("logs", help="Display latest logs from DraftMk services")
    subparsers.add_parser("stop", help="Stop all running DraftMk containers")
    subparsers.add_parser(
        "up", help="Start DraftMk environment (auto-runs init if needed)"
    )
    subparsers.add_parser("status", help="Show status of DraftMk containers")

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()

    if args.command == "init":
        target = args.target
        if target == ".":
            console.print(
                "[bold cyan][?][/bold cyan] [bold]Enter a project directory name:[/bold] [dim](default: draftmk-docs)[/dim]",
                end=" ",
            )
            target = input().strip() or "draftmk-docs"

        if not re.match(r"^[a-z]+(-[a-z]+)*$", target):
            console.print(
                "[bold red][X] Invalid project name. Use lowercase letters and hyphens only (e.g., draftmk-docs).[/bold red]"
            )
            return

        init_project(target, no_git=args.no_git, repo_name=args.repo)
        console.print(
            f"\n[bold blue]Hint:[/bold blue] Run [bold cyan]cd {target}[/bold cyan] then [bold cyan]draftmk up[/bold cyan] to get started."
        )
    elif args.command == "preview":
        preview(open_browser=args.open)
    elif args.command == "view":
        view()
    elif args.command == "logs":
        logs()
    elif args.command == "stop":
        stop()
    elif args.command == "up":
        up()
    elif args.command == "status":
        status()
    else:
        parser.print_help()
        console.print(
            "\n[bold blue]Hint:[/bold blue] Run [bold cyan]draftmk init[/bold cyan] to begin a new project."
        )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(
            "\n[bold yellow][!][/bold yellow] Interrupted by user. Exiting cleanly..."
        )
        sys.exit(0)
