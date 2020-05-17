from kafka import KafkaProducer


kafka_host = 'localhost'
kafka_port = '9092'

producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092')

print('going to send messages')
for _ in range(1):
    producer.send('spark', b'hdfs://inference/image_name.jpg')
    producer.flush()
print('sent messages on kafka')


from kafka import KafkaConsumer
consumer = KafkaConsumer('spark', bootstrap_servers='127.0.0.1:9092')
for msg in consumer:
    print (msg)