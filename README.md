# Animals Detection in Browning Cameras

The first step is to run the megadetector on each image. Next, you can run the temperature recognition model and the species classification model.

## Install the conda environments
To export an environment:
```
conda env export --name mammals > /data/mammals.yml
conda env export --name digits > /data/digits.yml
conda env export --name species_classification > /data/species_classification.yml
```
To import an environment:
```
conda env create --file /data/mammals.yml
conda env create --file /data/digits.yml
conda env create --file /data/species_classification.yml
```
To copy python project from a uset to another user:
```
sudo cp -r /home/ofir/Dropbox/pycharm_projects/digits_recognition /home/daniella/PycharmProjects/.
sudo chown -R daniella /home/daniella/PycharmProjects/SpeciesClassification
```

## Running the temperature detection model

1) Open the terminal.
2) Run the model
```
conda activate mammals
cd /home/daniella/PycharmProjects/mega_detector
python run_tf_detector_batch.py md_v4.1.0.pb /data2/Daniella_camera_traps_cont/Alona2_May/cam_23 detections/out_trial.json --recursive --threshold 0.25
```
Explenation of the arguments:
md_v4.1.0.pb - the mega detector model.

/data2/Daniella_camera_traps_cont/Alona2_May/cam_23 - the path to the folder with the images.

detections/out_trial.json - the path and name of the output file.

--recursive - tells the code to check inside each folder for other folders with images.

--threshold 0.25 - tells the code to keep detections with 25% confidence.
3) Watching the results in the json file
```
vi detections/out_trial.json
```
write ":q" to exit the vi environment.

## Running the detection model
1) Open the terminal.
2) Run the model
```
conda activate digits
cd /home/daniella/PycharmProjects/digits_recognition
python read_temperatures_08-08-2021.py -c=./SVHNClassifier-PyTorch/model-54000.pth -j=/home/daniella/PycharmProjects/mega_detector/detections/out_for_analysis_2-8-21.json
```
Explenation of the arguments:

-c=./SVHNClassifier-PyTorch/model-54000.pth - the digits detector model.

-j=/home/daniella/PycharmProjects/mega_detector/detections/out_trial.json - the json file with the results of the mega-detector. 

To run the model in parallel at several terminals:
```
conda activate digits
./run_detector_digits.sh 2 1 out_for_analysis_2-8-21.json 
```
Explenation of the arguments:
1) The number of processes to run in parallel. In this case: 2
2) The GPU number (either 0 or 1) to run the processes. In this case: 1
3) The json file to analyze. In this case: out_for_analysis_2-8-21.json

Output:

The model will write a text output file for each image. The name of the output files will be the name of the input image file + ".txt". 

To collect the files into one big file, open the terminal in the main folder of the images. For example:
```
cd /home/daniella/PycharmProjects/mega_detector/for_analysis
```
Then, use the 'find' and 'cat' commands to concatonate all txt files into one file:
```
# add end-of-line to each file if it's missing
find . -name "*.txt" -exec sed -i -e '$a\' {} +
# create a file temperatures.txt from all the files
find . -name "*.txt" -exec cat > temperatures.txt {} +
```

## Running the classification model

1) Open the terminal.
2) Run the model
```
conda activate computer_vision
cd /home/daniella/PycharmProjects/SpeciesClassification
python classify_mammals_daniella_model.py -j=/home/daniella/PycharmProjects/mega_detector/detections/out_for_analysis_2-8-21.json
```
Explenation of the arguments:

-j=/home/daniella/PycharmProjects/mega_detector/detections/out_trial.json - the json file with the results of the mega-detector. 

To run the model in parallel at several terminals:
```
conda activate computer_vision
./run_detector_classification.sh 2 1 out_for_analysis_2-8-21.json 
```
The arguments passed to `run_detector_classification.sh` have the same meaning as for the `run_detector_digits.sh` bash script.

Output:

The model will write a text output file for each image. The name of the output files will be "classification_" + the name of the input image file + ".txt". 

To collect the files into one big file, open the terminal in the main folder of the images. For example:
```
cd /home/daniella/PycharmProjects/mega_detector/for_analysis
```
Then, use the 'find' and 'cat' commands to concatonate all txt files into one file:
```
# add end-of-line to each file if it's missing
find . -name "classification_*.txt" -exec sed -i -e '$a\' {} +
# create a file temperatures.txt from all the files
find . -name "classification_*.txt" -exec cat > classifications.txt {} +
```




