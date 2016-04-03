#!/bin/bash
. ~/sdr/setup_env.sh
echo /home/hflinner3/node_infrastructure-operations/rfsncc/recordings/commands/epoch0.sh >> /home/hflinner3/node_infrastructure-operations/rfsncc/recordings/log.txt
specrec --args=master_clock_rate=25e6 --rate=25e6 --ant=RX2 --time=2 --freq=2406 --gain=50 --ref=gpsdo --metadata=true --segsize=24999936 --file=/home/hflinner3/node_infrastructure-operations/rfsncc/recordings/epoch0.sc16 --starttime="2016-04-03 13:25:00" >> /home/hflinner3/node_infrastructure-operations/rfsncc/recordings/log.txt 2>&1