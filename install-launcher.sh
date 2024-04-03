#!/bin/bash

# run this to install desktop icon

installdir=$(pwd)
dfile="[Desktop Entry]"
dfile="${dfile}\nName=aiarttools"
dfile="${dfile}\nExec=${installdir}/run-sd-ui.sh"
dfile="${dfile}\nTerminal=false"
dfile="${dfile}\nIcon=${installdir}/icon.png"
dfile="${dfile}\nType=Application"
dfile="${dfile}\nName[en_US]=aiarttools"
echo -e ${dfile} > ~/Desktop/aiarttools.desktop
chmod +x ~/Desktop/aiarttools.desktop

