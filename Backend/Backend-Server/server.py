import requests
import shutil
import random
import socket
import string
from flask import Flask
from PIL import Image
from bs4 import BeautifulSoup

WEBHDFS_URL = 'http://84.117.81.51:9870/webhdfs/v1/dataset/'

host = 'localhost'
port = 8637

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((host,port))
server_socket.listen(5)

def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            break
    return data

while True:
    try:
        (conn, address) = server_socket.accept()
        image_path = recvall(conn)
        image_path = image_path.decode("utf-8")
        print(image_path)
    except Exception as e:
        print(e)
        print('Recieved wrong formatted path')

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def get_random_image():
    #url = 'https://picsum.photos/416/416'
    url = 'https://source.unsplash.com/random/416x416'
    #response = requests.get(url, stream=True)
    #print(response.url)
    #with open(randomString() + '.jpg', 'wb') as out_file:
    #    shutil.copyfileobj(response.raw, out_file)


#def contribute_with_image(url,sentiment):
    #print(url)
    #print(sentiment)
#    response = requests.get(url, stream=True)
#    with open(sentiment+ '_' + randomString() + '.jpg', 'wb') as out_file:
#        shutil.copyfileobj(response.raw, out_file)
    
#    response = requests.put(WEBHDFS_URL + 'imagine3.jpg',params = {'user.name': 'root','op':'CREATE','overwrite':'true'})
#    location = response.headers['location']
#    response = requests.put()
        
    # now we need to write this file to hdfs


#contribute_with_image('https://source.unsplash.com/random/416x416','sad')


def predict_image(image):

    image = Image.open("sad_ijcthfjl.jpg")



'''
def create_routes(app):
    @app.route('/')
    def index():
        return '<h1>Server running</h1>'

    @app.route('/request-image',methods=['GET'])
    def image_request():


    print('Set Index route')

def __server__():
    
    print('Starting flask server')
    app = Flask('app')
    create_routes(app)
    app.run(debug=True)
    print('Started flask server')

if __name__ == "__main__":
    __server__()
'''