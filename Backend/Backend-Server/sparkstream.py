
import os
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

os.environ['PYSPARK_SUBMIT_ARGS'] = "--jars '/home/eduard/Private/Master/Anul 1/Semestrul 2/Big Data/Dotano/Backend/Backend-Server/spark-streaming-kafka-0-8-assembly_2.11-2.4.5.jar' pyspark-shell"

# Kafka Config
topic = 'spark'
zkQuorum = 'localhost:2181'

sc = SparkContext(appName="SparkConsumer")
ssc = StreamingContext(sc, 5)

kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
lines = kvs.map(lambda x: x[1])
counts = lines.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a+b)
counts.pprint()

ssc.start()
ssc.awaitTermination()