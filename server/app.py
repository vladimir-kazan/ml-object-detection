'''
Object recognition module
'''

import os
from flask import Flask, request, redirect, url_for, make_response, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS

# local imports
from recognition import recognize_image

# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'src/uploads')
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
APP = Flask(__name__)
CORS(APP)
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    '''
    Check file extension
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@APP.route('/')
def index():
    '''
    Entry point
    '''
    # response = flask.jsonify({ 'some': 'data' })
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # return response
    response = make_response('Hello world!')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
# {
#         response = 'Hello world!',
#         status = 200,
#         mimetype = 'application/json'
#     }

@APP.route('/upload', methods=['POST'])
def upload_file():
    '''
    POST /upload - handler for file uploading
    '''

    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        full_file_path = os.path.join(APP.config['UPLOAD_FOLDER'], filename)
        APP.logger.info('Save file %s', full_file_path)
        file.save(full_file_path)
        recognize_image(full_file_path)

    # response = make_response()
    response = jsonify(message='File uploaded')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'
    return response
