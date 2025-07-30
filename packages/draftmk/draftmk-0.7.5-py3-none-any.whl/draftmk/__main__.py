#!/usr/bin/env python3
import argparse
import json
import logging
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

import psutil
from copier import run_copy
from rich.console import Console

from draftmk.exceptions import MissingDependencyError
from draftmk.version import __version__

console = Console()

logger = logging.getLogger(__name__)

# Default Copier template repo for scaffolding
DEFAULT_TEMPLATE_REPO = "gh:jonmatum/draftmk-template"


# Get template repo from .draftmk/settings.json or fallback to default
def get_template_repo():
    settings_path = Path(".draftmk/settings.json")
    if settings_path.exists():
        try:
            with open(settings_path) as f:
                settings = json.load(f)
            return settings.get("template_repo", DEFAULT_TEMPLATE_REPO)
        except Exception as e:
            console.print(
                f"[bold yellow][!][/bold yellow] Failed to read settings.json: {e}"
            )
    return DEFAULT_TEMPLATE_REPO


from importlib.resources import files


def _scaffold(template=None, quiet=False, dst_path=Path.cwd()):
    try:
        # Ensure target directory is created early to support logging
        dst_path.mkdir(parents=True, exist_ok=True)
        # Setup logging to the target .draftmk/logs/draftmk.log
        log_dir = dst_path / ".draftmk/logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "draftmk.log"
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
        )
        logger.info(f"Scaffolding DraftMk project to: {dst_path.resolve()}")
        # Determine template source based on new priority
        if template:
            template_source = template
            template_origin = "explicit"
        else:
            # Check if settings file defines a custom remote template
            configured_template = get_template_repo()
            if configured_template != DEFAULT_TEMPLATE_REPO:
                template_source = configured_template
                template_origin = "settings"
            else:
                # Use internal package template via importlib.resources
                try:
                    import draftmk.templates

                    template_source = files("draftmk.templates")
                    template_origin = "internal"
                except ModuleNotFoundError:
                    console.print(
                        "[bold red][X] Internal templates are missing. Cannot scaffold.[/bold red]"
                    )
                    return

        # Check that template_source is not None before running copier
        if not template_source:
            console.print("[bold red][X] No valid Copier template found.[/bold red]")
            return

        # Check if the template_source is a valid directory when using internal template
        if template_origin == "internal":
            # template_source may be a Traversable; check with str(template_source)
            if not Path(str(template_source)).is_dir():
                console.print(
                    "[bold red][X] Internal Copier template path is not a valid directory.[/bold red]"
                )
                return
            console.print(
                f"[bold cyan]Scaffolding using internal template:[/bold cyan] {template_source}"
            )
        elif template_origin == "explicit":
            console.print(
                f"[bold cyan]Scaffolding using specified template:[/bold cyan] {template_source}"
            )
        else:
            console.print(
                f"[bold cyan]Scaffolding using remote template:[/bold cyan] {template_source}"
            )
        # Discover ports before copying
        used = set()
        frontend_port = find_open_port(used)
        backend_port = find_open_port(used)
        preview_port = find_open_port(used)

        run_copy(
            src_path=str(template_source),
            dst_path=dst_path,
            quiet=True,
            defaults=False,
            data={
                "project_name": "DraftMk Docs",
                "repo_name": "your-org/your-repo",
                "site_url": "https://example.com",
                "vite_env": "production",
                "frontend_port": frontend_port,
                "backend_port": backend_port,
                "preview_port": preview_port,
                "ask_for_ssh": True,
            },
        )
        # Ensure .draftmk subdirectories exist if not created by Copier template
        subdirs = [
            ".draftmk/config",
            ".draftmk/logs",
            ".draftmk/site/public",
            ".draftmk/site/internal",
        ]
        for subdir in subdirs:
            path = dst_path / subdir
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        console.print(f"[bold red][X] Failed to scaffold project: {e}[/bold red]")


def check_prerequisites():
    required = ["docker", "docker-compose"]
    for cmd in required:
        if not shutil.which(cmd):
            logger.error(f"Missing required command: {cmd}")
            raise MissingDependencyError(f"Required command '{cmd}' not found.")


def find_open_port(used_ports, start=3000, end=3999):
    try:
        busy_ports = {
            conn.laddr.port
            for conn in psutil.net_connections(kind="inet")
            if conn.status == psutil.CONN_LISTEN
        }
    except (psutil.AccessDenied, psutil.ZombieProcess) as e:
        console.print(
            "[bold yellow][!][/bold yellow] Could not inspect open ports due to permission limits. Falling back to socket scan."
        )
        busy_ports = set()

    for _ in range(1000):  # prevent infinite loop
        port = random.randint(start, end)
        if port in used_ports or port in busy_ports:
            continue
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("localhost", port))
                used_ports.add(port)
                return port
        except OSError:
            continue

    raise RuntimeError("Could not find an open port in the given range.")


