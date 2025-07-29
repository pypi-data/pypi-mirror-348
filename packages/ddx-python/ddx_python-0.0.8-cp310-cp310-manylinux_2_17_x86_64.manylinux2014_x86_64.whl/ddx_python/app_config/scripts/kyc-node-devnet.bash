#!/bin/bash
set -e
operator-init.bash
# If a startup delay is set, wait for the specified duration before starting the node
if [[ -n "${NODE_STARTUP_DELAY}" ]]; then
    echo "Delaying node startup by ${NODE_STARTUP_DELAY}"
    sleep "${NODE_STARTUP_DELAY}"
fi

echo "In devnet mode, self-registering with the contract server"
REGISTRATION_DATA=$(RUST_LOG="off,kycenclave=error" kyc acquire-reg-report)
REGISTRATION_DATA="$(jq '. += {"custodianAddress": env.ETH_SENDER, "applicationId": "kyc-operator" }' <<<$REGISTRATION_DATA)"
curl -d "$REGISTRATION_DATA" -X POST -H 'Content-Type: application/json' $CONTRACT_SERVER_URL/register

# Start the node
echo "Registration completed; running: kyc $@"
exec kyc $@
