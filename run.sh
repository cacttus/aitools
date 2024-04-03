
# Runs a pyton script in the virtual environment (venv)
fpath="$(dirname $(realpath $0))"
if [[ $(pwd) != "${fpath}" ]]; then
  cd "${fpath}"
fi

source ./bashutils.sh
if [[ -z "${VIRTUAL_ENV}" ]]; then
  start_venv
fi

filename=$1
extension="${filename##*.}"
if [[ "${extension}" != ".py" ]]; then
  filename="${filename%.*}.py"
fi

"${_PYTHON_EXE}" "${filename}"