def generate_env(env_path, repo_name=None):
    """
    Generate a .env file if it does not exist.
    If Copier has already written the .env file (with ports), skip generation.
    Otherwise, generate ports and write defaults.
    """
    if Path(env_path).exists():
        console.print(
            "[bold yellow][!][/bold yellow] .env already exists. Skipping generation."
        )
        return False

    # Check if port values are already set in the environment, otherwise generate them
    used = set()
    fp = int(os.environ.get("FRONTEND_PORT", find_open_port(used)))
    bp = int(os.environ.get("BACKEND_PORT", find_open_port(used)))
    pp = int(os.environ.get("PREVIEW_PORT", find_open_port(used)))

    # Write .env file with these values (as a fallback if Copier did not handle it)
    with open(env_path, "w") as f:
        f.write(f"FRONTEND_PORT={fp}\n")
        f.write(f"BACKEND_PORT={bp}\n")
        f.write(f"PREVIEW_PORT={pp}\n")
        f.write("GITHUB_TOKEN=\n")
        f.write(f"GITHUB_REPO={repo_name or 'your-org/your-repo'}\n")
        f.write("GITHUB_BRANCH=main\n")
        f.write(f"VITE_API_BASE_URL=http://localhost:{bp}\n")
        f.write(f"VITE_DOCS_PREVIEW_BASE_URL=http://localhost:{pp}\n")
        f.write("VITE_ENVIRONMENT=production\n")
    logger.info(f".env file generated at: {env_path}")
    return True


def init_project(
    target_dir=".",
    no_git=False,
    repo_name=None,
    force=False,
    force_git=False,
    template=None,
):
    check_prerequisites()
    target = Path(target_dir)
    # Check directory emptiness before scaffolding
    if target.exists():
        non_hidden_files = [
            p
            for p in target.iterdir()
            if not p.name.startswith(".") and p.name != "draftmk.log"
        ]
        if non_hidden_files and not force:
            console.print(
                f"[bold cyan][?][/bold cyan] [bold]Directory {target.resolve()} is not empty. Use --force to continue.[/bold]"
            )
            return
    # Scaffold project if .draftmk directory does not exist
    if not (target / ".draftmk").exists():
        _scaffold(template=template, dst_path=target, quiet=force)
    console.print(
        f"\n[bold cyan]Initializing DraftMk project in: [bold]{target.resolve()}[/bold][/bold cyan]"
    )
    logger.info(f"Initializing DraftMk project in: {target.resolve()}")

    # If scaffold already created config files, docs, or .env, do not overwrite
    internal_config = target / ".draftmk/config/mkdocs.internal.yml"
    public_config = target / ".draftmk/config/mkdocs.public.yml"
    docs_path = target / "docs"
    index_file = docs_path / "index.md"

    # Skip config creation if scaffold already created them
    if internal_config.exists():
        logger.info("mkdocs.internal.yml already exists. Skipping.")
    if public_config.exists():
        logger.info("mkdocs.public.yml already exists. Skipping.")

    # Only create docs directory if it doesn't exist (Copier may have created index.md)
    docs_path.mkdir(parents=True, exist_ok=True)

    # Only create .env if it doesn't exist
    env_path = target / ".env"
    if not env_path.exists():
        if generate_env(env_path, repo_name=repo_name):
            console.print("[bold green][+][/bold green] .env file created (fallback).")
    console.print("[bold green][+][/bold green] Project directories initialized.")

    # Decide on Git initialization logic
    git_should_init = False
    if not no_git:
        if force:
            git_should_init = True
        elif force_git or not (target / ".git").exists():
            # Prompt user
            console.print(
                "[bold cyan][?][/bold cyan] [bold]Would you like to initialize a Git repository?[/bold] [dim](default: yes)[/dim]",
                end=" ",
            )
            choice = input().strip().lower()
            if choice in ("", "y", "yes"):
                git_should_init = True
    if git_should_init:
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


def preview(open_browser=False):
    check_prerequisites()

    print("\033c", end="")  # Clear terminal screen

    console.print("[bold cyan][?][/bold cyan] Pulling latest images...")
    try:
        subprocess.run(["docker-compose", "--env-file", ".env", "pull"], check=True)
        logger.info("Docker images pulled successfully.")
    except subprocess.CalledProcessError:
        console.print("[bold red][X] Failed to pull Docker images.[/bold red]")
        return

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

    try:
        subprocess.run(
            [
                "docker-compose",
                "--env-file",
                ".env",
                "up",
                "--build",
                "--remove-orphans",
                "--force-recreate",
            ],
            check=True,
        )
    except subprocess.CalledProcessError:
        console.print("[bold red][X] Failed to start DraftMk services.[/bold red]")


