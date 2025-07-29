#!/bin/bash
# This script is used to propose a release for the kyc operator
#
# NOTE - For development, this script should be invoked from operator-run.bash or equivalent.
#
set -e
if [[ $PROPOSE != "YES" ]]; then
    exit
fi
# propose release for kyc operator
if RUST_LOG=error kyc identity >kyc_mr.json; then
    echo "Operator identity saved to kyc_mr.json"
else
    echo "Failed to run 'kyc identity'"
    exit 1
fi

MR_ENCLAVE=$(jq -r .mrEnclave kyc_mr.json)

jq -n --arg mrEnclave "$MR_ENCLAVE" --arg isvsvn "0x0000" --arg startingEpochId "$STARTING_EPOCH_ID" '{"mrEnclave":$mrEnclave, "isvsvn": $isvsvn, "startingEpochId":$startingEpochId, "applicationId": "kyc-operator"}' >data.json

curl -X POST http://contract-server:4040/propose-release -H "Content-Type: application/json" -d @data.json

exit
