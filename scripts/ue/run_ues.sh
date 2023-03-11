#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "USE: ./run_ues.sh <Number of UEs> <Number of eNBs>"
    exit 1
fi

helm upgrade -i \
    --set-string num_ues=$1 \
    --set-string num_enbs="$2" \
    ues .