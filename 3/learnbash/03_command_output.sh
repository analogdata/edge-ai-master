#!/bin/bash
current_date=$(date)
current_user=$(whoami)
disk_space=$(df -h / | tail -1 | awk '{print $5}')
echo "Date: $current_date"
echo "User: $current_user"
echo "Disk used: $disk_space"
