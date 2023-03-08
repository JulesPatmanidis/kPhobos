#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "USE: sudo ./proxy_run.sh <Number of UEs>"
    exit 1
fi

if [ ! -f /local/repository/proxy-setup-complete ]; then
    echo "The Proxy setup has not finished. Please wait"
    exit 0
fi

cd /local/repository/proxy-handover/build


# ./proxy --lte_handover_n_enb [path to enb ips file] [num_UEs] [proxy_ip]
#sudo -E ./proxy --lte_handover $1 192.168.2.1 192.168.2.3 192.168.3.1 192.168.2.2
sudo -E ./proxy --lte_handover_n_enb /local/repository/config/ran/enb_ips.conf $1 192.168.3.1 | tee /local/repository/scripts/ran/proxy.log 2>&1