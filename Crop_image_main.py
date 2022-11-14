#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 13:00:22 2022

@author: thibault
Contain functions to get the bounding box (bbox) from the metadata file
and crop the fish out of the image from the bbox
everything is wrap into a main function executable via
Crop_image_main.py image metadatafile output_crop
"""

import sys
import json
import numpy as np
import argparse
from PIL import Image, ImageFile
import matplotlib.pyplot as plt

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

def Crop(image, bbox, increase=0.05):
    '''
    Crop the image using the bounding box, expected format [left,top,right,bottom] and adding
    an increase in size vertically and horizontally.
    The function will cut off the crop at the boundary of the image if it would otherwise exceed the 
    image boundary

    Parameters
    ----------
    image : PIL image format
        DESCRIPTION. image imported using PIL.Image.open(image_file)
    bbox : list
        DESCRIPTION. list with bbox coordinate format [left,top,right,bottom]
    increase : float, optional
        DESCRIPTION. The default is 0.05. increase of the size of the box around the fish per dimension
        width + 5% and height + 5%

    Returns
    -------
    im1 : image PIL format
        DESCRIPTION. Cropped image

    '''
    
    # 5% increase by default of the bbox, metadata bbox is very tight sometime too tight
    # increase factor in each direction (width height)
    factor = increase/2
    left,top,right,bottom = bbox
   
    #h_increase = int(abs((right-left)*factor))
    #v_increase = int(abs((bottom-top)*factor))
    h_increase = (right-left)*factor
    v_increase = (bottom-top)*factor    
    new_bbox = (left-h_increase, top-v_increase, right+h_increase, bottom+v_increase)
    
    # cutoff the cropping to the original image boundary
    image_limit = (0,0)+image.size
    new_bbox_cutoff_1 = map(np.maximum, new_bbox[0:2], (0,0))
    new_bbox_cutoff_2 = map(np.minimum, new_bbox[2:4], image.size)
    new_bbox = tuple(new_bbox_cutoff_1) + tuple(new_bbox_cutoff_2)
    
    im1 = image.crop(new_bbox) # bbox (left,top,right,bottom)
    return im1

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
    increase : float, optional
        DESCRIPTION. The default is 0.05. increase of the size of the box around the fish per dimension
        width + 5% and height + 5%

    Returns
    -------
    None.

    '''
    

    im = Image.open(image_file)

    bbox = get_bbox(metadata_file)

    if bbox:
        # use the crop function
        im1 = Crop(im, bbox, increase=increase)

    else:
        # if no bounding box detected
        print ("no bounding box available for {}, will return empty cropped image".format(image_file))
        im1 = Image.fromarray(np.zeros(im.size))

    im1.save(output_file)

def argument_parser():
    parser = argparse.ArgumentParser(description='Crop the fish image using bounding bbox from a metadata.json.')
    parser.add_argument('input_image', help='Path of input original fish image. Format JPG image file.')
    parser.add_argument('input_metadata', help='Path of input drexel_metadata_reformatted. Format JSON metadata file.')
    parser.add_argument('output', help='Path of output cropped fish image. Format JPG image file.')
    parser.add_argument('--increase', type=float, default=0.05, 
                        help='size increase apply to the bounding box for cropping (in width and height).Default 0.05. Format float.')
    return parser
    

if __name__ == '__main__':
    
    parser = argument_parser()
    args = parser.parse_args()
    main(args.input_image, args.input_metadata, args.output, increase=args.increase)
        