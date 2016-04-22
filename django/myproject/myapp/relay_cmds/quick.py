import os, subprocess
hostname = 'rfsn-demo1-rly.vip.gatech.edu'
port = '2101'
mine, mine2 = subprocess.Popen(['./rfsn_ctl', hostname, port, 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
print("PRINTING")
print(mine)
#print(mine2)