def view(print_only=False):
    check_prerequisites()
    if not os.path.exists(".env"):
        console.print(
            "[bold red][X] .env file not found. Please run 'draftmk init' or 'draftmk up' first.[/bold red]"
        )
        return
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
        if print_only:
            console.print(f"[bold green]Frontend URL:[/bold green] {url}")
        else:
            from webbrowser import open as open_url

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
    try:
        subprocess.run(["docker-compose", "--env-file", ".env", "down"], check=True)
        logger.info("DraftMk services stopped.")
    except subprocess.CalledProcessError:
        console.print("[bold red][X] Failed to stop DraftMk services.[/bold red]")


def up(open_browser=True):
    if not Path(".env").exists():
        console.print("[bold yellow].env not found, running init...[/bold yellow]")
        init_project(no_git=True)
    preview(open_browser=open_browser)


def status():
    check_prerequisites()
    console.print("[bold yellow]Checking DraftMk service status...\n[/bold yellow]")
    try:
        subprocess.run(["docker-compose", "--env-file", ".env", "ps"], check=True)
    except subprocess.CalledProcessError:
        console.print("[bold red][X] Failed to check service status.[/bold red]")


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


def valid_project_name(name):
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
        raise argparse.ArgumentTypeError(
            "Invalid project name. Use lowercase letters, numbers, and hyphens only (e.g., draftmk-docs123)."
        )
    return name


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
    init_parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target directory",
    )
    # Group for init options
    group = init_parser.add_argument_group("init options")
    group.add_argument(
        "--no-git", action="store_true", help="Skip Git repository initialization"
    )
    group.add_argument(
        "--repo", metavar="REPO", help="Repository name for .env (e.g. org/repo)"
    )
    group.add_argument(
        "--force",
        action="store_true",
        help="Continue in non-empty directories without prompting",
    )
    group.add_argument(
        "--force-git",
        action="store_true",
        help="Initialize Git even if a .git directory exists",
    )
    group.add_argument(
        "--template",
        metavar="TEMPLATE",
        help="Copier template repo or path to use (e.g. gh:org/template or ./local-dir)",
    )

    preview_parser = subparsers.add_parser(
        "preview", help="Start DraftMk services and follow logs"
    )
    preview_parser.add_argument(
        "--open", action="store_true", help="Open the frontend in a browser after start"
    )
    view_parser = subparsers.add_parser(
        "view", help="Open frontend preview in default browser"
    )
    view_parser.add_argument(
        "--print",
        dest="print_only",
        action="store_true",
        help="Only print the frontend URL instead of opening it",
    )
    subparsers.add_parser("logs", help="Display latest logs from DraftMk services")
    subparsers.add_parser("stop", help="Stop all running DraftMk containers")
    up_parser = subparsers.add_parser(
        "up", help="Start DraftMk environment (auto-runs init if needed)"
    )
    up_parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not open the frontend in a browser after starting services",
    )
    subparsers.add_parser("status", help="Show status of DraftMk containers")

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        console.print(
            "\n[bold blue]Hint:[/bold blue] Run [bold cyan]draftmk init[/bold cyan] to begin a new project."
        )
        sys.exit(0)
    try:
        if args.command == "init":
            target = args.target
            if target == ".":
                console.print(
                    "[bold cyan][?][/bold cyan] [bold]Enter a project directory name:[/bold] [dim](default: draftmk-docs)[/dim]",
                    end=" ",
                )
                target = input().strip() or "draftmk-docs"
            try:
                valid_project_name(target)
            except argparse.ArgumentTypeError as e:
                console.print(f"[bold red][X] {e}[/bold red]")
                sys.exit(1)
            if not args.repo:
                args.repo = target
            init_project(
                Path.cwd() / target,
                no_git=args.no_git,
                repo_name=args.repo,
                force=args.force,
                force_git=args.force_git,
                template=args.template,
            )
            console.print(
                f"\n[bold blue]Hint:[/bold blue] Run [bold cyan]cd {target}[/bold cyan] then [bold cyan]draftmk up[/bold cyan] to get started."
            )
        elif args.command == "preview":
            preview(open_browser=args.open)
        elif args.command == "view":
            view(print_only=args.print_only)
        elif args.command == "logs":
            logs()
        elif args.command == "stop":
            stop()
        elif args.command == "up":
            up(open_browser=not args.no_browser)
        elif args.command == "status":
            status()
    except MissingDependencyError as e:
        console.print(f"[bold red][X] {e}[/bold red]")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[bold yellow][!][/bold yellow] Interrupted by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
