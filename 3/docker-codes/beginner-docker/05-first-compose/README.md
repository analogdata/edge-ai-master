# 05 — First Docker Compose

The simplest possible `docker-compose.yml` — just one service.

## What is Docker Compose?

Instead of typing long `docker run` commands with many flags, you describe
everything in a YAML file and start it all with one command.

**Without Compose:**
```bash
docker run -d --name my-app --restart always -e GREETING="Hello!" my-image
```

**With Compose:**
```bash
docker compose up -d
```
All the settings live in `docker-compose.yml` — version controlled, readable,
and repeatable.

## Try It

```bash
# Start in the foreground (see logs directly)
docker compose up

# OR start in the background (detached)
docker compose up -d

# Check the status
docker compose ps

# View logs
docker compose logs

# Watch logs live
docker compose logs -f

# Stop and remove the container
docker compose down
```

## docker-compose.yml Structure

```
version: "3.9"       ← Compose file format version

services:            ← Define your containers here
  myapp:             ← Service name (becomes the hostname)
    build: .         ← Build from Dockerfile in current directory
    container_name:  ← Fixed name for the container
    restart: always  ← Auto-restart on crash
    environment:     ← Environment variables
      - GREETING=...
```
