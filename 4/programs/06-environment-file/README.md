# 06 — EnvironmentFile and .env: Loading Configuration Securely

## Concept (Part 8 of the notes)

### The Problem with Hardcoding

```python
# BAD — values hardcoded in source code
MQTT_BROKER = "192.168.1.100"
API_KEY = "sk_live_abc123verysecretkey"
MODEL_PATH = "/home/pi/models/v2/model.tflite"
```

Problems:
- Push to GitHub → API keys exposed publicly
- Deploy to 20 devices with different broker IPs → need 20 different script versions
- Upgrade model to v3 → need to edit and re-deploy source code
- Change broker IP → need to edit code, not just config

### The Solution: .env + EnvironmentFile=

Store all configuration in a separate `.env` file, never commit it, and load it at runtime.

### Project Folder Structure

```
/home/pi/edgeai/
├── inference.py          ← your Python script
├── .env                  ← configuration (never commit this)
├── .gitignore            ← tells Git to ignore .env
└── models/
    └── model.tflite      ← your model file
```

### .env File Format

```ini
# One KEY=value per line. No spaces around =. No quotes needed.
# Lines starting with # are comments.
MODEL_PATH=/home/pi/edgeai/models/model.tflite
CAMERA_ID=0
CONFIDENCE_THRESHOLD=0.75
MQTT_BROKER=192.168.1.100
MQTT_PORT=1883
API_KEY=your_secret_api_key_here
LOG_LEVEL=INFO
```

### Protecting the .env File

```bash
chmod 600 /home/pi/edgeai/.env
# -rw------- means only the owner can read/write it
```

### .gitignore

```
.env
```

### Reading Values in Python

```python
import os
MODEL_PATH = os.environ.get("MODEL_PATH", "/home/pi/models/model.tflite")
```

`os.environ.get("KEY", "default")`:
1. Look for env var named `KEY`
2. If found → use that value
3. If NOT found → use the `"default"` fallback

The fallback is important: during local development (without systemd loading .env),
the fallback keeps the script working with sensible defaults.

### EnvironmentFile= vs Environment=

| Method | When to use |
|---|---|
| `EnvironmentFile=` | Multiple values or any secrets |
| `Environment=` | One-off non-sensitive overrides |

```ini
# In .service file:
EnvironmentFile=/home/pi/edgeai/.env
# Or for single values:
Environment="LOG_LEVEL=INFO"
Environment="CAMERA_ID=0"
```

## What This Program Does

- `bad_hardcoded.py` — shows the problem with hardcoded values
- `good_env_config.py` — shows the correct approach with os.environ.get()
- `.env.example` — template .env file
- `.gitignore` — git ignore file

## How to Run

```bash
# See the bad approach:
python3 bad_hardcoded.py

# See the good approach (with .env loaded):
python3 good_env_config.py

# Test without .env (uses fallback defaults):
unset MODEL_PATH && python3 good_env_config.py
```
