#!/bin/bash
set -euo pipefail
# =====================================================
# Combined Demo — Showcases multiple concepts together
# Usage: ./combined_demo.sh
# Demonstrates: variables, if, for, while, case, functions,
#               colours, user input, and safe mode
# =====================================================

# Colour codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function: log a message with timestamp and colour
log_message() {
    local level="$1"
    local message="$2"
    local colour="$NC"
    case "$level" in
        "INFO")  colour="$BLUE" ;;
        "WARN")  colour="$YELLOW" ;;
        "ERROR") colour="$RED" ;;
        "OK")    colour="$GREEN" ;;
    esac
    echo -e "${colour}[$(date '+%H:%M:%S')] [$level] $message${NC}"
}

# Function: check if a file exists
check_file() {
    local filepath="$1"
    if [ -f "$filepath" ]; then
        log_message "OK" "File exists: $filepath"
        return 0
    else
        log_message "ERROR" "File not found: $filepath"
        return 1
    fi
}

echo "======================================"
echo "  Combined Shell Scripting Demo"
echo "  $(date)"
echo "======================================"

# --- Variables ---
device="Raspberry Pi"
log_message "INFO" "Device: $device"

# --- User input ---
echo ""
read -p "Enter a file path to check (or press Enter for /tmp/test.txt): " user_file
user_file="${user_file:-/tmp/test.txt}"
check_file "$user_file"

# --- For loop ---
echo ""
log_message "INFO" "Looping through a list of models:"
for model in resnet50 mobilenet_v2 efficientnet; do
    echo "  - $model"
done

# --- While loop ---
echo ""
log_message "INFO" "Countdown:"
count=3
while [ $count -gt 0 ]; do
    echo "  $count..."
    sleep 1
    count=$((count - 1))
done
log_message "OK" "Ready!"

# --- Case statement ---
echo ""
read -p "Choose an action (start/stop/status): " action
case "$action" in
    "start")  log_message "INFO" "Starting inference service..." ;;
    "stop")   log_message "WARN" "Stopping inference service..." ;;
    "status") log_message "INFO" "Service status: running" ;;
    *)        log_message "ERROR" "Unknown action: $action" ;;
esac

echo ""
echo "======================================"
log_message "OK" "Demo complete!"
echo "======================================"
