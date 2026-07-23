# 06 — Two Service Compose (Producer + Consumer)

Two services that share data through a Docker named volume.

## What You'll Learn

- How to define **multiple services** in one `docker-compose.yml`
- How `depends_on` controls startup order
- How **named volumes** let two containers share files
- How each service can have its own Dockerfile in a subdirectory

## Architecture

```
┌─────────────┐         ┌─────────────────┐         ┌─────────────┐
│   producer   │ ──────▶ │  sensor_data    │ ◀────── │   consumer   │
│  (generates  │         │  (named volume) │         │   (reads     │
│   readings)  │  write   │  /shared/       │  read   │   readings)  │
└─────────────┘         │  data.json      │         └─────────────┘
                        └─────────────────┘
```

## Try It

```bash
# Start both services in the foreground (see both logs interleaved)
docker compose up

# OR start in the background
docker compose up -d

# Watch logs from both services
docker compose logs -f

# Watch only the producer's logs
docker compose logs -f producer

# Watch only the consumer's logs
docker compose logs -f consumer

# Check status of both services
docker compose ps

# Stop and remove both containers (volume data is kept)
docker compose down

# Stop, remove containers, AND delete the volume (all data gone)
docker compose down -v
```

## What's Happening?

1. Docker Compose starts the **producer** first (because of `depends_on`)
2. The producer writes sensor readings to `/shared/data.json`
3. The **consumer** starts next and reads from the same file
4. Both services share the `sensor_data` named volume
5. Data persists even if you `docker compose down` (unless you add `-v`)
