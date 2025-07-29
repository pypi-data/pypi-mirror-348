#!/bin/bash
set -e

cargo install --locked tokio-console
exec tokio-console "$@"
