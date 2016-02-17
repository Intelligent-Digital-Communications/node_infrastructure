#!/bin/bash
BINDIR=/usr/local/bin/RFSNServer
INITD=/etc/init.d
PYSCRIPT=RFSNServer.py
SHSCRIPT=RFSNServer.sh
# Don't need to touch anything below here!
PYPATH=$BINDIR/$PYSCRIPT
SHPATH=$INITD/$SHSCRIPT
mkdir $BINDIR
cp $PYSCRIPT $PYPATH && chmod +x $PYPATH
cp $SHSCRIPT $SHPATH && chmod +x $SHPATH
$SHPATH start 
$SHPATH status
update-rc.d $SHSCRIPT defaults
ls -l /etc/rc?.d/*$SHSCRIPT
