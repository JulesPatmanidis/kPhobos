#!/bin/bash

if [ ! -f /local/repository/enb-setup-complete ]; then
    echo "The eNB setup has not finished. Please wait"
    exit 0
fi

cd /local/repository/openairinterface5g/
source oaienv
cd cmake_targets/

#sudo -E ./ran_build/build/lte-softmodem -O ../ci-scripts/conf_files/episci/proxy_rcc.band7.tm1.nfapi.conf \
# --noS1 --node-number 1 --emulate-l1 \
# --log_config.global_log_options level,nocolor,time,thread_id --log_config.global_log_level debug | tee ~/logs/eNB1.log 2>&1 &


sudo -E ./ran_build/build/lte-softmodem -O /local/repository/config/ran/enb.conf --emulate-l1 --node_number 1 \
--log_config.global_log_options level,nocolor,time,thread_id | tee /local/repository/scripts/ran/eNB.log 2>&1