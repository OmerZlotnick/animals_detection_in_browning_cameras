Use the instructions here: to install the megadetector environment:
1. Install conda
```
cd /data
./Miniconda3-latest-Linux-x86_64.sh #run installation
source ~/.bashrc #activate conda
```
2. Download the relevant github repositories as explain here: https://github.com/microsoft/CameraTraps/blob/main/megadetector.md#using-the-model
```
cd ~/PycharmProjects 
git clone https://github.com/Microsoft/cameratraps
git clone https://github.com/Microsoft/ai4eutils
```
3. Install the conda environnment:
```
cd cameratraps
conda env create --file environment-detector.yml
```
