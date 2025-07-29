#!/bin/bash
#
# operator-init.bash
# - Ensures required environment variables (APP_SHARE, DEBUG_MODE, SGX_*) are set.
# - Starts the AESM daemon if not running.
# - Seeds Cargo cache and application share if needed.
#
set -e
if [[ -z "$APP_SHARE" ]]; then
  echo "APP_SHARE must be set"
  exit 1
fi
echo "Setting up; PWD=$PWD EUID=$EUID JOBS=${JOBS} APP_SHARE=${APP_SHARE} DEBUG_MODE=${DEBUG_MODE} SGX_PRERELEASE=${SGX_PRERELEASE}"
if [[ "$DEBUG_MODE" -eq 1 ]]; then
  echo "Building in debug mode"
  [[ "$SGX_DEBUG" -ne 1 ]] && {
    echo "SGX_DEBUG should be set"
    exit 1
  }
  [[ "$SGX_PRERELEASE" -eq 1 ]] && {
    echo "SGX_PRERELEASE should not be set"
    exit 1
  }
else
  echo "Building in release mode"
  [[ "$SGX_DEBUG" -eq 1 ]] && {
    echo "SGX_DEBUG should not be set"
    exit 1
  }
fi
all_ps="$(ps aux)"
# Start AESM daemon if not already running.
if [[ ! "${all_ps}" =~ 'aesm_service' ]]; then
  if [[ $EUID -ne 0 ]]; then
    # Background on AESM service issues in Docker: https://gitlab.com/dexlabs/derivadex/-/issues/3872
    # Simplified container-appropriate variant of Intel's initd config: `/opt/intel/sgx-aesm-service/startup.sh`
    sudo -b LD_LIBRARY_PATH=/opt/intel/sgx-aesm-service/aesm/ /opt/intel/sgx-aesm-service/aesm/aesm_service 2>&1 &
    echo "Started AESM service at root"
  else
    /opt/intel/sgx-aesm-service/aesm/aesm_service 2>&1 &
    echo "Started AESM service"
  fi
else
  echo "AESM service is already running"
fi
# If CARGO_HOME is /var/local/cargo (a volume), seed it from /opt/cargo or /root/.cargo to enable cache reuse.
#
if [[ "${CARGO_HOME}" == /var/local/cargo ]]; then
  if [[ -z "$(ls -A /var/local/cargo)" ]]; then
    echo "Bootstrapping cargo cache..."
    if [[ -d /opt/cargo ]]; then
      # Mirror cargo cache from /opt/cargo to /var/local/cargo.
      # Using --delete ensures that extraneous files in the target are removed so that it exactly mirrors the source.
      rsync -a --stats --human-readable --delete --copy-links /opt/cargo/ /var/local/cargo/
    elif [[ -d /root/.cargo ]]; then
      rsync -a --stats --human-readable --copy-links /root/.cargo/ /var/local/cargo/
    else
      echo "No cargo cache found"
    fi
  else
    echo "Re-using cargo cache /var/local/cargo..."
  fi
else
  echo "Using default cargo cache at ${CARGO_HOME}"
fi

# If APP_SHARE equals /var/local/dexlabs, it is a mounted volume.
# Seed it from /dexlabs if empty, allowing dynamic artifact updates without rebuilding.
#
if [[ "${APP_SHARE}" == /var/local/dexlabs ]]; then
  # How emptiness is determined is crucial. Reuse this method for consistency and never use the "-f" switch, as it will always return false for a directory, not a file.
  if [[ -z "$(ls -A /var/local/dexlabs)" ]]; then
    if [[ -n "${BUILD_ON_INIT}" ]]; then
      echo "Building from source; ignoring pre-built artifacts"
      operator-build.bash
    else
      echo "Bootstrapping application share from /dexlabs..."
      rsync -a --stats --human-readable --delete --copy-links --ignore-existing /dexlabs/ /var/local/dexlabs/
    fi
  else
    echo "Re-using application share /var/local/dexlabs..."
  fi
  echo "NOTICE: Manage the 'share' volume to keep it up-to-date."
else
  echo "Using default application share at ${APP_SHARE}"
fi
