#!/bin/bash
LOGFILE="power_log.csv"

echo "Timestamp,Power (W)" > "$LOGFILE"

INTERVAL=5

echo "Logging power usage every $INTERVAL seconds. Press Ctrl+C to stop."

while true; do
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    
    # Read initial energy values (in microjoules)
    declare -a T0=( $(sudo cat /sys/class/powercap/*/energy_uj) )
    
    # Wait for the defined interval
    sleep $INTERVAL
    
    # Read energy values again after the interval
    declare -a T1=( $(sudo cat /sys/class/powercap/*/energy_uj) )
    
    # Calculate the total energy difference for all sensors
    sum_diff=0
    for i in "${!T0[@]}"; do
        diff=$(( ${T1[i]} - ${T0[i]} ))
        sum_diff=$(( sum_diff + diff ))
    done
    
    # Convert energy difference to power (Watts)
    # Energy difference is in microjoules, so we divide by the interval and 1e6 to get Watts.
    power=$(awk -v diff="$sum_diff" -v interval="$INTERVAL" 'BEGIN { printf "%.1f", diff/interval/1e6 }')
    
    # Append the timestamp and power reading to the log file
    echo "$TIMESTAMP,$power" >> "$LOGFILE"
done

