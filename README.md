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
python read_temperatures_08-08-2021.py -c=./SVHNClassifier-PyTorch/model-54000.pth -j=/home/daniella/PycharmProjects/mega_detector/detections/out_trial.json
```
Explenation of the arguments:

-c=./SVHNClassifier-PyTorch/model-54000.pth - the digits detector model.
-j=/home/daniella/PycharmProjects/mega_detector/detections/out_trial.json - the json file with the results of the megadetector. 

To run the model in parallel at several terminals:
```
conda activate digits
./run_detector.sh 2 1 out_for_analysis_2-8-21.json 
```
Explenation of the arguments:
1) The number of processes to run in parallel. In this case: 2
2) The GPU number (either 0 or 1) to run the processes. In this case: 1
3) The json file to analyze. In this case: out_for_analysis_2-8-21.json

Output:

The model will a txt output file for each image. The name of the output files will be the name of the input image file + ".txt". 

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
conda activate species_classification
cd /home/daniella/PycharmProjects/SpeciesClassification
python classify_mammals.py -j=/home/daniella/PycharmProjects/mega_detector/detections/out_trial.json.digits.out
```
Explenation of the arguments:

-j=/home/daniella/PycharmProjects/mega_detector/detections/out_trial.json.digits.out - the json file with the results of the megadetector and digits recognition.

Output:

The model will create an output json file. The name of the output file will be the name of the input json file + "species.out". 

## Converting results to table
1) Open the terminal.
2) Run the convert_json_to_table.py script
```
conda activate species_classification
cd /home/daniella/PycharmProjects/SpeciesClassification
python convert_json_to_table.py -j=/home/ofir/Dropbox/pycharm_projects/mammals_cameras/detections/out.json.digits.out.species.out
```
Explenation of the arguments:

-j=/home/ofir/Dropbox/pycharm_projects/mammals_cameras/detections/out.json.digits.out.species.out - the json file with the results of all the models.

Output:

The script will create an output text file. The name of the output file will be the name of the input json file + "table.txt". 









