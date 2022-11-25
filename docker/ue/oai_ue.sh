#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "USE: ./oai_ue.sh <UE ID>"
    exit 1
fi

cd ../../../
source oaienv
cd cmake_targets/ran_build/build/

# Modify the configuration file
UE_IP_ADDR=$(ifconfig eth0 | grep 'inet' | awk '{ print $2}')
sed -i "s/ue_addr/$UE_IP_ADDR/g" ue.conf

cp sim.conf tmp_sim.conf
sed -i "s/CUSTOM_MSIN/$(printf "%010d" $1)/g" tmp_sim.conf # Add the MSIN
../../../targets/bin/conf2uedata -c tmp_sim.conf -o . # Compile SIM
../../../targets/bin/usim -g -c tmp_sim.conf -o .
../../../targets/bin/nvram -g -c tmp_sim.conf -o .
rm tmp_sim.conf

num="$(($1-1))"
./lte-uesoftmodem -O ue.conf --L2-emul 5 --nokrnmod 1 --num-ues 1 --node-number 1 --num-enbs 2 --log_config.global_log_options level,nocolor,time,thread_id | tee ue.log 2>&1

# node_id=2
# sudo -E ./ran_build/build/lte-uesoftmodem -O ../ci-scripts/conf_files/episci/proxy_ue.nfapi.conf --L2-emul 5 \
# --nokrnmod 1 --ue-idx-standalone $node_id --num-ues 1 --node-number $node_id --nsa \
# --log_config.global_log_options level,nocolor,time,thread_id | tee ue_$node_id.log 2>&1