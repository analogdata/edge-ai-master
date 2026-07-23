# Docker Codes — Edge AI on Raspberry Pi (ARM64)

Analog Data — EdgeAI Engineering Bootcamp

Programs and configurations from the "Docker on Pi (ARM64)" notes (3.3).

## Two Learning Tracks

- **`beginner-docker/`** — Start here if you're new to Docker. Progressive examples from hello-world to multi-service compose.
- **Root examples (`01-04`)** — Production-style Edge AI Dockerfiles and compose stacks from the notes.

## Directory Structure

```
docker-codes/
│
├── beginner-docker/                # 🟢 START HERE — No Docker experience needed
│   ├── 01-hello-world/             # Absolute simplest Dockerfile (prints hello)
│   ├── 02-first-python-app/        # Python app with ENV, WORKDIR, COPY
│   ├── 03-dockerfile-explained/    # Every Dockerfile instruction annotated
│   ├── 04-docker-run-flags/        # All essential docker run flags explained
│   ├── 05-first-compose/           # Simplest docker-compose.yml (one service)
│   ├── 06-two-service-compose/     # Two services sharing data via volumes
│   ├── 07-compose-with-volumes/    # Named volumes & bind mounts (persistence)
│   └── 08-compose-with-env/        # Environment variables & .env files
│
├── 01-basic-dockerfile/            # Part 4 — Simple single-stage Dockerfile
│   ├── Dockerfile                  # Basic Dockerfile with FROM, WORKDIR, COPY, RUN, CMD
│   ├── inference.py                # Edge AI inference engine (simulated)
│   └── requirements.txt            # Python dependencies
│
├── 02-multistage-dockerfile/       # Part 5 — Multi-stage Dockerfile (builder + runtime)
│   ├── Dockerfile                  # Two-stage build: builder compiles, runtime runs
│   ├── inference.py                # Same inference engine, designed for multi-stage
│   └── requirements.txt            # Includes tflite-runtime for real inference
│
├── 03-docker-compose-stack/        # Part 6 — Full 4-service Docker Compose stack
│   ├── docker-compose.yml          # MQTT + Inference + FastAPI + SQLite backup
│   ├── .env                        # Environment variables (secrets)
│   ├── .dockerignore               # Exclude files from build context
│   ├── Dockerfile                  # Multi-stage Dockerfile for inference service
│   ├── inference.py                # Inference engine for the compose stack
│   ├── requirements.txt            # Inference dependencies
│   ├── api/                        # FastAPI server subfolder
│   │   ├── Dockerfile              # Dockerfile for the API service
│   │   ├── main.py                 # FastAPI app with SQLite + MQTT subscriber
│   │   └── requirements.txt        # API dependencies
│   ├── mosquitto/                  # Mosquitto MQTT broker config
│   │   └── config/
│   │       └── mosquitto.conf      # Broker configuration
│   ├── models/                     # Place your model.tflite here
│   └── backups/                    # SQLite backups are written here
│
└── 04-check-architecture/          # Part 9 — Verify ARM64 architecture
    └── check_architecture.py       # Script to detect CPU architecture
```

## Beginner Quick Start (No Experience Needed)

Work through these in order — each builds on the previous one.

### 01. Hello World — Your first Docker image
```bash
cd beginner-docker/01-hello-world
docker build -t my-hello .
docker run my-hello
```

### 02. First Python App — ENV, WORKDIR, COPY
```bash
cd beginner-docker/02-first-python-app
docker build -t my-first-app .
docker run my-first-app
docker run -e NAME=Alice my-first-app   # override env var
```

### 03. Dockerfile Explained — Every instruction annotated
```bash
cd beginner-docker/03-dockerfile-explained
docker build -t dockerfile-explained .
docker run dockerfile-explained
```

### 04. Docker Run Flags — All essential flags
```bash
cd beginner-docker/04-docker-run-flags
docker build -t counter-app .
docker run -d --name my-counter counter-app
docker logs -f my-counter
docker stop my-counter && docker rm my-counter
```

### 05. First Compose — Simplest docker-compose.yml
```bash
cd beginner-docker/05-first-compose
docker compose up        # Ctrl+C to stop
docker compose down      # cleanup
```

### 06. Two Service Compose — Producer + Consumer
```bash
cd beginner-docker/06-two-service-compose
docker compose up        # see both services' logs
docker compose down
```

### 07. Compose with Volumes — Data persistence
```bash
cd beginner-docker/07-compose-with-volumes
docker compose up -d
docker compose logs -f
docker compose down      # data is KEPT
docker compose up -d     # counter continues from where it left off!
docker compose down -v   # now delete the data too
```

### 08. Compose with Env — .env files and variables
```bash
cd beginner-docker/08-compose-with-env
docker compose up        # see all config values printed
docker compose down
```

## Production Examples Quick Start

### 1. Basic Dockerfile (Part 4)

```bash
cd 01-basic-dockerfile
docker build -t edgeai:latest .
docker run edgeai:latest
```

### 2. Multi-Stage Dockerfile (Part 5)

```bash
cd 02-multistage-dockerfile
docker build -t edgeai:latest .
docker run edgeai:latest
```

### 3. Docker Compose Stack (Part 6)

```bash
cd 03-docker-compose-stack

# Start all 4 services in the background
docker compose up -d

# Check status
docker compose ps

# Watch inference logs
docker compose logs -f inference

# Stop everything
docker compose down
```

### 4. Check Architecture (Part 9)

```bash
# Run on your Pi
python3 04-check-architecture/check_architecture.py

# Or inside a container
docker run --rm python:3.11-slim python3 -c "
import platform; print(platform.machine())
"
```

## Key Concepts

- **Image**: Read-only template (the recipe)
- **Container**: Running instance of an image (the dish)
- **Dockerfile**: Instructions to build an image
- **Docker Compose**: Define and run multiple containers together
- **ARM64**: Raspberry Pi's CPU architecture — images must be ARM64-compatible
- **Multi-stage build**: Small final image by separating build and runtime stages
- **Resource limits**: `mem_limit` and `cpus` prevent one container from crashing the Pi
