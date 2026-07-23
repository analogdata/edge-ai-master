# Hands-On Lab — Edge AI Inference on Raspberry Pi

Analog Data — EdgeAI Engineering Bootcamp (Module 3)

## Overview

This lab takes a single Python inference script and runs it three ways:

1. **Part A** — Directly with `python3 inference.py`
2. **Part B** — As a **systemd service** with auto-restart and boot persistence
3. **Part C** — In a **Docker container** managed by Docker Compose with resource limits
4. **Part D** — Cleanup (stop one before running the other)

You will crash-test both systemd and Docker to verify auto-restart works.

## Prerequisites

- Raspberry Pi 4B or Pi 5 running Pi OS Bookworm (64-bit)
- SSH access to the Pi from your laptop
- Docker installed (Module 3.3 installation steps)
- A model file at `/home/pi/edgeai/models/model.tflite`

```bash
# On the Pi — create the directory structure and placeholder model
mkdir -p /home/pi/edgeai/models
mkdir -p /home/pi/edgeai/logs
touch /home/pi/edgeai/models/model.tflite
```

## File Structure

```
hands-on-lab/
├── inference.py                 # Part A — the inference script (works everywhere)
├── .env                         # Part B — environment variables for systemd
├── requirements.txt             # Part C — Python dependencies (empty for lab)
├── edgeai.service               # Part B — systemd service file
├── crash_test_systemd.py        # Part B — automated crash test for systemd
├── Dockerfile                   # Part C — multi-stage Dockerfile (builder + runtime)
├── .dockerignore                # Part C — exclude files from Docker build
├── docker-compose.yml           # Part C — single inference service with limits
├── crash_test_docker.py         # Part C — automated crash test for Docker
├── docker-compose-mqtt.yml      # Extension 1 — add MQTT broker service
├── test_start_limit_burst.py    # Extension 3 — test systemd StartLimitBurst
├── models/                      # Place model.tflite here
├── logs/                        # Log directory (if using file-based logging)
└── README.md                    # This file
```

---

## Part A — Python Script

### Step 1: Copy files to the Pi

```bash
# From your laptop — copy the lab files to the Pi
scp -r hands-on-lab/ pi@<pi-ip>:/home/pi/edgeai/
```

Or create the files directly on the Pi following the instructions below.

### Step 2: Create the inference script

The script is in `inference.py`. Copy it to the Pi:

```bash
# On the Pi
cp inference.py /home/pi/edgeai/inference.py
```

### Step 3: Create the model placeholder

```bash
mkdir -p /home/pi/edgeai/models
touch /home/pi/edgeai/models/model.tflite
```

### Step 4: Test the script manually

```bash
python3 /home/pi/edgeai/inference.py
```

Expected output:
```
2026-07-23 08:30:00  INFO     =======================================================
2026-07-23 08:30:00  INFO       Edge AI Inference Service — LAB VERSION
2026-07-23 08:30:00  INFO     =======================================================
2026-07-23 08:30:00  INFO     Model path : /home/pi/edgeai/models/model.tflite
2026-07-23 08:30:00  INFO     Interval   : 2.0s between frames
2026-07-23 08:30:00  INFO     Model file found. Starting inference loop.
2026-07-23 08:30:00  INFO     Frame 000001 | Elapsed: 0.0s | Avg FPS: 0.00
2026-07-23 08:30:02  INFO     Frame 000002 | Elapsed: 2.0s | Avg FPS: 1.00
```

Press `Ctrl+C` to stop. Fix any errors before moving on.

---

## Part B — systemd Service

### Step 1: Create the .env file

```bash
cp .env /home/pi/edgeai/.env
chmod 600 /home/pi/edgeai/.env    # protect it — only pi user can read
```

### Step 2: Install the service file

```bash
sudo cp edgeai.service /etc/systemd/system/edgeai.service
```

### Step 3: Enable and start the service

```bash
# Tell systemd about the new file
sudo systemctl daemon-reload

# Start it now
sudo systemctl start edgeai

# Check it is running
sudo systemctl status edgeai
# You should see: Active: active (running)
```

### Step 4: Watch the live logs

Open a second terminal:

```bash
journalctl -u edgeai -f
```

You should see inference frames scrolling. Leave this running for the crash test.

### Step 5: Enable auto-start at boot

```bash
sudo systemctl enable edgeai
```

### Step 6: CRASH TEST — Verify auto-restart in <= 5 seconds

**Option A — Manual:**

```bash
# Terminal 1: find and kill the process
sudo kill -9 $(systemctl show -p MainPID edgeai | cut -d= -f2)

# Terminal 2 (journalctl -f): watch the restart
# You should see the service restart within 5 seconds
```

**Option B — Automated:**

```bash
python3 crash_test_systemd.py
```

Record your results:

| Test | Expected | Actual |
|------|----------|--------|
| Time from crash to restart | <= 5 seconds | ___ seconds |
| Service status after restart | active (running) | ___ |
| Frame counter restarted from 1 | Yes | ___ |

### Step 7: Test boot persistence

```bash
sudo reboot
# Wait for the Pi to come back up, SSH in, then:
sudo systemctl status edgeai
# Should be running without you doing anything
```

---

## Part C — Dockerise the Inference Script

### Step 1: Copy files to the Pi (if not already there)

