import glob
import os
import re
import io
from pywebhdfs.webhdfs import PyWebHdfsClient
from PIL import Image
import cv2 as cv
from kafka import KafkaProducer

kafka_host = 'localhost'
kafka_port = '9092'
producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092')


HOST = '5.12.214.167'
PORT = '9870'
USERNAME = 'adria'

hdfs = PyWebHdfsClient(host=HOST,port=PORT, user_name=USERNAME)


def write_image(image_name, image, sentiment):

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


def main():
	imgs = read_images()
	img_name, img = read_image(imgs[0])
	write_image(img_name, img, extract_sentiment(img_name))
	producer.send('spark',img_name.encode())
	producer.flush()