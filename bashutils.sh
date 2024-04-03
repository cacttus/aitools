#!/bin/bash
#utils bash and python, venv, .. 

# Globals

if [[ ! -z "${_DEBUG}" ]]; then
  export _DEBUG="1"
fi
if [[ -z "${_PYTHON_EXE}" ]]; then
  export _PYTHON_EXE="python3"
fi
if [[ -z "${_VENV_DIR}" ]]; then
  export _VENV_DIR=".venv"
fi
if [[ -z "${_VENV_REQUIREMENTS}" ]]; then
  export _VENV_REQUIREMENTS="requirements.txt"
fi

# Constants
c_RED='\033[1;31m'
c_CYAN='\033[1;36m'
c_WHITE='\033[0;37m'
C_MAGENTA='\033[1;35m' 
c_NC='\033[0m'

# Utils
function msg() {
  echo -e "${c_WHITE}[Bash][I] $1${c_NC}"
}
function err() {
  echo -e "${c_RED}[Bash][E] $1${c_NC}"
}
function dbg() {
  if [[ -z "${_DEBUG}" ]]; then
    echo -e "${c_CYAN}[Bash][D] $1${c_NC}"
  fi
}
function waitforkey() {
  read -p 'Press any key to exit.'
}
function raise() {
  err "$1"
  #waitforkey
  exit 1
}
function open_url_timeout() {
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
function venv_print_debug() {
  dbg "settings:"
  dbg "_VENV_DIR=${_VENV_DIR}" 
  dbg "_PYTHON_EXE=${_PYTHON_EXE}" 
  dbg "current dir=$(pwd)" 
  dbg "arguments=$@"
}
function start_venv() {
  #create (if not exist) and run python venv
  if [[ ! -d "${_VENV_DIR}" ]]; then
    msg "Making venv '${_VENV_DIR}'"
    "${_PYTHON_EXE}" -m venv "${_VENV_DIR}"
    "${_PYTHON_EXE}" -m pip install -r "${_VENV_REQUIREMENTS}"
  fi
  if [[ -z "${VIRTUAL_ENV}" ]]; then
    if [[ -f "${_VENV_DIR}"/bin/activate ]]; then
      dbg "starting venv '${_VENV_DIR}'"
      source "${_VENV_DIR}"/bin/activate
    else
      raise "Cannot activate python venv, aborting..."
    fi
  else
    msg "python venv already activate: ${VIRTUAL_ENV}"
  fi

  export WORKSPACE_DIR="${VIRTUAL_ENV}/.."
}
function quit_venv() {
  if [[ -z "${VIRTUAL_ENV}" ]]; then
    deactivate
  else
    msg "python venv was not active"
  fi
}
function install_package() {
  if [[ -z "${VIRTUAL_ENV}" ]]; then
    cd "${WORKSPACE_DIR}"
    "pip install $1"
    "pip freeze > requirements.txt"
  else
    msg "python venv was not active"
  fi
}
function join_by {
  local d=${1-} f=${2-}
  if shift 2; then
    printf %s "$f" "${@/#/$d}"
  fi
}
function pyexec() {
  local src=$( join_by '\n' "$@" )
  if [[ -z "${_DEBUG}" ]]; then
    printf "%s\n\n" "src=${src}"
  fi
  "${_PYTHON_EXE}" -c "exec(${src@Q})"
}
function list_installed() {
  msg "installed packages:"
  local src=(
    'import pkg_resources'
    'dists = [str(d).replace(" ","==") for d in pkg_resources.working_set]'
    'for i in dists:'
    '  print(i)'
  )
  pyexec "${src[@]}" #@Q
}