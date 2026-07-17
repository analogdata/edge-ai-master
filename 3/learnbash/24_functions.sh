#!/bin/bash
set -euo pipefail

# Define a function
check_temperature() {
    local temp_raw
    temp_raw=$(vcgencmd measure_temp)
    local temp
    temp=$(echo "$temp_raw" | cut -d= -f2 | cut -d. -f1)
    echo "$temp"
}

# Define a function with arguments
log_message() {
    local level="$1"
    local message="$2"
    echo "[$(date '+%H:%M:%S')] [$level] $message"
}

# Call the functions
current_temp=$(check_temperature)
log_message "INFO" "Current temperature: ${current_temp}C"
if [ "$current_temp" -gt 70 ]; then
    log_message "WARN" "Temperature too high!"
fi
