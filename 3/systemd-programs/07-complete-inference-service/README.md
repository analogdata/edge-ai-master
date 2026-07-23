# 07 — The Complete Edge AI Inference Service

## Concept (Parts 9 & 10 of the notes)

This folder contains the **complete, production-ready** Edge AI inference service that combines
everything from the previous programs:

- A Python script that reads config from environment variables
- Graceful shutdown via SIGTERM handling
- Startup checks (verify model file exists)
- Structured logging (readable via journalctl)
- A complete `.service` unit file with all three sections

## Files

| File | Purpose |
|---|---|
| `inference.py` | The complete production-ready Python inference script |
| `edgeai.service` | The complete systemd service unit file |
| `.env.example` | Template .env file (copy to `.env` and fill in real values) |
| `.gitignore` | Tells Git to ignore `.env` |
| `models/` | Directory for your model files (place `model.tflite` here) |

## How to Set Up on a Raspberry Pi

```bash
# Step 1: Create project folder
mkdir -p /home/pi/edgeai/models

# Step 2: Copy files
cp inference.py /home/pi/edgeai/
cp .env.example /home/pi/edgeai/.env
cp .gitignore /home/pi/edgeai/
# Place your model file:
cp model.tflite /home/pi/edgeai/models/

# Step 3: Protect .env
chmod 600 /home/pi/edgeai/.env

# Step 4: Install service file
sudo cp edgeai.service /etc/systemd/system/

# Step 5: Tell systemd about the new file
sudo systemctl daemon-reload

# Step 6: Start the service
sudo systemctl start edgeai

# Step 7: Check it's running
sudo systemctl status edgeai

# Step 8: Enable auto-start at boot
sudo systemctl enable edgeai

# Step 9: Watch live logs
journalctl -u edgeai -f
```

## How to Run Locally (without systemd)

```bash
# Using fallback defaults:
python3 inference.py

# With .env loaded manually:
set -a; source .env.example; set +a
python3 inference.py
```
