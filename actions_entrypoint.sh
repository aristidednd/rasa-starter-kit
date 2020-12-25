#!/bin/bash

set -Eeuo pipefail

function print_help {
    echo "Available options:"
    echo " start  - Start Rasa Action Server"
    echo " help   - Print this help"
    echo " run    - Run an arbitrary command inside the container"
}

if [ -f /app/actions/requirements.txt  ] && [ ! -f /app/.pip ]; then
    echo "Installing pip dependencies"
    pip install -r /app/actions/requirements.txt > /dev/null
    echo "Installed"
    echo "Done" > /app/.pip
fi

case ${1} in
    start)
        exec python -m rasa_sdk "${@:2}"
        ;;
    run)
        exec "${@:2}"
        ;;
    *)
        print_help
        ;;
esac