#!/bin/bash
#
# NOTE: for matplotlib must install python3-tk on linux
#   sudo apt install python3-tk
#
#trap ctrl+c  (annoying) use ctrl+z to exit
trap 'echo -en "Use Ctrl+Z or type quit to exit\n>"' INT 
source ./bashutils.sh
msg "*******************************************"
msg "      Setting up PyTorch Environment       "
msg "*******************************************"
start_venv
print_debug
while true; do
  printf "\n\n"
  read -e -p ">" input
  history -s "${input,,}"
  if [[ "${input,,}" == "quit" || "${input,,}" == "exit" ]]; then
    exit 0
  else 
    "${_PYTHON_EXE}" ${input}
  fi
done
quit_venv