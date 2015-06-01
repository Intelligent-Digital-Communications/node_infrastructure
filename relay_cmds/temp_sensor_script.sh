#!/bin/sh

# Reads an 8-bit ADC from a National Control Devices (controlanything.com) Ethernet Relay
# every 10 seconds
if [ $# -ne 2 ]
then
  echo "$0: <ip_addr> <port>"
  echo "Default port is 2101"
  exit
fi

a=0
RELAY_IP=$1
# Default port is 2101
RELAY_PORT=$2
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
