#!/bin/bash
set -euo pipefail
# =====================================================
# System Health Reporter for Raspberry Pi
# Usage: ./health_report.sh
# =====================================================
echo "======================================"
echo "   RASPBERRY PI HEALTH REPORT"
echo "   $(date)"
echo "======================================"
# --- Temperature ---
# Note: vcgencmd is Raspberry Pi specific.
# On non-Pi systems, this will fail due to set -e.
# Comment out the vcgencmd lines and uncomment the dummy line to test on other systems.
temp_raw=$(vcgencmd measure_temp)              # output: temp=52.3'C
temp=$(echo "$temp_raw" | cut -d= -f2)        # extract: 52.3'C
echo ""
echo "CPU Temperature : $temp"
# Check if overheating
temp_num=$(echo "$temp" | cut -d. -f1)        # get just the number: 52
if [ "$temp_num" -gt 80 ]; then
    echo "STATUS          : ❌ CRITICAL - Overheating!"
elif [ "$temp_num" -gt 65 ]; then
    echo "STATUS          : ⚠️  WARNING  - Running hot"
else
    echo "STATUS          : ✅ OK"
fi
# --- Memory ---
echo ""
echo "Memory Usage:"
free -h | grep Mem | awk '{printf "  Total: %s | Used: %s | Free: %s\n", $2, $3, $4}'
# --- Disk Space ---
echo ""
echo "Disk Usage (root partition):"
df -h / | tail -1 | awk '{printf "  Total: %s | Used: %s | Free: %s | Used%%: %s\n", $2, $3, $4, $5}'
# Check if disk is almost full
disk_used=$(df / | tail -1 | awk '{print $5}' | cut -d% -f1)
if [ "$disk_used" -gt 90 ]; then
    echo "  STATUS: ❌ CRITICAL - Disk almost full!"
elif [ "$disk_used" -gt 75 ]; then
    echo "  STATUS: ⚠️  WARNING - Disk getting full"
else
    echo "  STATUS: ✅ OK"
fi
# --- CPU Load ---
echo ""
echo "CPU Load (1 min avg):"
load=$(cat /proc/loadavg | awk '{print $1}')
echo "  Load Average: $load"
# --- Throttling Check ---
echo ""
echo "Throttling Status:"
throttled=$(vcgencmd get_throttled)
if [ "$throttled" = "throttled=0x0" ]; then
    echo "  STATUS: ✅ No throttling detected"
else
    echo "  STATUS: ⚠️  WARNING - Throttling detected: $throttled"
fi
echo ""
echo "======================================"
echo "Report generated: $(date)"
echo "======================================"
