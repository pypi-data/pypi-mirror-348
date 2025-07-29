# draftmk

`draftmk` is a command-line tool that helps developers preview and manage DraftMk-based documentation environments locally using Docker and MkDocs.

It streamlines environment setup, port configuration, container orchestration, and browser preview, all with minimal configuration.

## Installation

Install from PyPI:

```bash
pip install draftmk
```

Or add it to your Python project with Poetry:

```bash
poetry add draftmk
```

## Commands

```bash
draftmk [command] [--options]
```

### `init`

Initializes the environment:

- Creates required `.draftmk` directories
- Generates a `.env` file with non-conflicting ports
- Downloads a default `docker-compose.yml` from GitHub Gist

```bash
draftmk init
```

### `up`

Runs `init` if needed, then launches the preview stack and opens the browser.

```bash
draftmk up
```

### `preview`

Starts the DraftMk Docker services and streams logs to the terminal.

```bash
draftmk preview --open
```

- `--open`: Opens the frontend in the default browser

### `view`

Opens the frontend in the default browser (reads the port from `.env`).

```bash
draftmk view
```

### `logs`

Displays the last 50 lines from the `.draftmk/logs/draftmk.log` file.

```bash
draftmk logs
```

### `stop`

Stops all running DraftMk Docker containers.

```bash
draftmk stop
```

### `status`

Displays the status of all services managed by DraftMk.

```bash
draftmk status
```

## Requirements

- Python 3.6 or higher
- Docker
- Docker Compose

## Directory Structure

After initialization, the project structure will look like this:

```
.draftmk/
├── config/
├── site/
│   ├── public/
│   └── internal/
├── logs/
.env
docker-compose.yml
```

## License

MIT © [Jonmatum](https://github.com/jonmatum)

---

> echo "Pura Vida & Happy Coding!";
