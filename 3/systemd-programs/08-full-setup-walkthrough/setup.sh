#!/bin/bash
#
# setup.sh — Automated setup for the Edge AI inference service
# Run on Raspberry Pi:  sudo bash setup.sh
#
# This script automates the steps from the setup walkthrough (Part 11).

set -e

PROJECT_DIR="/home/pi/edgeai"
SERVICE_NAME="edgeai"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

echo "=========================================="
echo " Edge AI Service — Automated Setup"
echo "=========================================="
echo ""

# Step 1: Create project folder
echo "[1/10] Creating project folder..."
mkdir -p ${PROJECT_DIR}/models
echo "  Done: ${PROJECT_DIR}/models/"

# Step 2: Copy Python script
echo "[2/10] Copying inference script..."
if [ -f inference.py ]; then
    cp inference.py ${PROJECT_DIR}/
    echo "  Done: ${PROJECT_DIR}/inference.py"
else
    echo "  WARNING: inference.py not found in current directory."
    echo "  Please copy it manually: cp inference.py ${PROJECT_DIR}/"
fi

# Step 3: Create .env file
echo "[3/10] Creating .env file..."
if [ -f .env.example ]; then
    cp .env.example ${PROJECT_DIR}/.env
    echo "  Done: ${PROJECT_DIR}/.env (from .env.example)"
    echo "  >>> EDIT IT: nano ${PROJECT_DIR}/.env"
else
    echo "  WARNING: .env.example not found. Creating minimal .env..."
    cat > ${PROJECT_DIR}/.env << 'EOF'
MODEL_PATH=/home/pi/edgeai/models/model.tflite
CAMERA_ID=0
CONFIDENCE_THRESHOLD=0.5
MQTT_BROKER=localhost
MQTT_PORT=1883
LOG_LEVEL=INFO
EOF
    echo "  Done: ${PROJECT_DIR}/.env (minimal defaults)"
fi

# Step 4: Protect .env
echo "[4/10] Setting .env permissions to 600..."
chmod 600 ${PROJECT_DIR}/.env
echo "  Done: $(ls -la ${PROJECT_DIR}/.env)"

# Step 5: Create .gitignore
echo "[5/10] Creating .gitignore..."
echo ".env" > ${PROJECT_DIR}/.gitignore
echo "  Done: ${PROJECT_DIR}/.gitignore"

# Step 6: Install service file
echo "[6/10] Installing service file..."
if [ -f edgeai.service ]; then
    cp edgeai.service ${SERVICE_FILE}
    echo "  Done: ${SERVICE_FILE}"
else
    echo "  WARNING: edgeai.service not found. Creating from template..."
    cat > ${SERVICE_FILE} << 'EOF'
[Unit]
Description=Edge AI Inference Service
After=network.target
StartLimitIntervalSec=60
StartLimitBurst=5

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/edgeai
EnvironmentFile=/home/pi/edgeai/.env
ExecStartPre=/bin/bash -c 'test -f /home/pi/edgeai/models/model.tflite'
ExecStart=/usr/bin/python3 /home/pi/edgeai/inference.py
ExecStop=/bin/kill -SIGTERM $MAINPID
Restart=always
RestartSec=5
TimeoutStopSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=edgeai

[Install]
WantedBy=multi-user.target
EOF
    echo "  Done: ${SERVICE_FILE} (from template)"
fi

# Step 7: daemon-reload
echo "[7/10] Running daemon-reload..."
systemctl daemon-reload
echo "  Done."

# Step 8: Start service
echo "[8/10] Starting service..."
systemctl start ${SERVICE_NAME}
echo "  Done."

# Step 9: Check status
echo "[9/10] Checking status..."
systemctl status ${SERVICE_NAME} --no-pager || true

# Step 10: Enable at boot
echo "[10/10] Enabling auto-start at boot..."
systemctl enable ${SERVICE_NAME}
echo "  Done."

echo ""
echo "=========================================="
echo " SETUP COMPLETE!"
echo "=========================================="
echo ""
echo " Watch live logs:"
echo "   journalctl -u ${SERVICE_NAME} -f"
echo ""
echo " Check status:"
echo "   sudo systemctl status ${SERVICE_NAME}"
echo ""
echo " Stop the service:"
echo "   sudo systemctl stop ${SERVICE_NAME}"
echo ""
echo " >>> Remember to edit your .env file:"
echo "   nano ${PROJECT_DIR}/.env"
echo "   sudo systemctl restart ${SERVICE_NAME}"
