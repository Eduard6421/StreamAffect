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


MONGODB_HOST = '188.26.164.67:27017'
MONGODB_USER = 'user'
MONGODB_PASSWORD = 'password'
MONGODB_DATABASE = 'mydatabase'
MONGODB_AUTH_MECHANISM = 'SCRAM-SHA-1'

HDFS_HOST = '188.26.164.67'
HDFS_PORT = '9870'
HDFS_USERNAME = 'adria'

KAFKA_HOST = '31.5.104.149'
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

memory = {}

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
	img = cv.resize(img,(416,416))

	filename = randomString() + '.jpg'
	

	cv.imwrite('cdn/'+ filename,img)
	image_path = 'inference/' + filename
	write_image(image_path, img)

	string_to_send = 'hdfs://localhost:9000/' + image_path
	producer.send('spark', str.encode(string_to_send))
	producer.flush()


	return jsonify({"status" : "OK"})





@app.route('/get_ids', methods=['GET'])
@cross_origin()
def get_ids():
	num_images = request.args.get('num_images')

	if(num_images is not None and num_images.isnumeric()):
		num_images = int(num_images)
		if(num_images == -1):
			predictions_list = predictions.find().sort("created_at",-1)
		else:
			predictions_list = predictions.find().sort("created_at",-1).limit(num_images)

	else:
		raise Exception('n-ai pus argumentu bn')

	
	res_arr = []
	for p in predictions_list:

		data = {}

		path = p['img']
		path = path.replace('hdfs://localhost:9000/', '')
		img_name = path.replace('inference/', '')

		data['img_name'] = img_name
		data['created_at'] = p['created_at']

		res_arr.append(data)

	print('returning ')

	return jsonify(res_arr)


@app.route('/get_image', methods=['GET'])
@cross_origin()
def get_image():

	print('Recieved request')

	image_id = request.args.get('image_id')

	composed_path = 'hdfs://localhost:9000/inference/' + image_id + '.jpg'

	predictions_list = predictions.find({'img' : composed_path})
	print('Mongo request finished')
	
	res_arr = []
	for p in predictions_list:

		data = {}

		path = p['img']
		path = path.replace('hdfs://localhost:9000/', '')


		img_name = path.replace('inference/', '')

		if not img_name in memory:
			if not os.path.exists('cdn/'+img_name):
				file = hdfs.read_file(path)
				f = open('cdn'+img_name, 'wb')
				f.write(file)
				f.close()
			print('getting byte img')
			img = get_byte_image('cdn/'+img_name)
			memory[img_name] = img
			print('did byte img')
		else:
			img = memory[img_name]
		
		data['image'] = img
		data['img_name'] = img_name
		data['created_at'] = p['created_at']
		data['predictions_nn'] = p['predictions_nn']
		data['predictions_lr'] = p['predictions_lr']

		res_arr.append(data)

	print('returning ')

	return jsonify(res_arr)





@app.route('/list', methods=['GET'])
@cross_origin()
def list_images():

	print('Recieved request')

	num_images = request.args.get('num_images')


	if(num_images is not None and num_images.isnumeric()):
		num_images = int(num_images)
		if(num_images == -1):
			predictions_list = predictions.find().sort("created_at",-1)
		else:
			predictions_list = predictions.find().sort("created_at",-1).limit(num_images)

	else:
		raise Exception('n-ai pus argumentu bn')


	print('Mongo request finished')
	
	res_arr = []
	for p in predictions_list:

		data = {}

		path = p['img']
		path = path.replace('hdfs://localhost:9000/', '')


		img_name = path.replace('inference/', '')

		if not img_name in memory:
			if not os.path.exists('cdn/'+img_name):
				file = hdfs.read_file(path)
				f = open('cdn/'+img_name, 'wb')
				f.write(file)
				f.close()
			print('getting byte img')
			img = get_byte_image('cdn/'+img_name)
			memory[img_name] = img
			print('did byte img')
		else:
			img = memory[img_name]
		
		data['image'] = img
		data['img_name'] = img_name
		data['created_at'] = p['created_at']
		data['predictions_nn'] = p['predictions_nn']
		data['predictions_lr'] = p['predictions_lr']

		res_arr.append(data)

	print('returning ')

	return jsonify(res_arr)





if __name__ == "__main__":

	app.run(host='0.0.0.0')


