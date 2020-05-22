from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient


import glob
import os
import re
import io
from pywebhdfs.webhdfs import PyWebHdfsClient
from PIL import Image
import cv2 as cv



HOST = '84.117.81.51'
PORT = '9870'
USERNAME = 'root'

hdfs = PyWebHdfsClient(host=HOST,port=PORT, user_name=USERNAME)


def write_image(image_name, image, sentiment=None):

	#image_path = 'dataset/' + sentiment + '/' + image.name()
	image_path = 'inference/' + image_name

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



app = Flask(__name__)
client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.mymongodb #Select the database
images = db.images #Select the collection name


@app.route('/upload', methods=['POST'])
def upload_pic():
    file = request.files['file']
    filename = secure_filename(file.filename)

    write_image(file, filename)



@app.route('/list', methods=['GET'])
def list_images():

	image_list = images.find()

	return image_list


if __name__ == "__main__":
    app.run()