```bash
# Ensure these files are in /home/pi/edgeai/:
#   inference.py, requirements.txt, Dockerfile, .dockerignore, docker-compose.yml
```

### Step 2: Build the Docker image

```bash
cd /home/pi/edgeai
docker compose build
```

Confirm the image was created:
```bash
docker images
# Should show the edgeai image with a recent timestamp
```

### Step 3: Start the container

```bash
docker compose up -d
```

Check it is running:
```bash
docker compose ps
# Should show: edgeai_lab  ...  Up X seconds
```

### Step 4: Watch the container logs

```bash
docker compose logs -f inference
```

You should see the same inference output as the direct run.

### Step 5: CRASH TEST — Verify Docker auto-restart

**Option A — Manual:**

```bash
# Terminal 1: force kill the container
docker kill --signal=SIGKILL edgeai_lab

# Terminal 2 (docker compose logs -f): watch the restart
# Docker restarts much faster than systemd (usually under 2 seconds)
```

**Option B — Automated:**

```bash
python3 crash_test_docker.py
```

Verify:
```bash
docker compose ps
# Status should show "Up X seconds" confirming it restarted
```

Record your results:

| Test | Expected | Actual |
|------|----------|--------|
| Time from kill to restart | < 5 seconds | ___ seconds |
| Container status after restart | Up X seconds | ___ |
| Frame counter restarted from 1 | Yes | ___ |

### Step 6: Stop the Docker service cleanly

```bash
docker compose down
```

---

## Part D — Stop the systemd Service (Avoid Conflicts)

Both systemd and Docker use the same script and model. Stop one before running the other:

```bash
# If keeping Docker, stop systemd:
sudo systemctl stop edgeai
sudo systemctl disable edgeai

# If keeping systemd, stop Docker:
docker compose down
```

---

## Extension Tasks

### Extension 1: Add an MQTT Broker to Docker Compose

```bash
# Use the mqtt compose file instead of the base one
docker compose -f docker-compose-mqtt.yml up -d

# Verify both services are running
docker compose -f docker-compose-mqtt.yml ps
# Should show: edgeai_lab  AND  mqtt_broker_lab

# Watch both services' logs
docker compose -f docker-compose-mqtt.yml logs -f

# Stop everything
docker compose -f docker-compose-mqtt.yml down
```

### Extension 2: Reduce the Docker Image Size

```bash
# Check current image size
docker images

# Try these techniques to reduce it:
#   1. Add more entries to .dockerignore
#   2. Use python:3.11-alpine as the runtime base (much smaller)
#   3. Combine RUN commands with && to reduce layers
#   4. Remove unnecessary files in the same layer they're created

# After changes, rebuild and compare:
docker compose build
docker images
```

### Extension 3: Test StartLimitBurst

```bash
# This script patches inference.py to crash immediately,
# then watches systemd retry up to 5 times before giving up
python3 test_start_limit_burst.py

# What you should see:
#   - systemd retries the service up to 5 times
#   - Each retry is ~5 seconds apart (RestartSec=5)
#   - After 5 failures in 60s, systemd stops (StartLimitBurst=5)
#   - systemctl status shows 'failed' with 'start-limit-hit'
```

### Extension 4: Use tmux for the Whole Lab

```bash
# Start a tmux session
tmux new -s edgeai-lab

# Inside tmux, run your commands
# Detach: Ctrl+B then d
# Close SSH — everything keeps running

# Reconnect later
ssh pi@<pi-ip>
tmux attach -t edgeai-lab

# Split panes inside tmux:
#   Ctrl+B then %   — split vertically
#   Ctrl+B then "   — split horizontally
```

---

## Lab Completion Checklist

### Part A — Python Script

- [ ] I created `inference.py` and it runs cleanly with `python3 inference.py`
- [ ] I understand what `os.environ.get()` does in the script

### Part B — systemd Service

- [ ] I created and secured `.env` with `chmod 600`
- [ ] I created `/etc/systemd/system/edgeai.service` with all correct fields
- [ ] I ran `daemon-reload`, `start`, `status` in the correct order
- [ ] `systemctl status edgeai` shows `Active: active (running)`
- [ ] I can see live logs with `journalctl -u edgeai -f`
- [ ] I ran `systemctl enable edgeai` for boot persistence
- [ ] **CRASH TEST PASSED** — Service restarted in <= 5 seconds after `kill -9`
- [ ] **REBOOT TEST PASSED** — Service was running after `sudo reboot`

### Part C — Docker

- [ ] I created `Dockerfile` with two stages (builder and runtime)
- [ ] I created `.dockerignore`
- [ ] I created `docker-compose.yml` with `restart: always`, volumes, and resource limits
- [ ] `docker compose build` completed without errors
- [ ] `docker compose up -d` started the container
- [ ] `docker compose ps` shows the container as `Up`
- [ ] I can see live container logs with `docker compose logs -f inference`
- [ ] **CRASH TEST PASSED** — Container restarted automatically after `docker kill --signal=SIGKILL`

### Instructor Sign-Off

| Check | Student Demo | Instructor Sign |
|-------|-------------|-----------------|
| systemd service running at boot | | |
| Crash test — restart within 5s | | |
| Docker container with resource limits | | |
| Docker crash test — auto-restart | | |
