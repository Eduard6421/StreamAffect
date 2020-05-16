import socket
from PIL import Image
import numpy as np

host = 'localhost'
port = 8637

image = Image.open('./sad_ukttewpb.jpg')
image = np.array(image)

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((host, port))
client_socket.sendall(b'./sad_ukttewpb.jpg')
client_socket.close()