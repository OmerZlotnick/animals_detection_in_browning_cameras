#!/bin/bash
## make sure you have the gnu parallel package : sudo apt-get install parallel

GPU=$2
N=$1
JSON=$3

# shellcheck disable=SC2051
for ((i=1;i<=$N;i++)); do
    gnome-terminal --tab --title="classification$i" -- /bin/bash -c "export CUDA_VISIBLE_DEVICES=$GPU; python classify_mammals_daniella_model.py -j=$JSON; exec bash;"
done
