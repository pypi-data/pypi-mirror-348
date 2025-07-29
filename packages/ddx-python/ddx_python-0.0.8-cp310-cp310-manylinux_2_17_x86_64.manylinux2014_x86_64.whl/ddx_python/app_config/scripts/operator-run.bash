#!/bin/bash
set -e

if [[ -n "${INIT_SILENT}" ]]; then
    operator-init.bash >/dev/null 2>&1
else
    operator-init.bash
fi

if [[ "$1" = "-c" ]]; then
    shift
    if [[ -z "${INIT_SILENT}" ]]; then
        echo "INFO Setup complete; executing in new shell: $@"
    fi
    exec bash -c "$@"
elif [[ "$1" = "-il" ]] || [[ "$1" = "-li" ]]; then
    echo "INFO Setup complete; opening interactive login shell"
    exec bash -i -l
else
    if [[ $# -eq 0 ]]; then
        if [[ -z "${INIT_SILENT}" ]]; then
            echo "INFO Setup complete; no command provided"
        fi
        exit 0
    fi
    if [[ -z "${INIT_SILENT}" ]]; then
        echo "INFO Setup complete; executing: $@"
    fi
    exec "$@"
fi
