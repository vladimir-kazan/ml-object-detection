import os
import six.moves.urllib as urllib
import tarfile

DESTINATION_FOLDER = 'datasets'
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
MODEL_FILE_NAME = '{0}.tar.gz'.format(MODEL_NAME)
MODEL_FULL_PATH = os.path.join(DESTINATION_FOLDER, MODEL_FILE_NAME)
DOWNLOAD_URL = 'http://download.tensorflow.org/models/object_detection/{0}'.format(MODEL_FILE_NAME)
CKPT_FULL_PATH = os.path.join(DESTINATION_FOLDER, MODEL_NAME, 'frozen_inference_graph.pb')


def download_and_extact():
    '''
    Download and extract pretrained model
    '''
    if not os.path.isfile(CKPT_FULL_PATH):
        if not os.path.isfile(MODEL_FULL_PATH):
            # download model archive
            opener = urllib.request.URLopener()
            print('Downloading {0}'.format(DOWNLOAD_URL))
            opener.retrieve(DOWNLOAD_URL, MODEL_FULL_PATH)
        else:
            print('Model archive exists: {0}'.format(MODEL_FULL_PATH))

        # Extract
        tar_file = tarfile.open(MODEL_FULL_PATH)
        for file in tar_file.getmembers():
            file_name = os.path.basename(file.name)
            if 'frozen_inference_graph.pb' in file_name:
                print('Extracting: {0}'.format(file_name))
                tar_file.extract(file_name, DESTINATION_FOLDER)
                print('File saved: {0}'.format(CKPT_FULL_PATH))
    else:
        print('File exists: {0}'.format(CKPT_FULL_PATH))

    assert os.path.isfile(CKPT_FULL_PATH)

if __name__ == '__main__':
    print('setup.py is started')
    download_and_extact()
    print('setup.py is finished')
