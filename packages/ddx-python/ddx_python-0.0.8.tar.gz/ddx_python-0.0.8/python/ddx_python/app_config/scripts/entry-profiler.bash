#!/bin/bash
#
# Prepares the Docker tty shell
#
set -e

/opt/intel/sgx-aesm-service/aesm/aesm_service &

# copy db files to dexlabs
mkdir -p /dexlabs/ddx/etc/
cp /profiler/etc/* /dexlabs/ddx/etc/ 

exec bash --login --i
