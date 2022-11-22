# running megadetector
1. open commandline
2. Insert code to open cameratrap environment

```
conda activate cameratraps-detector
```
3. if not in PycharmProjects enter
```
cd PycharmProjects/
```
4. Enter code to choose mega_detector
```
cd mega_detector/
```
5. Insert code
```
python run_detector_batch.py md_v4.1.0.pb /data2/loc_12-by\ lower\ seperation ./out_trial.json --recursive --threshold 0.25
```
# notes

/data2/loc_12-by\ lower\ seperation - The path to the folder with the images. Make sure to put \ before any spaces.

./out_trial.json - The path and name of the output file. Dot before indicates to save file in curent folder.

--recursive - Tells the code to check inside each folder for other folders with images.

--threshold 0.25 - Tells the code to keep detections with 25% confidence. 

6. Watching the results in the json file
```
vi detections/out_trial.json
```
Write ":q" to exit the vi environment.


# classification model

1. open commandline
2. Insert code to open computer vision environment

```
conda activate computer vision
```
3. if not in PycharmProjects enter
```
cd PycharmProjects/
```
4. Enter code to choose speciesclassification
```
cd SpeciesClassification/
```
4. Insert code
```
python classify_mammals_daniella_model_for_check.py -j ../mega_detector/out_trial_loc_num.json
```

# **notes**
../ - symbol to tell computer to look at one library higher than current one
out_trial_loc_num.json - name of json file, "num" refers to number of location if in file name.

