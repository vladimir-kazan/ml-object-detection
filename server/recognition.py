'''
Object Recognition Module
'''

import os
import numpy as np
import tensorflow as tf
from google.protobuf import text_format
from PIL import Image
# local imports
from protos import string_int_label_map_pb2
from setup import CKPT_FULL_PATH

PRE_TRAINED_MODEL = None
LABELS = None

# load pre-trained model
def load_pre_trained_model():
    '''
    Load pre-trained model for object detection
    '''
    detection_graph = tf.Graph()
    # pylint: disable=E1129
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(CKPT_FULL_PATH, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    return detection_graph

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
    print('recognizing' + filename)
    detection_graph = PRE_TRAINED_MODEL
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
            image = Image.open(filename)
            image_np = load_image_into_numpy_array(image)
            image_np_expanded = np.expand_dims(image_np, axis=0)
            (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})

    scores = np.squeeze(scores)
    classes = np.squeeze(classes).astype(np.int32)
    boxes = np.squeeze(boxes)
    print('Probablity = {0:.2f}% that this is a {1}'.format(scores[0] * 100, LABELS[classes[0]]))
    print('Probablity = {0:.2f}% that this is a {1}'.format(scores[1] * 100, LABELS[classes[1]]))
    print(boxes[0])
    print(boxes[1])

    return 'recognized successfully'

if PRE_TRAINED_MODEL is None:
    PRE_TRAINED_MODEL = load_pre_trained_model()



if LABELS is None:
    DESTINATION_FOLDER = UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'datasets')
    PATH_TO_LABELS = os.path.join(DESTINATION_FOLDER, 'data', 'mscoco_label_map.pbtxt')
    NUM_CLASSES = 90

    label_map = string_int_label_map_pb2.StringIntLabelMap()
    with tf.gfile.GFile(PATH_TO_LABELS, 'r') as fid:
        label_map_string = fid.read()
        text_format.Merge(label_map_string, label_map)

    LABELS = { item.id: item.display_name for item in label_map.item }


if __name__ == "__main__":
    print('recognition __main__')
else:
    print('recognition ' + __name__)