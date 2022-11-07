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

import sys
import json
import numpy as np
import argparse
from PIL import Image, ImageFile

# Some of the image are truncated and trigger an error the follow line solve the problem
ImageFile.LOAD_TRUNCATED_IMAGES = True

def get_bbox(metadata_file):
    '''
    From metadata.json (drexel_metadata_reformatter.py) extract the fish bounding box.
    Version extracting from the reformat see (https://github.com/hdr-bgnn/drexel_metadata_formatter)

    Parameters
    ----------
    metadata_file : string
        location/name of the json file containing the metadata to be extracted.

    Returns
    -------
    bbox : list
        list containing the bbox around the fish [left, top, right, bottom].

    '''

    f = open(metadata_file)
    data = json.load(f)
    bbox = []

    if 'fish' in data:
        if data['fish']['fish_num']>0:
             bbox = data['fish']['bbox']
             
    return bbox

def main(image_file, metadata_file, output_file, increase=0.05):
    '''
    Extract the fish bbox from the metadatafile.json and crop the fish and save the result in outputfile

    Parameters
    ----------
    image_file : string
        DESCRIPTION. filename location of the image .jpg
    metadata_file : string
        DESCRIPTION. filename location of the metadata file .json
    output_file : string
        DESCRIPTION. filename location where to save the cropped image
    increase : int, optional
        DESCRIPTION. The default is 0.05. increase of the size of the box around the fish per dimension
        width + 5% and height + 5%

    Returns
    -------
    None.

    '''
    

    im = Image.open(image_file)

    bbox = get_bbox(metadata_file)

    if bbox:
        # 5% increase by default of the bbox, metadata bbox is very tight sometime too tight
        # increase factor in each direction (width height)
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

def argument_parser():
    parser = argparse.ArgumentParser(description='Crop the fish image from metadata.json.')
    parser.add_argument('input_image', help='Path of input original fish image format JPG image file.')
    parser.add_argument('input_metadata', help='Path of input drexel_metadata_reformatted format JSON metadata file.')
    parser.add_argument('output', help='Path of output cropped fish image format JPG image file.')
    return parser
    
def show_usage():
    
    print()
    print(f'Usage : {sys.argv[0]} <original_image.jpg> <metadata.json> <cropped_image.jpg>\n')
    print()

if __name__ == '__main__':
    
    parser = argument_parser()
    args = parser.parse_args()
    main(args.input_image, args.input_metadata, args.output)
        