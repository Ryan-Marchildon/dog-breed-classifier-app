# Note: uses Python2 for stable compatability with the server stack.

from __future__ import print_function

import os
import json
import sys
import signal
import traceback

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
    
import flask

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn import preprocessing


# PATHS AND GLOBAL VARIABLES

prefix = '/opt/ml/'
MODEL_PATH = os.path.join(prefix, 'model')

CURRENT_MODEL_NAME = 'dbc_stanford_10_23'
FROZEN_MODELS_DIR = MODEL_PATH
INCEPTION_INPUT_TENSOR = 'DecodeJpeg/contents:0'
OUTPUT_TENSOR_NAME = 'output_node' + ':0'

BREEDS = os.path.join(MODEL_PATH, 'breeds.csv')
CLASSES_COUNT = 120

ALLOWED_FILE_EXTENSIONS = set(['jpg', 'jpeg'])


# HELPER FUNCTIONS

# used for loading our stored model into a TF graph
def unfreeze_into_current_graph(model_path, tensor_names):
    with tf.gfile.FastGFile(name=model_path, mode='rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')
        g = tf.get_default_graph()

        tensors = {t: g.get_tensor_by_name(t) for t in tensor_names}

        return tensors

# used to decode predictions into their class labels
def one_hot_label_encoder():
    train_Y_orig = pd.read_csv(BREEDS, dtype={'breed': np.str})
    lb = preprocessing.LabelBinarizer()
    lb.fit(train_Y_orig['breed'])

    def encode(labels):
        return np.asarray(lb.transform(labels), dtype=np.float32)

    def decode(one_hots):
        return np.asarray(lb.inverse_transform(one_hots), dtype=np.str)

    return encode, decode

# checks if a file has an allowed file file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS


# MODEL AND SCORING SERVICE

class ScoringService(object):
    tensors = None
    sess = None
    
    @classmethod
    def get_model(cls):
        
        # load model and new TF session, if not already loaded
        if cls.tensors == None or cls.sess == None:
            with tf.Graph().as_default(), tf.Session().as_default() as sess:

                cls.tensors = unfreeze_into_current_graph(
                    os.path.join(FROZEN_MODELS_DIR, CURRENT_MODEL_NAME + '.pb'),
                    tensor_names=[INCEPTION_INPUT_TENSOR, OUTPUT_TENSOR_NAME])

                cls.sess = sess

        return cls
        
    @classmethod
    def predict(cls, img_raw):
    
        clf = cls.get_model()
    
        _, one_hot_decoder = one_hot_label_encoder()

        probs = clf.sess.run(clf.tensors[OUTPUT_TENSOR_NAME],
                         feed_dict={clf.tensors[INCEPTION_INPUT_TENSOR]: img_raw})

        breeds = one_hot_decoder(np.identity(CLASSES_COUNT)).reshape(-1)

        df = pd.DataFrame(data={'prob': probs.reshape(-1), 'breed': breeds})

        return df.sort_values(['prob'], ascending=False)



# FLASK APP FOR SERVING PREDICTIONS
app = flask.Flask(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    """
    Determine if the container is working and healthy. 
    """
    print('*** Running Health Check', file=sys.stderr)
    
    # health check (can we load the model successfully?)
    health = ScoringService.get_model() is not None  

    status = 200 if health else 404
    return flask.Response(
		response='\n', 
		status=status, 
		mimetype='application/json')



@app.route('/invocations', methods=['POST'])
def transformation():
	"""
	Perform inference on a single image. The input is a raw .jpg file. 

	"""
	print('*** Transformation function invoked.', file=sys.stdout)

	# check that the post request has an attached file
	if 'image' not in flask.request.files:
		print('> Image not found.', file=sys.stdout)
		return flask.Response(
			response='Bad Request: received no image.\n', 
			status=400, 
			mimetype='text/plain')
	else:
		print('> Found an attached image.', file=sys.stdout)

	# check that the attached file has an allowed extension
	img_file = flask.request.files['image']
	if allowed_file(img_file.filename):
		
		print('> File passed extension check.', file=sys.stdout)
		
		# read in the file
		img_raw = img_file.read()

		# obtain prediction
		probs_df = ScoringService.predict(img_raw)

		# convert dataframe to CSV for output
		# (returning only the top 5 most probable classes)
		out = StringIO()
		probs_df[0:5].to_csv(out, header=False, index=False)
		result = out.getvalue()

		return flask.Response(
			response=result, 
			status=200, 
			mimetype='text/csv')

	else:
		print('> Image not in allowed extensions: %s' \
			% ALLOWED_FILE_EXTENSIONS, 
			file=sys.stdout)
		return flask.Response(
			response='Image not of an allowed format. Require one of: %s \n' \
			% ALLOWED_FILE_EXTENSIONS, 
			status=415, 
			mimetype='text/plain')
