import time

import pymongo
from ml_tools import ML_Tools
from pyspark import SparkContext
from pyspark.ml.image import ImageSchema
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from logistic_regression.predict import predict


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

        for record in records:
            img = ImageSchema.readImages(record[1])
            img = img.select('image.data').collect()
            images.append(img)

        if len(images) != 0:
            ml_tools = ML_Tools(model_path="checkpoint/VGG16_Hybrid_1365_20200517-042722_0.7704918032786885.hdf5")
            preds_nn = ml_tools.predict(images)
            preds_lr = predict(images, model_path="./models/LogisticRegression_model_vgg_scene_22420200526-124611_0.8001998001998002")

            for i in range(len(preds_nn)):
                mycol.insert({"img": records[i][1], "created_at": str(time.time()),
                              "predictions_nn": {"anger": preds_nn[i].tolist()[0],
                                                 "fear": preds_nn[i].tolist()[1],
                                                 "happy": preds_nn[i].tolist()[2],
                                                 "horny": preds_nn[i].tolist()[3],
                                                 "sad": preds_nn[i].tolist()[4]},
                              "predictions_lr": {"anger": preds_lr[i].tolist()[0],
                                                 "fear": preds_lr[i].tolist()[1],
                                                 "happy": preds_lr[i].tolist()[2],
                                                 "horny": preds_lr[i].tolist()[3],
                                                 "sad": preds_lr[i].tolist()[4]
                                                 }
                              })

    kvs.foreachRDD(handler)
    ssc.start()
    ssc.awaitTermination()


if __name__ == "__main__":
    main()
