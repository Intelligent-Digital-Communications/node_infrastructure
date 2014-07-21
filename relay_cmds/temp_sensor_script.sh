#!/bin/sh

# Reads an 8-bit ADC from a National Control Devices (controlanything.com) Ethernet Relay
# PWG 7.15.2014
a=0
RELAY_IP=143.215.249.197
RELAY_PORT=2101
RELAY_CMD="relay_readadc1_8bit.hex"
# Update Rate (sec)
UPDATE_TIME=10
while [ "$a"==0 ]; do
 val=`cat $RELAY_CMD | nc $RELAY_IP $RELAY_PORT | hexdump -v -e '"%d"'` 
 # Convert 8-bit temperature value
 temp=`echo "scale=2; ${val}*5*100/255" | bc -l`
 echo "`date`|$temp deg F"
 sleep $UPDATE_TIME
done
