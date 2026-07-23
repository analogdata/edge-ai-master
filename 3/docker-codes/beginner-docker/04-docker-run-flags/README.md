# 04 — Docker Run Flags

Learn the essential `docker run` flags with a simple counting app.

## Build the Image

```bash
docker build -t counter-app .
```

## Essential `docker run` Flags

### 1. Basic Run (foreground — blocks your terminal)

```bash
docker run counter-app
```
The container runs in the foreground. Press Ctrl+C to stop it.

### 2. Detached Mode (-d — runs in the background)

```bash
docker run -d counter-app
```
The container runs in the background. Docker prints the container ID.
You can continue using your terminal.

### 3. Give the Container a Name (--name)

```bash
docker run -d --name my-counter counter-app
```
Instead of a random name like "festive_einstein", the container is named
"my-counter". Easier to reference later:
```bash
docker logs my-counter
docker stop my-counter
docker rm my-counter
```

### 4. Environment Variables (-e)

```bash
docker run -d --name my-counter -e APP_NAME="MyApp" -e INTERVAL="5" counter-app
```
Overrides the ENV defaults from the Dockerfile. The app now prints every 5
seconds with the name "MyApp".

### 5. Auto-Remove (--rm)

```bash
docker run --rm counter-app
```
The container is automatically removed when it stops. Great for one-off
commands. No need to `docker rm` afterwards.

### 6. Interactive Shell (-it)

```bash
docker run -it python:3.11-slim bash
```
Opens an interactive bash shell inside the container. Great for debugging
and exploring what's inside an image.
- `-i` = keep stdin open (interactive)
- `-t` = allocate a pseudo-TTY (terminal)

### 7. Port Mapping (-p)

```bash
docker run -d -p 8080:8000 my-web-app
```
Maps port 8080 on your host to port 8000 inside the container.
Format: `-p <host_port>:<container_port>`

### 8. Volume Mount (-v)

```bash
docker run -d -v /home/pi/data:/app/data counter-app
```
Mounts `/home/pi/data` from your host into `/app/data` in the container.
Changes on either side are immediately visible on the other.

## Other Essential Commands

```bash
# List running containers
docker ps

# List ALL containers (including stopped ones)
docker ps -a

# View container logs
docker logs my-counter

# Watch logs live (like tail -f)
docker logs -f my-counter

# View last 20 lines of logs
docker logs --tail 20 my-counter

# Open a shell inside a running container
docker exec -it my-counter bash

# Check resource usage (CPU, memory) of all containers
docker stats

# Stop a container
docker stop my-counter

# Start a stopped container
docker start my-counter

# Remove a stopped container
docker rm my-counter

# Stop and remove in one command
docker rm -f my-counter
```

## Cleanup Commands

```bash
# Remove all stopped containers, unused images, unused networks
docker system prune

# Remove everything including unused images (more aggressive)
docker system prune -a

# Check total disk usage by Docker
docker system df
```
