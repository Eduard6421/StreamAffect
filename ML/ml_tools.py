import datetime
import pdb
import random
import keras
from keras.backend import set_session
from keras.engine.saving import load_model
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.shell import sc, spark
from pyspark.sql import SparkSession
from utils import emotions
import numpy as np
from pyspark.sql.functions import lit
import tensorflow as tf
from classification_models.scene_model import VGG16_Hybrid_1365
from utils import preprocess_datas, CustomSparkModel


class ML_Tools:

    def __init__(self, model_path=None):
        self.hdfs_dataset = "hdfs://localhost:9000/emotions_dataset/"

        if model_path is None:
            data = self.__get_train_data()
            self.__set_gpu_config()
            self.nn_model = self.train(data)
        else:
            self.__set_gpu_config()
            keras_model = load_model(model_path)
            self.nn_model = CustomSparkModel(keras_model, frequency='batch', mode='synchronous')

    def train(self, data):
        splits = data.randomSplit([0.80, 0.20], random.seed())
        train = splits[0]
        test = splits[1]

        # ---build model---
        estimator = self.__get_estimator()

        # ---train---
        estimator.fit(train, epochs=30, batch_size=32, validation_split=0.1)

        # ---eval---
        predictionAndLabels = test.map(
            lambda lp: (float(np.argmax(estimator.predict(np.expand_dims(lp[0], axis=0)))), float(lp[1])))
        metrics = MulticlassMetrics(predictionAndLabels)
        accuracy = metrics.accuracy
        print("Accuracy: " + str(accuracy))
        print(metrics.confusionMatrix())

        # ---save model---
        file_name = "VGG16_Hybrid_1365_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filepath = "./checkpoint/" + file_name + "_" + str(accuracy) + ".hdf5"
        estimator.save(filepath)

        return estimator

    @staticmethod
    def __get_train_data():
        d = None
        for key in emotions:
            images = spark.read.format("image").load("hdfs://localhost:9000/emotions_dataset/" + emotions[key] + "/*")
            images = images.select("image.data").limit(1000)
            images = images.withColumn("label", lit(float(key)))
            images.show()
            if d is None:
                d = images
            else:
                d = d.unionAll(images)

        d = d.limit(30000)
        data = d.rdd.map(lambda value: (preprocess_data(value.data), float(value.label)))
        return data

    @staticmethod
    def __get_estimator():
        base_model = VGG16_Hybrid_1365(weights='places', include_top=False)
        for layer in base_model.layers:
            layer.trainable = False
        x = keras.layers.GlobalAveragePooling2D()(base_model.output)
        output = keras.layers.Dense(5, activation='softmax')(x)
        model = keras.models.Model(inputs=[base_model.input], outputs=[output])
        adam = keras.optimizers.Adam(lr=0.001)
        model.compile(optimizer=adam, metrics=['accuracy'], loss='sparse_categorical_crossentropy')
        estimator = CustomSparkModel(model, frequency='batch', mode='synchronous')
        return estimator

    @staticmethod
    def __set_gpu_config():
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        config.gpu_options.per_process_gpu_memory_fraction = 0.8
        sess = tf.Session(config=config)
        keras.backend.tensorflow_backend.set_session(sess)

    def predict(self, datas):
        return self.nn_model.predict(preprocess_datas(datas))
