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
2) Activate the mammals conda environment (or use option B)
3) Go to the pycharm project folder:
```
cd /home/daniella/PycharmProjects/mega_detector
```
4) Run the model
```
/home/ofir/intel/intelpython3/envs/mammals/bin/python run_tf_detector_batch.py md_v4.1.0.pb /data/trail_cameras/Alona_26-08-2020 detections/out_26-08-2020.json --recursive --threshold 0.25
```
Explenation of the arguments:
md_v4.1.0.pb - the mega detector model.

/data/trail_cameras/Alona_26-08-2020 - the path to the folder with the images.

detections/out_26-08-2020.json - the path and name of the output file.

--recursive - tells the code to check inside each folder for other folders with images.

--threshold 0.25 - tells the code to keep detections with 25% confidence.








