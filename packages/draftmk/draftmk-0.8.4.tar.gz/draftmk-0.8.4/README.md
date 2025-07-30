# draftmk

`draftmk` is an advanced command-line tool that automates the setup, management, and deployment of MkDocs-based documentation projects using Docker. It streamlines local previews, live editing, and environment setup. It also supports CI/CD automation with flexible repository integration and configuration scaffolding for both public and internal documentation views.

## Features

- One-command environment bootstrap with optional Git initialization
- CI-friendly flags: `--no-git` to skip Git setup, `--repo` to link existing repositories
- Automatic port assignment (avoids conflicts)
- Auto-generation of `docs/index.md` and configuration scaffolding
- Colorful CLI output for improved user experience
- Docker Compose configuration scaffolded from templates
- Friendly preview logs and automatic browser launching
- Supports seamless integration into CI pipelines
- Supports remote Copier templates

## Quick Start

```bash
draftmk init my-docs
cd my-docs
draftmk up
```

Make sure Docker and Python ≥ 3.9 are installed.

This scaffolds your project, starts Docker services, and opens the frontend in your browser. Edit content in `docs/index.md` and see it live instantly!

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

If no directory is passed, you'll be prompted to enter one. Default is `draftmk-docs`.

- If no `<directory>` is given, user is prompted (default is `draftmk-docs`)
- `--repo` defaults to the directory name
- Initializes `.draftmk` structure and `.env` file with dynamic ports
- See [Git Initialization Logic](#git-initialization-logic)
- See [Project Scaffolding with Copier](#project-scaffolding-with-copier)
- Uses `--force` to bypass directory emptiness check
- `--yes` is deprecated and replaced with `--force`

You can override the default Copier template with `--template`.
See [Project Scaffolding with Copier](#project-scaffolding-with-copier).

### `up`

Initializes the project (if needed), pulls images, builds containers, and opens the browser.

```bash
draftmk up
```

- Runs `init` automatically if `.env` is missing
- `--no-browser`: Do not open the frontend automatically

### `preview`

Starts the full environment and shows Docker logs.

```bash
draftmk preview --open
```

- Assumes project is already initialized
- `--open`: Launches the frontend in your default browser

### `view`

Launches the frontend in your browser using the port defined in `.env`.

```bash
draftmk view
```

- `--print`: Only print the preview URL instead of launching the browser
- `--print` will only show the frontend URL

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

## .env Handling and Port Assignment

When initializing, `draftmk` provides dynamic ports for the frontend, backend, and preview services (unless set via environment variables) to the Copier template, which is responsible for generating the `.env` file.

To regenerate `.env`, delete it and rerun `draftmk init`. The actual content and structure of `.env` is determined by the Copier template in use.

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
├── docs/
│   └── index.md
├── .env
├── docker-compose.yml
```

## Git Initialization Logic

- `--no-git`: Skip Git setup entirely
- `--force-git`: Force Git init even if `.git` exists
- If neither flag is set:
  - CLI prompts user interactively (default is yes)
  - Initializes on `main` branch

## Usage Examples for CI Automation

To bootstrap a project without Git initialization (useful in CI pipelines):

```bash
draftmk init --no-git
```

To bootstrap and link to an existing repository:

```bash
draftmk init --repo yourusername/yourrepo
```

## Docker Images

DraftMk uses pre-built Docker images hosted on Docker Hub:

- **Backend**: [`jonmatum/draftmk-backend`](https://hub.docker.com/r/jonmatum/draftmk-backend)
- **Frontend**: [`jonmatum/draftmk-frontend`](https://hub.docker.com/r/jonmatum/draftmk-frontend)
- **Preview**: [`jonmatum/draftmk-preview`](https://hub.docker.com/r/jonmatum/draftmk-preview)

## Project Scaffolding with Copier

DraftMk scaffolds projects using [Copier](https://copier.readthedocs.io/) during `draftmk init`. The default template is [`gh:jonmatum/draftmk-copier-templates`](https://github.com/jonmatum/draftmk-copier-templates).

To override the template, pass `--template` with a Copier-compatible repo or path.

This enables full customization of how your documentation project is initialized.

- Copier variables supported include:
  ```yaml
  project_name: "Your Docs"
  repo_name: "your-org/your-repo"
  site_url: "https://example.com"
  vite_env: "production"
  ```
- DraftMk pre-fills dynamic ports and environment for the template using Copier's data injection.

DraftMk no longer downloads a remote `docker-compose.yml` from a GitHub Gist.

Instead, all files are scaffolded using the Copier template you specify (or the default).

## Requirements

- Python ≥ 3.9
- Docker
- Docker Compose

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
├── docs/
│   └── index.md
├── .env
├── docker-compose.yml
```

## Template Source

As of the latest version, DraftMk exclusively uses the [public Copier template repository](https://github.com/jonmatum/draftmk-copier-templates) for project scaffolding by default.

- Internal templates have been removed
- Custom templates can still be provided via `--template`
- Default behavior uses: `gh:jonmatum/draftmk-copier-templates`

## License

MIT © [Jonatan Mata](https://jonmatum.dev)

---

```bash
echo "Pura Vida & Happy Coding!";
```
