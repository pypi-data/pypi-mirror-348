#!/bin/bash
set -e
operator-init.bash

# IMPORTANT - The SENDER_PRIVATE_KEY env variable must be visible in this shell
# for the bridge to work with a locked account (like on Goerli or Mainnet).
exec ddx eth-bridge
