#!/usr/bin/env python3
import argparse
import os
import random
import re
import shutil
import socket
import subprocess
import time
import urllib.request
from pathlib import Path

from rich.console import Console

console = Console()


def check_prerequisites():
    required = ["docker", "docker-compose"]
    for cmd in required:
        if not shutil.which(cmd):
            console.print(
                f"[bold red]✖ Required command '{cmd}' not found. Please install it and try again.[/bold red]"
            )
            exit(1)


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


def generate_env(env_path):
    used = set()
    fp = find_open_port(used)
    bp = find_open_port(used)
    pp = find_open_port(used)

    with open(env_path, "w") as f:
        f.write(f"FRONTEND_PORT={fp}\n")
        f.write(f"BACKEND_PORT={bp}\n")
        f.write(f"PREVIEW_PORT={pp}\n")
        f.write("GITHUB_TOKEN=\n")
        f.write("GITHUB_REPO=draftmk-template\n")
        f.write("GITHUB_BRANCH=main\n")
        f.write(f"VITE_API_BASE_URL=http://localhost:{bp}\n")
        f.write(f"VITE_DOCS_PREVIEW_BASE_URL=http://localhost:{pp}\n")
        f.write("VITE_ENVIRONMENT=production\n")


def init_project(target_dir="."):
    check_prerequisites()
    target = Path(target_dir)
    console.print(
        f"\n[bold cyan]Initializing DraftMk project in:[/bold cyan] [bold]{target.resolve()}[/bold]"
    )
    (target / ".draftmk/config").mkdir(parents=True, exist_ok=True)
    (target / ".draftmk/site/public").mkdir(parents=True, exist_ok=True)
    (target / ".draftmk/site/internal").mkdir(parents=True, exist_ok=True)
    (target / ".draftmk/logs").mkdir(parents=True, exist_ok=True)
    generate_env(target / ".env")
    console.print("[green]✔ .env file created.[/green]")
    console.print("[green]✔ Project directories initialized.[/green]")

    # Ask user if they want to initialize a git repo
    if not (target / ".git").exists():
        choice = (
            input("Would you like to initialize a Git repository? [Y/n]: ")
            .strip()
            .lower()
        )
        if choice in ("", "y", "yes"):
            try:
                subprocess.run(["git", "init", "-b", "main"], cwd=target, check=True)
                console.print(
                    "[green]✔ Git repository initialized on branch 'main'.[/green]"
                )
            except Exception as e:
                console.print(
                    f"[bold yellow]Could not initialize Git repository: {e}[/bold yellow]"
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
            console.print("[green]✔ docker-compose.yml downloaded.[/green]")
        except Exception as e:
            console.print(
                f"[bold red]✖ Failed to download docker-compose.yml: {e}[/bold red]"
            )


def preview(open_browser=False):
    check_prerequisites()

    print("\033c", end="")  # Clear terminal screen

    console.print("[bold cyan]Pulling latest images...[/bold cyan]")
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

    console.print("\nDraftMk Preview is starting...")
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
            "[bold red]✖ .env file not found. Please run 'draftmk init' or 'draftmk up' first.[/bold red]"
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
        console.print(f"[bold yellow]Failed to open browser: {e}[/bold yellow]")


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
        console.print("[bold cyan].env not found, running init...[/bold cyan]")
        init_project()
    preview(open_browser=True)


def status():
    check_prerequisites()
    console.print("[bold cyan]Checking DraftMk service status...\n[/bold cyan]")
    subprocess.run(["docker-compose", "--env-file", ".env", "ps"])


def main():
    parser = argparse.ArgumentParser(description="Draftmk CLI")
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Initialize Draftmk project")
    init_parser.add_argument("target", nargs="?", default=".", help="Target directory")

    preview_parser = subparsers.add_parser(
        "preview", help="Start Docker Compose preview"
    )
    preview_parser.add_argument(
        "--open", action="store_true", help="Open frontend in browser after start"
    )
    subparsers.add_parser("view", help="Open frontend in browser")
    subparsers.add_parser("logs", help="Show recent logs")
    subparsers.add_parser("stop", help="Stop Docker services")
    subparsers.add_parser(
        "up", help="Start Draftmk environment (init + preview + open)"
    )
    subparsers.add_parser("status", help="Show status of Draftmk services")

    args = parser.parse_args()

    if args.command == "init":
        target = args.target
        if target == ".":
            target = (
                input(
                    "> Enter a project directory name (e.g., my-docs) [default: draftmk-docs]: "
                ).strip()
                or "draftmk-docs"
            )

        if not re.match(r"^[a-z]+(-[a-z]+)*$", target):
            console.print(
                "[bold red]✖ Invalid project name. Use lowercase letters and hyphens only (e.g., draftmk-docs).[/bold red]"
            )
            return

        init_project(target)
        console.print(f"\n[bold green]To get started:[/bold green]")
        console.print(f"[cyan]  cd {target}[/cyan]")
        console.print(f"[cyan]  draftmk up[/cyan]")
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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(
            "\n[bold yellow]Interrupted by user. Exiting cleanly...[/bold yellow]"
        )
        exit(0)
