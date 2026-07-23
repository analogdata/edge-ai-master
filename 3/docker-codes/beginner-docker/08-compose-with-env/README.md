# 08 — Compose with Environment Variables and .env

Demonstrates three ways to pass environment variables to containers.

## What You'll Learn

- How `ENV` in a Dockerfile sets **defaults** baked into the image
- How `environment` in docker-compose.yml **overrides** at runtime
- How `.env` file provides **secrets** automatically loaded by Compose
- How `${VAR_NAME}` syntax reads from `.env` in the compose file

## Three Ways to Set Environment Variables

```
Priority (highest wins):
  ┌──────────────────────────────────────────────────────────┐
  │  docker-compose.yml 'environment' section                │  ← wins
  │  .env file (via ${VAR_NAME} in compose)                  │
  │  ENV instruction in Dockerfile                           │  ← default
  │  os.environ.get("VAR", "fallback") in Python             │  ← last resort
  └──────────────────────────────────────────────────────────┘
```

## Try It

```bash
# Start the app — see all config values printed
docker compose up

# You should see:
#   APP_NAME        : my-env-app        (from compose 'environment')
#   ENVIRONMENT     : production        (from compose 'environment')
#   API_KEY         : sk-1234567890...  (from .env file)
#   DATABASE_URL    : sqlite:///data... (from .env file)
#   LOG_LEVEL       : INFO              (from Dockerfile ENV default)

# Try changing .env and restart
# Edit .env: API_KEY=sk-different-key
docker compose down
docker compose up

# Try changing docker-compose.yml environment values
# Edit: - APP_NAME=custom-name
docker compose down
docker compose up
```

## .env File Best Practices

1. **Never commit `.env` to git** — add it to `.gitignore`
2. **Commit `.env.example`** — shows what variables are needed (no secrets)
3. **Use `.env` for secrets** — API keys, passwords, tokens
4. **Use `environment` in compose** for non-secret config — app name, log level

## env_file vs ${VAR} — What's the Difference?

```yaml
# Method A: ${VAR} — reference individual variables from .env
environment:
  - API_KEY=${API_KEY}     # reads API_KEY from .env

# Method B: env_file — load ALL variables from a file
env_file:
  - .env                   # every line in .env becomes an env var
```

- **Method A** (`${VAR}`): You pick specific variables. More explicit.
- **Method B** (`env_file`): All variables loaded at once. Less control.
