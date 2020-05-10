import requests
import shutil
from flask import Flask
from bs4 import BeautifulSoup
import random
import string

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


def contribute_with_image(url,sentiment):
    print(url)
    print(sentiment)
    response = requests.get(url, stream=True)
    with open(sentiment+ '_' + randomString() + '.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

contribute_with_image('https://source.unsplash.com/random/416x416','sad')
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