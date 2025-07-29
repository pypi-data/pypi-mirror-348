#!/bin/bash
set -e

# Install wget and add Google Chrome repository
echo "Installing wget and adding Google Chrome repository..."
apt update
apt install -y wget gnupg
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome
echo "Installing Google Chrome..."
apt update
apt install -y google-chrome-stable

echo 'Waiting for node0 to reach the Master state...'
until curl -s "${LEADER_URL}/status" |rg Master; do
    echo 'Still waiting for node0...'
    sleep 6s
done
echo "Cluster ready; running cypress $@"
cd /usr/src/packages/frontend-spa
yarn run cypress install
exec yarn run cypress $@ --browser chrome
