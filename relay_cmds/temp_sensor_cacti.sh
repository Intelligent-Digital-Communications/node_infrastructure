#!/bin/sh

# Reads an 8-bit ADC from a National Control Devices (controlanything.com) Ethernet Relay
# This script is ment to interface with CACTI
# PWG 7.15.2014

# Check input args
if [ $# -lt 2 ] 
then
  echo "usage: $0 <ip_addr> <cmd_file>"
  exit
fi

# Read args and constants
#RELAY_IP=143.215.249.197
RELAY_IP=$1
RELAY_PORT=2101
RELAY_CMD=$2

# Check for file existance
if [ ! -f $RELAY_CMD ] 
then
  echo "Can't find relay command file $RELAY_CMD."
  exit
fi

#Execute
val=`cat $RELAY_CMD | nc $RELAY_IP $RELAY_PORT | hexdump -v -e '"%d"'` 
# Convert 8-bit temperature value (deg F)
temp=`echo "scale=2; ${val}*5*100/255" | bc -l`
echo "$temp"
