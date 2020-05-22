import pymongo
from ml_tools import ML_Tools
import numpy as np
import cv2 as cv
from pyspark import SparkContext
from pyspark.ml.image import ImageSchema
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


def main():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["predictions"]

    topic = 'spark'
    zkQuorum = '84.117.81.51:2181'

    c = SparkContext.getOrCreate()
    ssc = StreamingContext(c, 5)

    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})

    def handler(msg):
        records = msg.collect()
        images = []

        if len(records) != 0:
            ml_tools = ML_Tools(model_path="checkpoint/VGG16_Hybrid_1365_20200517-042722_0.7704918032786885.hdf5")

        for record in records:
            img = ImageSchema.readImages(record[1])
            img = img.select('image.data').collect()
            images.append(img)

        if len(images) != 0:
            preds = ml_tools.predict(images)

            for i in range(len(preds)):
                mycol.insert({"img": records[i][1], "predict": {"anger": preds[i].tolist()[0],
                                                                "fear": preds[i].tolist()[1],
                                                                "happy": preds[i].tolist()[2],
                                                                "horny": preds[i].tolist()[3],
                                                                "sad": preds[i].tolist()[4]}})

    kvs.foreachRDD(handler)
    ssc.start()
    ssc.awaitTermination()


if __name__ == "__main__":
    main()
