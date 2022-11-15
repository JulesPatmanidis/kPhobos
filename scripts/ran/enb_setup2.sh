#!/bin/bash

if [ -f /local/repository/enb-setup-complete ]; then
    echo "eNB setup already ran; not running again"
    exit 0
fi

# Move to repository folder
cd /local/repository

# Clone repository
git clone https://gitlab.eurecom.fr/oai/openairinterface5g.git

cd openairinterface5g/
# Change branch
git checkout episys-lte-handover
# git checkout develop
source oaienv
cd cmake_targets/

# Build eNB
sudo ./build_oai -I
sudo ./build_oai --eNB

# eNB config
# Backhaul
BACKHAUL_IFACE=$(ip route list 192.168.1.3/24 | awk '{print $3}')
sed -i "s/BACKHAUL_IFACE/$BACKHAUL_IFACE/g" /local/repository/config/ran/enb2.conf

# Fronthaul
FRONTHAUL_IFACE=$(ip route list 192.168.2.3/24 | awk '{print $3}')
sed -i "s/FRONTHAUL_IFACE/$FRONTHAUL_IFACE/g" /local/repository/config/ran/enb2.conf

# Install byobu
sudo apt install byobu

touch /local/repository/enb-setup-complete
# sudo -E ./ran_build/build/lte-softmodem -O /local/repository/config/ran/enb.conf --emulate-l1 --nsa --log_config.global_log_options level,nocolor,time,thread_id | tee eNB.log 2>&1
