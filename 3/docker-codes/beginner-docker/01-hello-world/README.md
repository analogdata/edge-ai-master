# 01 — Hello World

The absolute simplest Docker example. One Dockerfile, one line of output.

## What is Docker?

Docker packages your code AND everything it needs (Python, libraries, system
dependencies) into one portable unit called a **container**. The container runs
identically on your laptop, on a Raspberry Pi, and on a cloud server.

**Analogy**: Think of a shipping container. Before standard containers existed,
cargo was loaded piece by piece — every port used different methods. Shipping
containers solved this: pack everything into a standard box, and every port
handles it the same way. Docker works the same way for software.

## Key Terms

- **Image**: A read-only template (the recipe). Built once, used many times.
- **Container**: A running instance of an image (the dish).
- **Dockerfile**: A text file with instructions for building an image.

## Try It

```bash
# Build the image (the -t gives it a name/tag)
docker build -t my-hello .

# Run the container
docker run my-hello

# You should see:  Hello from Docker!
```

## What Happens Behind the Scenes

1. `docker build` reads the Dockerfile, downloads `python:3.11-slim` from
   Docker Hub (if not already cached), and creates an image named `my-hello`.
2. `docker run` creates a new container from that image and runs the `CMD`.
3. The Python script prints the message, and the container exits.
