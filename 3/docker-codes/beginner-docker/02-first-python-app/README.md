# 02 — First Python App in Docker

A simple Python app that reads an environment variable and prints a greeting.

## What You'll Learn

- How `WORKDIR` sets the working directory inside a container
- How `COPY` transfers your files into the container
- How `ENV` sets environment variables with defaults
- How to override environment variables with `docker run -e`

## Try It

```bash
# Build the image
docker build -t my-first-app .

# Run with the default NAME (World)
docker run my-first-app
# Output: Hello, World!

# Run with a custom NAME
docker run -e NAME=Alice my-first-app
# Output: Hello, Alice!

# Run with a different name each time
docker run -e NAME="Edge AI Engineer" my-first-app
```

## What's Happening?

1. `FROM python:3.11-slim` — downloads a small Python image (if not cached)
2. `WORKDIR /app` — creates and enters the `/app` directory inside the container
3. `COPY app.py .` — copies `app.py` from your computer into `/app/` in the container
4. `ENV NAME="World"` — sets a default value for the NAME environment variable
5. `CMD ["python3", "app.py"]` — runs the script when the container starts
