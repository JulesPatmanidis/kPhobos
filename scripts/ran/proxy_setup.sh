#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "USE: sudo ./proxy_setup.sh <Number of eNBs> <GitHub Token>"
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
#git clone https://JulesPatmanidis:$2@github.com/JulesPatmanidis/proxy-handover.git
#cd proxy-handover/

git clone https://github.com/andrewferguson/phobos-proxy.git
cd phobos-proxy
git checkout target_from_discovery_feature

# Compile proxy
make

# Install byobu
sudo apt install byobu

# 
filename=/local/repository/config/ran/enb_ips.conf
> $filename
for ((i=1;i<=$1;i++)); do
    printf "192.168.1.%d\n" $(($i+1)) >> $filename
done

touch /local/repository/proxy-setup-complete
