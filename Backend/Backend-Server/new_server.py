import socket
import threading
import time

from pyspark import SparkContext
from pyspark.streaming import StreamingContext


message_host = 'localhost'
message_port = 9998

spark_host = 'localhost'
spark_port = 9999

def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            break
    return data

def tcp_server(host,port):
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((host,port))
    server_socket.listen(5)
    return server_socket

def spark_server():
    sc = SparkContext("local[2]","Spark Streaming Image Read")
    ssc = StreamingContext(sc, 5)
    return ssc

def run_message_broker(message_server,spark_server):
    while True:
        try:
            (conn, address) = message_server.accept()
            image_path = recvall(conn)
            conn.close()
            print('closed connection')
            #image_path = image_path.decode("utf-8")
        except Exception as e:
            print(e)
            print('Recieved wrong formatted path')


def run_spark_server(ssc):
    lines = ssc.socketTextStream(host, port)
    lines.pprint()
    ssc.start()
    ssc.awaitTermination()


message_host = 'localhost'
message_port = 9998

spark_host = 'localhost'
spark_port = 9999



def main():

    print('Setting up message reciever TCP server')
    message_server_socket = tcp_server(message_host,message_port)
    print('Finished setting up message reciever TCP server')

    print('Setting up message reciever TCP server')
    spark_server_socket = tcp_server(spark_host,spark_port)
    print('Finished setting up message reciever TCP server')

    broker_thread = threading.Thread(target=run_message_broker,args=(message_server_socket,spark_server_socket))
    broker_thread.start()

    print('Setting up spark server')
    time.sleep(5)
    spark_worker = spark_server()
    spark_server_thread = threading.Thread(target=run_spark_server,args=(spark_worker,))
    spark_server_thread.start()
    print('Finished setting up spark server')

main()