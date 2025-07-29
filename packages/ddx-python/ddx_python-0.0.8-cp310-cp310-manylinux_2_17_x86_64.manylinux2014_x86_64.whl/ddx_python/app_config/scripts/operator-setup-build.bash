#!/bin/bash
#

# This is set to the absolute path `Dockerfile.enclave` image, so it's safe the call the script from other directories
if [[ -z $RUST_DIR ]]; then
    export RUST_DIR=$PWD
fi

if [[ "${CONTRACT_DEPLOYMENT}" != "snapshot"  && "${CONTRACT_DEPLOYMENT}" != "hardhat_fork_geth" ]]; then
  echo "Expected CONTRACT_DEPLOYMENT to be 'snapshot' but got '${CONTRACT_DEPLOYMENT}'; aborting to avoid inconsistent state issue"
  exit 1
fi

cd "$RUST_DIR"
pushd ddx-operator
make "${APP_SHARE}"/ddx/libEnclave_u.a "${APP_SHARE}"/ddx/enclave.signed.so
popd

pushd kyc-operator
make "${APP_SHARE}"/kyc/libEnclave_u.a "${APP_SHARE}"/kyc/enclave.signed.so
popd

pushd copy-trading
make "${APP_SHARE}"/copytrading/libEnclave_u.a "${APP_SHARE}"/copytrading/enclave.signed.so
popd

if [[ "$REPORT_TYPE" == "SELF" ]]; then
  REPORT_FEATURE="--features self_ra"
else
  REPORT_FEATURE=""
fi

if [[ "$SGX_MODE" == "sw" ]]; then
  if [[ "$REPORT_TYPE" != "SELF" ]]; then
    echo "Error: The software simulation mode only works with self-signed report!"
    exit 1
  fi
  REPORT_FEATURE+=",sw"
fi

export REPORT_FEATURE
export RUST_BACKTRACE=1
