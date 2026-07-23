# 07 — Compose with Volumes (Persistence)

Demonstrates how Docker volumes preserve data across container restarts.

## What You'll Learn

- **Named volumes**: Docker-managed storage that persists across restarts
- **Bind mounts**: Map a host directory directly into the container
- The difference between `docker compose down` and `docker compose down -v`

## Two Types of Volumes

### Named Volume (Docker-managed)
```yaml
volumes:
  - my_data:/data    # Docker stores this somewhere on disk
```
- Docker manages where the data lives
- Data survives `docker compose down` (containers removed, data kept)
- Only `docker compose down -v` deletes the volume

### Bind Mount (Host directory)
```yaml
volumes:
  - ./config:/config  # Maps ./config on your host to /config in container
```
- You control where the data lives (a specific directory on your host)
- Changes on either side are immediately visible
- Great for development: edit on host, container sees changes instantly

## Try It

```bash
# Start the app
docker compose up -d

# Watch the counter increment
docker compose logs -f

# Stop and remove the container (volume data is KEPT)
docker compose down

# Start again — the counter CONTINUES from where it left off!
docker compose up -d
docker compose logs -f

# When you're done and want to DELETE the data too:
docker compose down -v

# List all Docker volumes on your system
docker volume ls
```

## Why This Matters

Containers are **ephemeral** (temporary). When a container is removed,
all files created inside it are lost. Volumes solve this:

```
Without volume:                With volume:
  Container starts → count=0     Container starts → reads count from volume
  Count goes 1, 2, 3...          Count continues 101, 102, 103...
  Container stops                 Container stops
  Container restarts → count=0   Container restarts → reads count from volume
  (data is LOST)                  Count continues 104, 105... (data PERSISTED)
```
