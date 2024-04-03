#!/bin/bash

function color(){
  #thermal color
  local val=$1
  local c='1;37'
  if [[ $(echo "$val >= 95" | bc) == 1 ]]; then
    local c='1;31'
  elif [[ $(echo "$val >= 80" | bc) == 1 ]]; then
    local c='1;31'
  elif [[ $(echo "$val >= 60" | bc) == 1 ]]; then
    local c='1;33'
  elif [[ $(echo "$val >= 40" | bc) == 1 ]]; then
    local c='1;32'
  elif [[ $(echo "$val >= 20" | bc) == 1 ]]; then
    local c='0;37'
  else
    local c='1;37'
  fi

  echo -en "\e["$c"m$val\e[0m"
}

function gpuinf(){
  local id=$1
  local inf=$(nvidia-smi -i=$id --query-gpu=gpu_name,utilization.gpu,utilization.memory,temperature.gpu,memory.used,memory.free --format=csv,noheader)
  local name=$(echo $inf | awk -F , '{print $1}' )
  local gpu=$(echo $inf | awk -F , '{print $2}' | egrep -o '[0-9]+')
  local mem=$(echo $inf | awk -F , '{print $3}' | egrep -o '[0-9]+')
  local temp=$(echo $inf | awk -F , '{print $4}' | egrep -o '[0-9]+')
  local mu=$(echo $inf | awk -F , '{print $4}' | egrep -o '[0-9]+')
  local mf=$(echo $inf | awk -F , '{print $4}' | egrep -o '[0-9]+')
  local gpu=$(color "$gpu")
  local mem=$(color "$mem")
  local temp=$(color "$temp") 

  #\e[1;37\e[0m +10 spaces
  printf "  ..%-9s|  %-4s|  %-16s|  %-16s|  %-17s" "${name: -8}" $id $gpu% $mem% $temp°
}

function run() {
  local llen=0
  echo -e "\e[1;30m    NAME     |  ID  |  GPU  |  MEM  | TEMP\e[0m"
  local gpucount=0
  while true
  do
    local lastgpucount=$gpucount
    local gpucount=$(nvidia-smi --query-gpu=gpu_name --format=csv,noheader | wc -l)
    local outpt=""
    local app=""
    for ((i=0;i<$gpucount;i++)) ; do
      local outpt="$outpt$app$(gpuinf $i)"
      local app="\\n"
    done
        
    #clear
    for ((i=0;i<$lastgpucount;i++)) ; do
      echo -ne "\033[1A\033[0K\r"
    done

    #output
    echo -ne "$outpt\\n"
    sleep 0.5

  done
}

run
