'''
Object Recognition Module
'''

import numpy as np
import tensorflow as tf
from google.protobuf import text_format
from PIL import Image
# local imports
from protos import string_int_label_map_pb2
from setup import CKPT_FULL_PATH

def load_image_into_numpy_array(image):
    '''
    Transform an image to np.array
    '''
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

def recognize_image(filename):
    '''
    Detect object in image file
    '''
    print('recognize' + filename)
    return 'recognize'
