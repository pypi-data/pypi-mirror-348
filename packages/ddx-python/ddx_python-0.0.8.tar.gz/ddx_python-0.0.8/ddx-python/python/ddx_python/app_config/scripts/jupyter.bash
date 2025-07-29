#!/bin/bash
#
# Jupyter notebook entrypoint script
#
set -e

if [ -n "$JUPYTER_PW" ]; then
    PASSWORD_HASH=$(python3 -c "from jupyter_server.auth import passwd; print(passwd('$JUPYTER_PW'))")
    PASSWORD="--ServerApp.password=$PASSWORD_HASH"
else
    PASSWORD="--NotebookApp.token='' --NotebookApp.password=''"
fi

exec jupyter lab --allow-root $PASSWORD --port=8888 --ip=0.0.0.0 --no-browser --ServerApp.base_url=/jupyter --NotebookApp.terminals_enabled=False $@
