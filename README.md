# Animals Detection in Browning Cameras

The first step is to run the megadetector on each image. Next, you can run the temperature recognition model and the species classification model.

## Install the conda environments
To export an environment:
```
conda activate mammals
conda env mammals > /data/mammals.yml
conda activate digits
conda env digits > /data/digits.yml
conda activate species_classification
conda env species_classification > /data/species_classification.yml
```
To import an environment:
```
conda env update --name mammals --file /data/mammals.yml
conda env update --name digits --file /data/digits.yml
conda env update --name species_classification --file /data/species_classification.yml
```
Option B - use the path to the environments that exists in ofir home directory
for mammals, use `/home/ofir/intel/intelpython3/envs/mammals/bin/python`
for digits, use `/home/ofir/intel/intelpython3/envs/digits/bin/python`
for species_classification, use `/home/ofir/intel/intelpython3/envs/species_classification/bin/python`



## Running the detection model

1) Open the terminal.
2) Activate the mammals conda environment.
3) Go to  the 
