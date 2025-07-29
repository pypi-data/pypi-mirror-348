#!/bin/bash
set -e
operator-init.bash

# If a startup delay is set, wait for the specified duration before starting the node
if [[ -n "${NODE_STARTUP_DELAY}" ]]; then
    echo "Delaying node startup by ${NODE_STARTUP_DELAY}"
    sleep "${NODE_STARTUP_DELAY}"
fi

echo "In devnet mode, self-registering with the contract server"
REGISTRATION_DATA=$(RUST_LOG="off,ddxenclave=error" ddx acquire-reg-report)
REGISTRATION_DATA="$(jq '. += {"custodianAddress": env.ETH_SENDER, "applicationId": "exchange-operator" }' <<<$REGISTRATION_DATA)"
curl -d "$REGISTRATION_DATA" -X POST -H 'Content-Type: application/json' $CONTRACT_SERVER_URL/register

# Start the node
echo "Registration completed; running: ddx $@"
# If USE_HEAPTRACK is set, run the node with heaptrack
if [[ ${USE_HEAPTRACK} ]]; then
    echo "Using heaptrack"
    # get the current hostname
    HOSTNAME=$(hostname)
    # get the timestamp
    TIMESTAMP=$(date +%s)
    # set the environment variable to turn off logging to reduce verbosity and its memory footprint
    export RUST_LOG="off,ddxenclave=error"
    exec heaptrack -o /tmp/heaptrack.${HOSTNAME}.${TIMESTAMP}.gz ddx $@
else
    exec ddx $@
fi
