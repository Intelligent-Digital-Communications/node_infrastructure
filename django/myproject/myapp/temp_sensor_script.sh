#!/bin/sh

# Reads 8-bit ADC vals from a National Control Devices (controlanything.com) Ethernet Relay
# PWG 7.15.2014
a=0
RELAY_CMD="relay_readadcall_8bit.hex"
# Update Rate (sec)
UPDATE_TIME=10

# Check input args
if [ $# -ne 3 ]
then
  echo "$0: <ip_addr> <port> <chans>"
  echo "Default port is 2101, chan [1,8] separated by commas"
  echo "Ex: $0 rfsn2-rly.vip.gatech.edu 2101 1,2"
  exit
fi

RELAY_IP=$1
RELAY_PORT=$2
CHANS=$3
chan_arr=$(echo $CHANS | tr "," " " )
while [ "$a"==0 ]; do
   # !!! 
   # If you write the result from nc into a variable and then
   # try and hexdump, it leaves off the trailing zeros.  Probably because that's a 
   # c-style string (null) termination
   resp=`cat ${RELAY_CMD} | nc $RELAY_IP $RELAY_PORT | hexdump -v -e '/1 "%02d "'` 
  for chan in $chan_arr; do
    # offset zero-indexed but channel is 1-indexed
    offset=`expr $chan - 1`
    val=`echo $resp | cut -d ' ' -f $chan`
    temp=`echo "scale=2; ${val}*5*100/255" | bc -l`
    # Convert 8-bit temperature value
    echo "`date` | Channel $chan is $temp deg F"
  done
  sleep $UPDATE_TIME
done
