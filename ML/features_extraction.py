import datetime
import glob
import os
import pdb
import random
import keras
from PIL import Image
from keras.backend import set_session
import cv2 as cv
from keras.engine.saving import load_model
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing.image import img_to_array, load_img
from pyspark import SparkContext
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.mllib.regression import LabeledPoint
from pyspark.shell import sc, spark
from pyspark.sql import SparkSession
from pyspark.shell import spark, sc
from utils import emotions
import numpy as np
from pyspark.sql.functions import lit
import tensorflow as tf
from classification_models.scene_model import VGG16_Hybrid_1365
from utils import preprocess_data, CustomSparkModel
from sparkdl import KerasImageFileTransformer


def load_data(uri):
    sc = SparkContext("local", "First App")
    img = sc.read.format('image').load(uri)
    print(img)
    img = img.select('image.data').take(1)[0][0]
    img = np.array(img)
    img = np.reshape(img, (416, 416, 3))
    # img = np.zeros((128, 128, 3), dtype=np.float32)

    img = np.array(img, np.uint8)
    img = cv.resize(img, (128, 128))
    img = np.array(img, dtype=np.float32)
    # img = Image.fromarray(img)
    # img = img_to_array(img)
    image = np.expand_dims(img, axis=0)

    return preprocess_input(image)

class MlTools:

    def __init__(self, model_path=None):
        self.hdfs_dataset = "hdfs://localhost:9000/emotions_dataset/"

        if model_path is None:
            data = self.get_train_data()
            # self.nn_model = self.train(data)
        else:
            keras_model = load_model(model_path)
            self.nn_model = CustomSparkModel(keras_model, frequency='batch', mode='synchronous')

    def get_train_data(self):
        d = None
        base_folder_features = './dataset/'
        images_path          = []
        for key in emotions:
            # images = spark.read.format("image").load("hdfs://localhost:9000/emotions_dataset/" + emotions[key] + "/*")
            # images = spark.read.format("image").load("./dataset/" + emotions[key] + "/*")
            # images = images.select("image.data").limit(1000)
            # images = images.withColumn("label", lit(float(key)))
            # images.show(n=5)
            # if d is None:
            #     d = images
            # else:
            #     d = d.unionAll(images)
            images_names = glob.glob(os.path.join(base_folder_features + emotions[key] + "/*"))
            i = [(key, path_image) for path_image in images_names]
            images_path += i
        # d = d.limit(30000)
        # data = d.rdd.map(lambda value: (preprocess_data(value.data), float(value.label)))
        # d.collect()
        transformer = KerasImageFileTransformer(inputCol="uri", outputCol="features",
                                                modelFile='models/vgg16.hdf5',
                                                imageLoader=load_data,
                                                outputMode="vector")
        batch_size = 1
        your_rdd = sc.emptyRDD()
        for i in range(0, 1, batch_size):
            if i + batch_size < len(images_path):
                batch_data = images_path[i: i + batch_size]
            else:
                batch_data = images_path[i:]
            data_df = spark.createDataFrame(batch_data, ["label", "uri"])
            keras_pred_df = transformer.transform(data_df)
            keras_pred_df.show()
            to_save = keras_pred_df.select("label", "features") \
                .rdd.map(lambda x: LabeledPoint(x.label, self.l2_norm(x.features)))
            your_rdd = your_rdd.union(to_save)

        return your_rdd
    @staticmethod
    def l2_norm(X):
        l2_norm = np.sqrt(np.sum(X * X, axis=0))
        custom_normalisation = np.true_divide(X, l2_norm)
        return custom_normalisation

    # @staticmethod

    def predict(self, data):
        return self.nn_model.predict(np.expand_dims(preprocess_data(data), axis=0))

ml = MlTools()
# train = ml.get_train_data()

# img = spark.read.format('image').load('./dataset/anger\\anger154.jpg')
# img = img.select('image.data').take(1)[0][0]
# img = np.reshape(img, (416, 416, 3))
# img = np.array(img, np.uint8)
# cv.imshow('image', img)
# cv.waitKey(0)


