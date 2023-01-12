#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "USE: sudo ./enb_setup.sh <enb_id>"
    exit 1
fi

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


# IDs
sed -i "s/ENB_ID_HEX/0xe0$1/" /local/repository/config/ran/enb.conf # ONLY WORKS FOR < 10 ENBs
sed -i "s/NID_CELL_ID/$1/" /local/repository/config/ran/enb.conf

# Ports
PORT_OFFSET=$(($1 * 2))
sed -i "s/500\(..\)/50$PORT_OFFSET\1/g" /local/repository/config/ran/enb.conf

# IPs
IP_OFFSET=$(($1+2))

BACKHAUL_IFACE=$(ip route list 192.168.1.0/24 | awk '{print $3}')
ENB_BACKHAUL_IP="192.168.1.$IP_OFFSET"

sed -i "s/BACKHAUL_IFACE/$BACKHAUL_IFACE/g" /local/repository/config/ran/enb.conf
sed -i "s/ENB_BACKHAUL_IP/$ENB_BACKHAUL_IP/g" /local/repository/config/ran/enb.conf

MIDHAUL_IFACE=$(ip route list 192.168.2.0/24 | awk '{print $3}')
ENB_MIDHAUL_IP="192.168.2.$IP_OFFSET"

sed -i "s/MIDHAUL/$MIDHAUL_IFACE/g" /local/repository/config/ran/enb.conf
sed -i "s/ENB_MIDHAUL_IP/$ENB_MIDHAUL_IP/g" /local/repository/config/ran/enb.conf


# Install byobu
sudo apt install byobu

touch /local/repository/enb-setup-complete
# sudo -E ./ran_build/build/lte-softmodem -O /local/repository/config/ran/enb.conf --emulate-l1 --nsa --log_config.global_log_options level,nocolor,time,thread_id | tee eNB.log 2>&1
