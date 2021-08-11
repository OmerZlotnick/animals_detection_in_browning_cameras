#!/bin/bash
## make sure you have the gnu parallel package : sudo apt-get install parallel

GPU=$2
N=$1
JSON=$3

# shellcheck disable=SC2051
for ((i=1;i<=$N;i++)); do
    gnome-terminal --tab --title="detector$i" -- /bin/bash -c "export CUDA_VISIBLE_DEVICES=$GPU; python read_temperatures_08-08-2021.py -c=./SVHNClassifier-PyTorch/model-54000.pth -j=$JSON; exec bash;"
done
