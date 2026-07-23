# 03 — Dockerfile Explained

Every common Dockerfile instruction demonstrated with detailed comments.

## Instructions Covered

| Instruction    | Purpose                                         |
| -------------- | ----------------------------------------------- |
| `FROM`         | Base image to start from                        |
| `LABEL`        | Metadata (maintainer, version, etc.)            |
| `WORKDIR`      | Working directory inside the container          |
| `COPY`         | Copy files from host into the container         |
| `RUN`          | Run a shell command during the build            |
| `ENV`          | Set environment variables                       |
| `EXPOSE`       | Document which port the app listens on          |
| `USER`         | Run as a non-root user (security)               |
| `CMD`          | Default command when the container starts       |
| `ENTRYPOINT`   | Like CMD but harder to override (explained)     |

## Try It

```bash
# Build
docker build -t dockerfile-explained .

# Run with defaults
docker run dockerfile-explained

# Override the NAME env var
docker run -e APP_NAME="My Custom App" dockerfile-explained

# Override the CMD entirely
docker run dockerfile-explained python3 -c "print('Different command!')"

# Inspect the image metadata (shows LABELs)
docker inspect dockerfile-explained | grep -A5 Labels
```

## Quick Reference: Image vs Container

```
Image                          Container
─────                          ─────────
Read-only template             Running instance
Built with `docker build`      Created with `docker run`
Stored on disk                 Runs in memory
Can create many containers     One image → many containers
Like a recipe                  Like the cooked dish
```
