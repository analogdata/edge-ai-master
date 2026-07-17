#!/bin/bash
set -euo pipefail
# =====================================================
# Log Cleanup Script — Delete log files older than N days
# Usage: ./cleanup_logs.sh [log_directory] [days_to_keep]
# Default: /home/pi/logs and 7 days
# =====================================================

LOG_DIR="${1:-/home/pi/logs}"
DAYS="${2:-7}"

if [ ! -d "$LOG_DIR" ]; then
    echo "Error: Directory $LOG_DIR does not exist."
    exit 1
fi

echo "Cleaning up log files older than $DAYS days in: $LOG_DIR"
find "$LOG_DIR" -name "*.log" -mtime +"$DAYS" -print
find "$LOG_DIR" -name "*.log" -mtime +"$DAYS" -delete
echo "Cleanup complete."
