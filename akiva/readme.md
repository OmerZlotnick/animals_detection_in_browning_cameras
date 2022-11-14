# running megadetector
1. open commandline
2. insert code to open cameratrap environment

```
conda activate cameratraps-detector
```
3. if not in PycharmProjects enter
```
cd PycharmProjects/
```
4. enter code to choose mega_detector
```
cd mega_detector/
```
5. insert code
```
python run_detector_batch.py md_v4.1.0.pb /data2/loc_12-by\ lower\ seperation ./out_trial.json --recursive --threshold 0.25
```
# notes

/data2/loc_12-by\ lower\ seperation - the path to the folder with the images. make sure to put \ before any spaces

./out_trial.json - the path and name of the output file.dot before indicates to save file in curent folder

--recursive - tells the code to check inside each folder for other folders with images.

--threshold 0.25 - tells the code to keep detections with 25% confidence. 

6. Watching the results in the json file
```
vi detections/out_trial.json
```
write ":q" to exit the vi environment.


