#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "USE: sudo ./proxy_setup.sh <GitHub Token>"
    exit 1
fi

if [ -f /local/repository/proxy-setup-complete ]; then
    echo "Proxy setup already ran; not running again"
    exit 0
fi

# Install dependencies
sudo apt -y update
sudo apt -y install libsctp-dev

# Move to repository folder
cd /local/repository

# Clone proxy
git clone https://JulesPatmanidis:$1@github.com/JulesPatmanidis/proxy_handover.git
cd proxy_handover/

# Compile proxy
make

# Install byobu
sudo apt install byobu

touch /local/repository/proxy-setup-complete
