#!/bin/bash
# This script proposes a release for the DDX exchange.
#
# NOTE - For development, this script should be invoked from operator-run.bash or equivalent.
#
set -e
if [[ $PROPOSE != "YES" ]]; then
    exit
fi
# propose release for ddx exchange
if RUST_LOG=error ddx identity >release_mr.json; then
    echo "Operator identity saved to release_mr.json"
else
    echo "Failed to run 'ddx identity'"
    exit 1
fi

MR_ENCLAVE=$(jq -r .mrEnclave release_mr.json)

jq -n --arg mrEnclave "$MR_ENCLAVE" --arg isvsvn "0x0000" --arg startingEpochId "$STARTING_EPOCH_ID" '{"mrEnclave":$mrEnclave, "isvsvn": $isvsvn, "startingEpochId":$startingEpochId, "applicationId": "exchange-operator"}' >data.json

curl -X POST http://contract-server:4040/propose-release -H "Content-Type: application/json" -d @data.json

exit
