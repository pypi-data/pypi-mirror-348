#!/bin/bash
#
# operator-build.bash
# Builds the DDX Operator and its dependencies.
# Use -m to build only the ddx-python module.
#
set -e

MATURIN_ONLY=false

while getopts ":m" opt; do
  case $opt in
  m)
    MATURIN_ONLY=true
    echo "Only building the ddx-python module, skipping the operator"
    ;;
  \?)
    echo "Usage: operator-build.bash [-m]" >&2
    echo "  -m  Only build the ddx-python module" >&2
    exit 1
    ;;
  esac
done
shift $((OPTIND - 1))

function extract_features {
  local crate="$1"
  local filtered_features=""

  # Extract relevant features for the given crate from EXTRA_FEATURES.
  features="$(../extract_features.bash "$(cargo feature "$crate")")"

  # Filter features based on EXTRA_FEATURES. Ignore console if it is included as it is an App only feature
  for feature in $EXTRA_FEATURES; do
    if [[ " $features " == *" $feature "* ]]; then
      filtered_features+="$feature "
    fi
  done

  # Remove trailing space and convert to comma-separated format
  filtered_features="${filtered_features// /,}"
  # Trim any leading or trailing commas
  filtered_features="${filtered_features%,}"
  filtered_features="${filtered_features#,}"

  # Output the result if not empty
  if [[ -n "$filtered_features" ]]; then
    echo "Using $crate features $filtered_features" >&2
    echo "$filtered_features"
  else
    echo ""
  fi
}

if $MATURIN_ONLY; then
  echo "MATURIN_ONLY flag set: skipping full operator build; building only ddx-python."
else
  if [[ -z "$APP_SHARE" ]]; then
    echo "APP_SHARE must be set"
    exit 1
  fi
  echo "Begin build; JOBS=${JOBS} APP_SHARE=${APP_SHARE} DEBUG_MODE=${DEBUG_MODE} SGX_PRERELEASE=${SGX_PRERELEASE} EXTRA_FEATURES=${EXTRA_FEATURES}"
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

  pushd ddx-operator
  # Build sysroot: verify SGX_SYSROOT, clear its directory, and run make sysroot.
  if [[ -z "${SGX_SYSROOT}" ]]; then
    echo "SGX_SYSROOT must be set"
    exit 1
  fi
  if [[ -d "${SGX_SYSROOT}" ]]; then
    echo "Truncating sysroot ${SGX_SYSROOT}..."
    rm -rf "${SGX_SYSROOT}"/*
  fi
  echo "Building sysroot target into ${SGX_SYSROOT}..."
  make sysroot

  if [[ -d "${APP_SHARE}/ddx" ]]; then
    echo "Truncating share directory ${APP_SHARE}/ddx..."
    rm -rf "${APP_SHARE}/ddx"/*
  fi
  # Build ddx-operator: clear share directory and run make.
  echo "Building ddx-operator..."
  make
  popd

  pushd kyc-operator
  if [[ -d "${APP_SHARE}/kyc" ]]; then
    echo "Truncating share directory ${APP_SHARE}/kyc..."
    rm -rf "${APP_SHARE}/kyc"/*
  fi
  # Build kyc-operator: clear share and run make.
  echo "Building kyc-operator..."
  make
  popd

  pushd copy-trading
  if [[ -d "${APP_SHARE}/copytrading" ]]; then
    echo "Truncating share directory ${APP_SHARE}/copytrading..."
    rm -rf "${APP_SHARE}/copytrading"/*
  fi
  # Build copy-trading: clear share and run make.
  echo "Building copy-trading..."
  make
  popd

  pushd ddx-wasm
  # Extract wasm features
  WASM_FEATURES=$(extract_features "ddx-wasm")

  # Build wasm targets
  mkdir -p "${APP_SHARE}/ddx/ddx-wasm"
  if [[ "$DEBUG_MODE" -eq 1 ]]; then
    echo "Building ddx-wasm in debug mode..."
    wasm-pack build --target bundler --scope derivadex -d "${APP_SHARE}/ddx/ddx-wasm/bundler" -- --features="${WASM_FEATURES}"
    wasm-pack build --target nodejs --scope derivadex -d "${APP_SHARE}/ddx/ddx-wasm/nodejs" -- --features="${WASM_FEATURES}"
    wasm-pack build --target web --scope derivadex -d "${APP_SHARE}/ddx/ddx-wasm/web" -- --features="${WASM_FEATURES}"
  else
    echo "Building ddx-wasm in release mode..."
    wasm-pack build --release --target bundler --scope derivadex -d "${APP_SHARE}/ddx/ddx-wasm/bundler" -- --no-default-features --features="${WASM_FEATURES}"
    wasm-pack build --release --target nodejs --scope derivadex -d "${APP_SHARE}/ddx/ddx-wasm/nodejs" -- --no-default-features --features="${WASM_FEATURES}"
    wasm-pack build --release --target web --scope derivadex -d "${APP_SHARE}/ddx/ddx-wasm/web" -- --no-default-features --features="${WASM_FEATURES}"
  fi
  # Workaround: update package.json main field; review after upgrading wasm-pack or bundler.
  jq '. | .main = "ddx_wasm.js"' "${APP_SHARE}/ddx/ddx-wasm/bundler/package.json" >tmp && mv tmp "${APP_SHARE}/ddx/ddx-wasm/bundler/package.json"
  popd
fi

if [[ -z "${CONDA_PREFIX}" ]]; then
  echo "CONDA_PREFIX must be set to enable maturin to find the Python environment"
  exit 1
fi

pushd ddx-python
# Extract Python features
PYTHON_FEATURES=$(extract_features "ddx-python")

# For now, disable the maturin import hook for dev installs
# Dev installs don't work correctly for mixed rust/python projects
# pip install maturin_import_hook
# python -m maturin_import_hook site install

# Build and install ddx-python:
# - Extract features and build with maturin.
# - Install the extension via pip.
echo "Building and installing ddx-python; MATURIN_INTERPRETER=${MATURIN_INTERPRETER} CONDA_PREFIX=${CONDA_PREFIX} PYTHON_FEATURES=${PYTHON_FEATURES} JOBS=${JOBS}"

WHLDIR=$(mktemp -d /tmp/ddx_python.XXXXXX)
trap "rm -rf $WHLDIR" EXIT
if [[ ${DEBUG_MODE} = 1 ]]; then
  maturin build --interpreter "${MATURIN_INTERPRETER}" -F "${PYTHON_FEATURES}" -j "${JOBS}" -o "$WHLDIR"
else
  maturin build --no-default-features --interpreter "${MATURIN_INTERPRETER}" -F "${PYTHON_FEATURES}" --release -j "${JOBS}" -o "$WHLDIR"
fi
pip --disable-pip-version-check install --no-deps --force-reinstall --no-index --find-links="$WHLDIR" ddx-python
popd
