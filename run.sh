#!/usr/bin/env bash
set -e
check_python(){
    if command -v python3 &> /dev/null; then
        echo "python3"
    elif command -v python &> /dev/null; then
        echo "python"
    else
        exit 1
    fi
}
activate_venv(){
    if [ -f "$VENV_DIR/Scripts/activate" ]; then
        source "$VENV_DIR/Scripts/activate" # Windows (Git Bash/WSL)
    elif [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"  # Linux/MacOS
    else
        echo "Error: Unable to find the activation script in '$VENV_DIR'." >&2
        exit 1
    fi
}
VENV_DIR=${VENV_DIR:-"venv"}
PYTHON_EXISTING=$(check_python)
if [ ! "$PYTHON_EXISTING" ]; then
    echo "There is no Python installed"
    exit 1
elif [ ! -d "$VENV_DIR" ]; then
    "$PYTHON_EXISTING" -m venv "$VENV_DIR"
fi
echo "Activating Venv..."
activate_venv
echo "Installing dependencies..."
pip install -r requirements.txt
ARG=$1
if [ -z "$ARG" ]; then
    echo "Print: .\run.sh Your Request"
    exit 1
else
    echo "Processing the request..."
    python src/search.py "$ARG"
fi
exit 0