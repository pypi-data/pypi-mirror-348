#!/bin/bash
set -e
if [[ -n "$1" ]]; then
    exec "$@"
else
    echo "No argument given; starting interactive shell..."
    # When attached to this shell, standard outputs are captured the Docker log manager.
    exec bash --login -i
fi
