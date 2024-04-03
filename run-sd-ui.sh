#!/bin/bash

#run stable diffusion webui for all gpus separate ports
trap "quit_err" ERR

function err() {
  echo -e "\033[0;31mError:$1\033[0m"
}
function quit_err() {
  err "$1"
  read -p 'Press any key to exit.'
}
function open_and_wait(){
  local addr=$1
  local delay=$2
  local open=false
  while [[ $SECONDS -lt $((SECONDS+${delay})) ]]; do
    if wget --spider ${addr} 2>/dev/null; then
      xdg-open "${addr}"
      local open=true
      break
    fi
    sleep 0.2
  done
  if [[ open == false ]]; then
    err "Failed to open ${addr}, timeout ${delay}s (could be installing)."
  fi
}
function run() {
  type nvidia-smi &>/dev/null
  if [[ ! $? ]]; then
    quit_err "nvidia-smi / driver not installed (only Nvidia GPUs for now)"
  else
    gnome-terminal --window --geometry=50x5+100+10 -- bash -c "~/git/aiarttools/gpustatus.sh"
    local gpucount=$(nvidia-smi --query-gpu=gpu_name --format=csv,noheader | wc -l)
    local winyoff=156
    local winysiz=266
    local baseport=7860
    local ip=$(hostname -I | egrep -o "[0-9\.]+" | head -1)
    local urls=[]
    if [[ ! $? ]]; then
      ip=""
      err "could not get ip address of local machine."
    else
      echo "ip=${ip}"
    fi

    #run sdui
    for (( i=0; i<$gpucount; i++ )) ; do
      local port=$(( ${baseport} + ${i} ))
      gnome-terminal --window --geometry=130x12+100+${winyoff} -- bash -c "export CUDA_VISIBLE_DEVICES=0; cd ~/git/stable-diffusion-webui; ./webui.sh --port ${port}"
      local winyoff=$(( ${winyoff} + ${winysiz} ))
      local urls+=("http://${ip}:${port}")
      echo "${urls[$i]}"
    done

    #launch browsers
    if [[ ip != "" ]]; then
      for (( i=0; i<${#urls[@]}; i++ )) ; do
        open_and_wait "${urls[$i]}" "15"
      done
    fi

  fi

}

run

#manual 
#./venv/bin/python3 ./webui.py

