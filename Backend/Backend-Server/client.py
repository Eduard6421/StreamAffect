import socket
from PIL import Image
import numpy as np

host = 'localhost'
port = 9998

#image = Image.open('./sad_ukttewpb.jpg')
#image = np.array(image)

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((host, port))
client_socket.sendall(b'un mesaj\n')
client_socket.close()
print('sent message')
