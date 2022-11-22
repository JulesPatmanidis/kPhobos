#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "USE: sudo ./proxy_run.sh <Number of UEs>"
    exit 1
fi

if [ ! -f /local/repository/proxy-setup-complete ]; then
    echo "The Proxy setup has not finished. Please wait"
    exit 0
fi

cd /local/repository/oai-lte-5g-proxy-ioulios/build

# ./proxy [options] [num_UEs] enb1_ip enb2_ip ...

sudo -E ./proxy --lte_handover $1 192.168.2.1 192.168.2.3 192.168.3.1 192.168.2.2