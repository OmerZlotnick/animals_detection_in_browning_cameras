All codes presented here run on the terminal.

1) install miniconda3:
    
    a. go to the directory in which you want to save the miniconda3:
    ```
    cd /data2/omer_zlotnick
    ```
    
    b. download miniconda3 download .sh file from https://repo.anaconda.com/miniconda/Miniconda3-py310_22.11.1-1-Linux-x86_64.sh and move it to the same directory
    ```
    mv ~/Downloads/Miniconda3-latest-Linux-x86_64.sh ./
    ```
    
    c. install miniconda3:
    ```
    bash Miniconda3-latest-Linux-x86_64.sh
    ```
    
    d. when you are asked to approve the directory in which conda will be saved, enter your current directory + "/miniconda3":
    ```
    ./miniconda3
    ```
    
    e. now you have miniconda3 installed, and you can work in conda environments. first, enter the base environment:
    ```
    source ~/.bashrc
    ```
    
 2) initialize megadetector
 
    a. first, we need to download the megadetector from https://github.com/microsoft/CameraTraps/releases/download/v5.0/md_v5a.0.0.pt
    
    b. move to the following directory:
    ```
    cd chapter1/ai_tools
    ```
    
    c. create new directory named 'git'
    ```
    mkdir git
    ```
    
    d. move the megadetector we downloaded to this directory
    ``` 
    mv ~/Downloads/md_v5a.0.0.pt  ./git
    ```
    
    e. now, step by step, run the follwong code to create the needed conda environments:
    ```
    cd git
    git clone https://github.com/ecologize/yolov5/
    git clone https://github.com/Microsoft/cameratraps
    git clone https://github.com/Microsoft/ai4eutils
    cd cameratraps
    conda env create --file environment-detector-mac.yml
    conda activate cameratraps-detector
    export PYTHONPATH="$PYTHONPATH:/data2/omer_zlotnick/chapter1/ai_tools/git/cameratraps:/data2/omer_zlotnick/chapter1/ai_tools/git/ai4eutils:/data2/omer_zlotnick/chapter1/ai_tools//git/yolov5"
    ```

3) using megadetector

    a. first, when we open a new terminal, we need to begin with:
    ```
    cd /data2/omer_zlotnick/chapter1/ai_tools/git/cameratraps
    conda activate cameratraps-detector
    export PYTHONPATH="$PYTHONPATH:/data2/omer_zlotnick/chapter1/ai_tools/git/cameratraps:/data2/omer_zlotnick/chapter1/ai_tools/git/ai4eutils:/data2/omer_zlotnick/chapter1/ai_tools//git/yolov5"
    ```
    
    b. now, we use the run_detector_batch function.
      the following parameters must be given (by order):
      location of the megadetector
      location of the input images
      wanted location for the json output file
    ```
    python detection/run_detector_batch.py "/data2/omer_zlotnick/chapter1/ai_tools/git/md_v5a.0.0.pt" "/data2/omer_zlotnick/chapter1/datasets_for_models/dataset1/raw_images" "/data2/omer_zlotnick/chapter1/datasets_for models/dataset1/md_results/md_results.json" --output_relative_filenames --recursive --checkpoint_frequency 10000
    ```
    
    
    
    
    
    
    
    
    
    
