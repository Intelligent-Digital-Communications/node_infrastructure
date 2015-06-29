#!/bin/sh

# Reads an 8-bit ADC from a National Control Devices (controlanything.com) Ethernet Relay
# PWG 7.15.2014
a=0
RELAY_CMD_CH1="relay_readadc1_8bit.hex"
RELAY_CMD_CH2="relay_readadc2_8bit.hex"
# Update Rate (sec)
UPDATE_TIME=10

# Check input args
if [ $# -ne 2 ]
then
  echo "$0: <ip_addr> <port>"
  echo "Default port is 2101"
  exit
fi

RELAY_IP=$1
RELAY_PORT=$2

while [ "$a"==0 ]; do
 val_ch1=`cat ${RELAY_CMD_CH1} | nc $RELAY_IP $RELAY_PORT | hexdump -v -e '"%d"'` 
 # If no sleep, val_ch2 is empty
 sleep 1
 val_ch2=`cat ${RELAY_CMD_CH2} | nc $RELAY_IP $RELAY_PORT | hexdump -v -e '"%d"'` 
 # Convert 8-bit temperature value
 temp_ch1=`echo "scale=2; ${val_ch1}*5*100/255" | bc -l`
 temp_ch2=`echo "scale=2; ${val_ch2}*5*100/255" | bc -l`
 echo "`date`| ch1 $temp_ch1 deg F,ch2 $temp_ch2 deg F"
 sleep $UPDATE_TIME
done
