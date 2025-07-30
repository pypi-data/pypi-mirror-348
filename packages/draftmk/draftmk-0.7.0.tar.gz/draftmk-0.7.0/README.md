# draftmk

`draftmk` is an advanced command-line tool that automates the setup, management, and deployment of MkDocs-based documentation projects using Docker. It streamlines local previews, environment initialization, live editing, and supports CI/CD automation with flexible repository integration and configuration scaffolding for both public and internal documentation views.

## Features

- One-command environment bootstrap with optional Git initialization
- CI-friendly flags: `--no-git` to skip Git setup, `--repo` to link existing repositories
- Automatic port assignment (avoids conflicts)
- Auto-generation of `docs/index.md`, `mkdocs.public.yml`, and `mkdocs.internal.yml` scaffolding
- Colorful CLI output for improved user experience
- Automatic Docker Compose setup via GitHub Gist download
- Friendly preview logs and automatic browser launching
- Supports seamless integration into CI pipelines

## Installation

Install from PyPI:

```bash
pip install draftmk
```

Or add to a Poetry project:

```bash
poetry add draftmk
```

> Requires Python ≥ 3.9, Docker, and Docker Compose.

## Commands

### `init`

Bootstraps a new DraftMk project.

```bash
draftmk init [--dir <directory>] [--no-git] [--repo <repository-url>]
```

- Prompts for a directory name (defaults to `draftmk-docs` if not specified)
- Creates `.draftmk/` structure and `.env` with available ports
- Generates default `docs/index.md`, `mkdocs.public.yml`, and `mkdocs.internal.yml` files for scaffolding
- Downloads `docker-compose.yml` from a GitHub Gist
- Optionally initializes a Git repository on the `main` branch unless `--no-git` is specified
- If `--repo` is provided, links the project to the existing Git repository

### `up`

Initializes the project (if needed), pulls images, builds containers, and opens the browser.

```bash
draftmk up
```

### `preview`

Starts the full environment and shows Docker logs.

```bash
draftmk preview --open
```

- `--open`: Launches the frontend in your default browser

### `view`

Launches the frontend in your browser using the port defined in `.env`.

```bash
draftmk view
```

### `logs`

Tails the last 50 lines of the `.draftmk/logs/draftmk.log` file.

```bash
draftmk logs
```

### `stop`

Stops all DraftMk-related Docker containers.

```bash
draftmk stop
```

### `status`

Shows the running status of all containers.

```bash
draftmk status
```

## Usage Examples for CI Automation

To bootstrap a project without Git initialization (useful in CI pipelines):

```bash
draftmk init --no-git
```

To bootstrap and link to an existing repository:

```bash
draftmk init --repo yourusername/yourrepo
```

## Directory Structure

After running `draftmk init`, you will have:

```
.
├── .draftmk/
│   ├── config/
│   ├── site/
│   │   ├── public/
│   │   └── internal/
│   └── logs/
├── docs/
│   └── index.md
├── mkdocs.public.yml
├── mkdocs.internal.yml
├── .env
└── docker-compose.yml
```

## Docker Images

DraftMk uses pre-built Docker images hosted on Docker Hub:

- **Backend**: [`jonmatum/draftmk-backend`](https://hub.docker.com/r/jonmatum/draftmk-backend)
- **Frontend**: [`jonmatum/draftmk-frontend`](https://hub.docker.com/r/jonmatum/draftmk-frontend)
- **Preview**: [`jonmatum/draftmk-preview`](https://hub.docker.com/r/jonmatum/draftmk-preview)

## Docker Compose Template

The CLI downloads a `docker-compose.yml` template from the following GitHub Gist:

- [https://gist.github.com/jonmatum/5175f2de585958b6466d7b328057f62c](https://gist.github.com/jonmatum/5175f2de585958b6466d7b328057f62c)

## Copier Template Support

DraftMk supports project scaffolding using [Copier](https://copier.readthedocs.io/). You can generate a new documentation project structure using:

```bash
draftmk scaffold
```

By default, this pulls from the official template:

- [gh:jonmatum/draftmk-template](https://github.com/jonmatum/draftmk-template)

To use a custom template, create a `.draftmk/settings.json` file in your project root with the following content:

```json
{
  "template_repo": "gh:your-org/your-template-repo"
}
```

This enables full customization of how your documentation project is initialized.

## Requirements

- Python ≥ 3.9
- Docker
- Docker Compose

## License

MIT © [Jonatan Mata](https://jonmatum.dev)

---

```bash
echo "Pura Vida & Happy Coding!";
```
