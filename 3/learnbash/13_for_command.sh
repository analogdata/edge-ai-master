#!/bin/bash
# Run a health check for each sensor listed in a file
# Create a sample sensors.txt file first:
#   echo "sensor_01" > /tmp/sensors.txt
#   echo "sensor_02" >> /tmp/sensors.txt
#   echo "sensor_03" >> /tmp/sensors.txt
# Then run: ./for_command.sh

SENSOR_FILE="/tmp/sensors.txt"

# Create a demo file if it doesn't exist
if [ ! -f "$SENSOR_FILE" ]; then
    echo "sensor_01" > "$SENSOR_FILE"
    echo "sensor_02" >> "$SENSOR_FILE"
    echo "sensor_03" >> "$SENSOR_FILE"
    echo "Created demo $SENSOR_FILE"
fi

for sensor_id in $(cat "$SENSOR_FILE"); do
    echo "Checking sensor: $sensor_id"
    # run your check here
done
