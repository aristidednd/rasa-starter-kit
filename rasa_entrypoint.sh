#!/bin/bash

set -Eeuo pipefail

function print_help {
    echo "Available options:"
    echo " start  - Start Rasa Action Server"
    echo " help   - Print this help"
    echo " run    - Run an arbitrary command inside the container"
}

# install rasa custom dependencies
if [ -f /app/requirements.txt  ] && [ ! -f /app/.pip ]; then
    echo "Installing pip dependencies"
    pip install -r /app/requirements.txt > /dev/null
    echo "Installed"
    echo "Done" > /app/.pip
fi

# download spacy language models
if [ ! -f /app/.spacy  ];then
    echo "Download spacy model"
    python -m spacy download fr_core_news_md 
    python -m spacy link fr_core_news_md fr
    echo "Done" > /app/.spacy
fi

case ${1} in
    rasa)
        shift
        exec rasa "$@"
        ;;
    *)
        exec rasa "$@"
        ;;
esac