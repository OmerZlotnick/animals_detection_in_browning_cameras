# %% Imports
import argparse
import json
import sys
import os
import pandas as pd
import glob
import urllib
import tempfile
import cv2 as cv
from PIL import Image
import sys
import torchvision.transforms as T
from tqdm import tqdm

sys.path.append("../computervision-recipes")

import fastai
from fastai.vision import (
    models, to_np, load_learner
)
# pip install progressbar2, not progressbar

# Species classification modules will be imported later

parser = argparse.ArgumentParser()
parser.add_argument('-j', '--json', type=str, required=True, help='path to json, e.g. /home/ofir/Dropbox/pycharm_projects/mammals_cameras/detections/out.json')

# Path to our classification model file.
# If a URL, will be automatically downloaded to a temp folder.
classification_model_path = '/data/species_classification_model'
classification_model_file = 'species_model.pkl'

# This must be True if detection is enabled.  Classification can be run
# on the CPU or GPU.
use_gpu = True

image_sizes = 400

# %% Create the model(s)

print('Loading model')
model = load_learner(classification_model_path, classification_model_file)
labels = model.data.classes
print('Finished loading model')

# %% Classify images
args = parser.parse_args()
path_to_json = args.json
json_f = open(path_to_json, "r")
data = json.load(json_f)
num_of_images = 0
for file in data['images']:
  num_of_images+=1
with tqdm(total = num_of_images) as pbar:
  for file in data['images']:
    pbar.update(1)
    if ('max_detection_conf' in file):
      print("File:", file['file'])
      file_name = file['file']
      base_name = os.path.basename(file_name)
      dir_name = os.path.dirname(file_name)
      lock_file_name = os.path.join(dir_name, "classification_lock_" + base_name)
      # rotated_file_name = os.path.join(dir_name, "transposed_" + base_name)
      txt_file_name = os.path.join(dir_name, "classification_"+os.path.basename(file_name) + '.txt')
      if (not os.path.isfile(txt_file_name)):
        if os.path.exists(lock_file_name):
          print("file is currently processes by another tracker")
        else:
          open(lock_file_name, 'a').close()
          cv_image = cv.imread(file['file'], 0)
          img_w, img_h = cv_image.shape[::-1]
          bboxes=[]
          f = open(txt_file_name, "w")
          for detection in file['detections']:
            if detection['conf']>0.85:
              bbox = detection['bbox'] # in [x_min, y_min, width_of_box, height_of_box]
              bbox[0] *=  img_w
              bbox[1] *= img_h
              bbox[2] = bbox[0]+bbox[2]*img_w
              bbox[3] = bbox[1]+bbox[3]*img_h
              bboxes.append([round(x) for x in bbox])
              image = Image.open(file['file'])
              image = image.convert('RGB')
              left, top, right, bottom = tuple(bbox)
              im1 = image.crop((left, top, right, bottom))  # cam6 - 1122, 1192 or cam4,cam8, (972, 1038)
              img_tensor = T.ToTensor()(im1)
              img_fastai = fastai.vision.Image(img_tensor)
              pred_class, pred_idx, outputs = model.predict(img_fastai)
              # im1.show()
              detection['label'] = str(pred_class)
              detection['label_probability'] = outputs[pred_idx].item()
              print(detection['label'] +" conf:"+str(detection['label_probability']))
              f.write(file_name + "," + detection['label'] + "," + str(detection['label_probability']) + '\n')
          if os.path.exists(lock_file_name):
            os.remove(lock_file_name)
          f.close()

