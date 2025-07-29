#!/bin/bash
set -e
operator-init.bash
# If a startup delay is set, wait for the specified duration before starting the node
if [[ -n "${NODE_STARTUP_DELAY}" ]]; then
    echo "Delaying node startup by ${NODE_STARTUP_DELAY}"
    sleep "${NODE_STARTUP_DELAY}"
fi

echo "In devnet mode, self-registering with the contract server"
REGISTRATION_DATA=$(RUST_LOG="off,copytradingenclave=error" copy-trading-backend acquire-reg-report)
REGISTRATION_DATA="$(jq '. += {"custodianAddress": env.ETH_SENDER, "applicationId": "copy-trading" }' <<<$REGISTRATION_DATA)"
curl -d "$REGISTRATION_DATA" -X POST -H 'Content-Type: application/json' $CONTRACT_SERVER_URL/register
# Deploy copy trading contracts
copy-trading-backend deploy

# Start the node
echo "Registration completed; running: copy-trading-backend $@"
exec copy-trading-backend $@