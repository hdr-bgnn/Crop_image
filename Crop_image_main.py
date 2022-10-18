#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 13:00:22 2022

@author: thibault
Contain functions to get the bounding box (bbox) from the metadata file
and crop the fish out of the image from the bbox
everything is wrap into a main function executable via
python crop_main.py <image> <metadatafile> <output_crop>
"""

import os
import sys
import json
import numpy as np
from PIL import Image, ImageFile
import pandas as pd
from pathlib import Path
ImageFile.LOAD_TRUNCATED_IMAGES = True

def get_bbox(metadata_file):

    f = open(metadata_file)
    data = json.load(f)
    bbox = []

    if 'fish' in data:
        if data['fish']['fish_num']>0:
             bbox = data['fish']['bbox']
             
    return bbox

def main(image_file, metadata_file, output_file, increase=0.05):

    im = Image.open(image_file)

    bbox = get_bbox(metadata_file)

    if bbox:
        # 5% increase by default of the bbox, metadata bbox is very tight sometime too tight
        # increase factor in each direction
        factor = increase/2
        left,top,right,bottom = bbox
        h_increase = int(abs((right-left)*factor))
        v_increase = int(abs((bottom-top)*factor))
        new_bbox = (left-h_increase, top-v_increase, right+h_increase, bottom+v_increase)
        im1 = im.crop(new_bbox) # bbox (left,top,right,bottom)

    else:
        # if no bounding box detected
        print ("no bounding box available for {}, will return empty cropped image".format(image_file))
        im1 = Image.fromarray(np.zeros(im.size))

    im1.save(output_file)

    
def show_usage():
    
    print()
    print(f'Usage : {sys.argv[0]} <original_image.jpg> <metadata.json> <cropped_image.jpg>\n')
    print()

if __name__ == '__main__':
    
    if len(sys.argv) == 4:
        image_file = sys.argv[1]
        metadata_file = sys.argv[2]
        output_file = sys.argv[3]
        main(image_file, metadata_file, output_file)
        
    else:
        show_usage()