#!/bin/bash

source "./bashutils.sh"

function run_sdui() {
  type nvidia-smi &>/dev/null
  if [[ $? ]]; then
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
        dbg "got here"
        open_url_timeout "${urls[$i]}" "60"
      done
    fi
  else
    raise "nvidia-smi / driver not installed (only Nvidia GPUs for now)"
  fi
}

run_sdui


