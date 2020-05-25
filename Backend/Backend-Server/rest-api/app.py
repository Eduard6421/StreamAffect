from flask import Flask
from flask import request
from flask import jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS,cross_origin
from pymongo import MongoClient
from kafka import KafkaProducer
import gridfs
from bson.objectid import ObjectId



import glob
import os
import re
import io
import string
import random
import json
import base64
from pywebhdfs.webhdfs import PyWebHdfsClient
from PIL import Image
import cv2 as cv
import numpy as np
from OpenSSL import SSL



context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
context.use_privatekey_file('server.key')
context.use_certificate_file('server.crt')

MONGODB_HOST = '188.26.164.67:27017'
MONGODB_USER = 'user'
MONGODB_PASSWORD = 'password'
MONGODB_DATABASE = 'mydatabase'
MONGODB_AUTH_MECHANISM = 'SCRAM-SHA-1'

HDFS_HOST = '188.26.164.67'
HDFS_PORT = '9870'
HDFS_USERNAME = 'adria'

KAFKA_HOST = '84.117.81.51'
KAFKA_PORT = '9092'

producer = KafkaProducer(bootstrap_servers=KAFKA_HOST + ':' + KAFKA_PORT)

hdfs = PyWebHdfsClient(host=HDFS_HOST, port=HDFS_PORT, user_name=HDFS_USERNAME)


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

client = MongoClient(MONGODB_HOST,
			username=MONGODB_USER,
			password=MONGODB_PASSWORD,
			authSource=MONGODB_DATABASE,
			authMechanism=MONGODB_AUTH_MECHANISM)
db = client[MONGODB_DATABASE] #Select the database
predictions = db["predictions"] #Select the collection name
images = db["fs.files"]
fs = gridfs.GridFS(db)



def write_image(image_path, image, sentiment=None):

	hdfs.create_file(image_path, image_to_binary(cv.cvtColor(image, cv.COLOR_BGR2RGB)))



def image_to_binary(image):
 	
	pil_im = Image.fromarray(image)
	b = io.BytesIO()
	pil_im.save(b, 'jpeg')
	im_bytes = b.getvalue()
	return im_bytes


def get_image_from_binary(value):

	cmap = {'0': (255,255,255),
	        '1': (0,0,0)}

	data = [cmap[letter] for letter in value]
	img = Image.new('BGR', (8, len(value)//8), "white")
	img.putdata(data)
	
	return img


def read_images():

	names = glob.glob("*.jpg")
	return names


def read_image(image_name):
	return image_name, cv.imread(image_name, cv.IMREAD_COLOR)


def extract_sentiment(image_name):
	return re.search(r"[a-z]*", image_name, re.IGNORECASE).group()


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def get_file_object(file_id):
  out = fs.get(ObjectId(file_id)).read()
  return out  


def get_byte_image(image_path='placeholder.jpg'):
	img = Image.open(image_path, mode='r')
	img_byte_arr = io.BytesIO()
	img.save(img_byte_arr, format='JPEG')
	encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
	return encoded_img



@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_pic():

	nparr = np.fromstring(request.data, np.uint8)
	img = cv.imdecode(nparr, cv.IMREAD_COLOR)

	filename = randomString() + '.jpg'

	image_path = 'inference/' + filename
	write_image(image_path, img)

	string_to_send = 'hdfs://localhost:9000/' + image_path
	producer.send('spark', str.encode(string_to_send))
	producer.flush()


	return jsonify({"status" : "OK"})




@app.route('/list', methods=['GET'])
@cross_origin()
def list_images():


	predictions_list = predictions.find()
	res_arr = []
	for p in predictions_list:

		data = {}

		path = p['img']
		path = path.replace('hdfs://localhost:9000/', '')

		file = hdfs.read_file(path)

		img_name = path.replace('inference/', '')

		if not os.path.exists(img_name):

			f = open(img_name, 'wb')
			f.write(file)
			f.close()

		img = get_byte_image(img_name)
		pred = p['predictions']

		data['image'] = img
		data['predictions'] = pred

		res_arr.append(data)

	return jsonify(res_arr)





if __name__ == "__main__":

	app.run(host='0.0.0.0')


