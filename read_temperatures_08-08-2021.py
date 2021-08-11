import sys

sys.path.append("SVHNClassifier-PyTorch")
import argparse
import torch
import os

from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from torchvision import transforms

from model import Model
import json
import imutils

import pandas as pd
import cv2 as cv
import numpy as np
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--checkpoint', type=str, required=True, help='path to checkpoint, e.g. ./logs/model-100.pth')
parser.add_argument('-j', '--json', type=str, required=True, help='path to json, e.g. /home/ofir/Dropbox/pycharm_projects/mammals_cameras/detections/out.json')


def _infer(path_to_checkpoint_file, path_to_json):
  model = Model()
  model.restore(path_to_checkpoint_file)
  model.cuda()

  with torch.no_grad():
    #go through the json file
    json_f = open(path_to_json, "r")
    data = json.load(json_f)
    scales_dic = {}
    crops_dic = {}
    image_count = 0
    num_of_images = 0
    for file in data['images']:
      num_of_images+=1
    with tqdm(total = num_of_images) as pbar:
      for file in data['images']:
        image_count+=1
        pbar.update(1)
        print("File:", file['file'])
        file_name = file['file']
        base_name = os.path.basename(file_name)
        dir_name = os.path.dirname(file_name)
        lock_file_name = os.path.join(dir_name, "lock_" + base_name)
        # rotated_file_name = os.path.join(dir_name, "transposed_" + base_name)
        txt_file_name = os.path.join(dir_name, os.path.basename(file_name) + '.txt')
        if (not os.path.isfile(txt_file_name)):
          if os.path.exists(lock_file_name):
            print("file is currently processes by another tracker")
          else:
            open(lock_file_name, 'a').close()
            transform = transforms.Compose([
              transforms.Resize([64, 64]),
              transforms.CenterCrop([64, 64]),
              transforms.ToTensor(),
              transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
            ])
            #file['file'] = '/data/trail_cameras/Alona_21-9-2020/cam4/IMG_0025.JPG'
            #file['file'] = '/data/trail_cameras/Alona_21-9-2020/cam10/IMG_0765.JPG'
            #file['file'] = '/data/trail_cameras/Alona_21-9-2020/cam9/IMG_0453.JPG'
            if (os.path.getsize(file['file'])>100):
              crop_area = crops_dic.get(os.path.dirname(file['file']))
              if (crop_area is None):
                cv_image = cv.imread(file['file'], 0)
                cv_template = cv.imread('/home/ofir/Dropbox/pycharm_projects/digits_recognition/temp_symbol.jpg',0)

                w, h = cv_template.shape[::-1]
                img_w, img_h = cv_image.shape[::-1]

                # Apply template Matching with scale
                scale = scales_dic.get(str(img_h)+"x"+str(img_w), 1.)
                resized = imutils.resize(cv_template, width=int(cv_template.shape[1] * scale))
                w, h = resized.shape[::-1]
                res = cv.matchTemplate(cv_image, resized, cv.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
                match=max_val>0.95
                best_scale=1
                if (not match): #scale does not match
                  print("no match, scaling...")
                  max_match = max_val
                  for scale in np.linspace(0.2, 1.2, 20)[::-1]:
                    resized = imutils.resize(cv_template, width=int(cv_template.shape[1] * scale))
                    w, h = resized.shape[::-1]
                    res = cv.matchTemplate(cv_image, resized, cv.TM_CCOEFF_NORMED)

                    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
                    if (max_match < max_val):
                      max_loc_match = max_loc
                      max_match = max_val
                      best_scale = scale
                      best_w = w
                      best_h = h
                    if (max_val > 0.99):
                      print("new scale found: "+str(scale))
                      break
                  scales_dic[str(img_h)+"x"+str(img_w)] = best_scale
                  w = best_w
                  h = best_h
                  max_loc = max_loc_match

                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)

                #crop
                top= top_left[1]
                bottom = top_left[1] + h
                left = top_left[0] + w
                right = left + 3*w
                crop_area = (left, top, right, bottom)
                crops_dic[os.path.dirname(file['file'])] = crop_area
                # end of finding crop area

              #crop area known - let's find the temperature
              image = Image.open(file['file'])
              image = image.convert('RGB')

              # get crop area from dictionary
              left, top, right, bottom = crop_area
              im1 = image.crop((left, top, right, bottom))
              cv_im1 = cv.cvtColor(np.array(im1), cv.COLOR_RGB2BGR)
              #check that C is not in the cropped area
              scale = scales_dic.get(str(img_h) + "x" + str(img_w), 1.)
              c_template = cv.imread('/home/ofir/Dropbox/pycharm_projects/digits_recognition/C_symbol.jpg')
              resized = imutils.resize(c_template, width=int(c_template.shape[1] * scale))
              res = cv.matchTemplate(cv_im1, resized, cv.TM_CCOEFF_NORMED)
              min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
              top_left = max_loc
              right = top_left[0] #set right to the left of the match
              im2 = im1.crop((0, 0 , right, cv_im1.shape[0]))  # cam6 - 1122, 1192 or cam4,cam8, (972, 1038)
              # Shows the image in image viewer
              #if (not match):
              #  im2.show()
              #  match=True
              im2 = transform(im2)
              images = im2.unsqueeze(dim=0).cuda()

              length_logits, digit1_logits, digit2_logits, digit3_logits, digit4_logits, digit5_logits = model.eval()(images)

              length_prediction = length_logits.max(1)[1]
              digit1_prediction = digit1_logits.max(1)[1]
              digit2_prediction = digit2_logits.max(1)[1]
              digit3_prediction = digit3_logits.max(1)[1]
              digit4_prediction = digit4_logits.max(1)[1]
              digit5_prediction = digit5_logits.max(1)[1]
              if (length_prediction.item()==2):
                temperature = digit1_prediction.item()*10 + digit2_prediction.item()
              else:
                temperature = digit1_prediction.item()
              file['temperature']=temperature
              print('temperature:', temperature)
            else:
              file['temperature'] = -999
            if os.path.exists(lock_file_name):
              os.remove(lock_file_name)
            f = open(txt_file_name, "w")
            f.write(file_name + "," + str(file['temperature']))
            f.close()
        else:
          print("file was already processed")
        #save file every 10,000 images
        #if image_count%10000 == 0:
        #  with open(path_to_json + ".digits.out", "w") as f:
        #    json.dump(data, f, indent=4)
#    with open(path_to_json+".digits.out", "w") as f:
#      json.dump(data, f, indent=4)
    #json_f.truncate()  # remove remaining part

def main(args):
  path_to_checkpoint_file = args.checkpoint
  path_to_input_json = args.json

  _infer(path_to_checkpoint_file, path_to_input_json)

if __name__ == '__main__':
    main(parser.parse_args())
