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
draftmk init [<directory>] [--no-git] [--repo <repository-url>] [--force] [--force-git] [--template <path-or-url>]
```

- Initializes `.draftmk` structure and `.env` file with dynamic ports
- Uses Copier to scaffold (internal or custom template via `--template`)
- Only initializes Git if not skipped with `--no-git`, or forced via `--force-git`
- Uses `--force` to bypass directory emptiness check
- `--yes` is deprecated and replaced with `--force`

You can override the default internal Copier template with `--template`, or configure one in `.draftmk/settings.json`.

### `up`

Initializes the project (if needed), pulls images, builds containers, and opens the browser.

```bash
draftmk up
```

- `--no-browser`: Do not open the frontend automatically

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

- `--print`: Only print the preview URL instead of launching the browser

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

```
.
├── .draftmk/
│   ├── config/
│   │   ├── mkdocs.internal.yml
│   │   └── mkdocs.public.yml
│   ├── site/
│   │   ├── public/
│   │   └── internal/
│   ├── logs/
│   │   └── draftmk.log
│   └── settings.json  # optional template override
├── docs/
│   └── index.md
├── .env
├── docker-compose.yml
```

## Docker Images

DraftMk uses pre-built Docker images hosted on Docker Hub:

- **Backend**: [`jonmatum/draftmk-backend`](https://hub.docker.com/r/jonmatum/draftmk-backend)
- **Frontend**: [`jonmatum/draftmk-frontend`](https://hub.docker.com/r/jonmatum/draftmk-frontend)
- **Preview**: [`jonmatum/draftmk-preview`](https://hub.docker.com/r/jonmatum/draftmk-preview)

## Docker Compose Template

DraftMk no longer downloads a remote `docker-compose.yml` from a GitHub Gist.

Instead, the file is scaffolded using Copier templates (either internal or from a configured template repo).

## Copier Template Support

DraftMk scaffolds projects using [Copier](https://copier.readthedocs.io/) during `draftmk init`. To override the template, pass `--template` or define `.draftmk/settings.json`.

```json
{
  "template_repo": "gh:your-org/your-template-repo"
}
```

This enables full customization of how your documentation project is initialized.

- Copier variables supported include:
  ```yaml
  project_name: "Your Docs"
  repo_name: "your-org/your-repo"
  site_url: "https://example.com"
  vite_env: "production"
  ```
- DraftMk pre-fills dynamic ports and environment for the template using Copier's data injection.

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
