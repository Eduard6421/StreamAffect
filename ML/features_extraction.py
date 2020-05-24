import datetime
import glob
import os
import pdb
from io import StringIO

import cv2 as cv
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing.image import img_to_array, load_img
from pyspark.ml.image import ImageSchema
from pyspark.ml.linalg import VectorUDT
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.util import MLUtils
from pyspark.shell import sc, spark
from pyspark.sql import SparkSession
from pyspark.shell import spark, sc
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, DoubleType, FloatType
from utils import emotions
import numpy as np
from sparkdl import KerasImageFileTransformer
from pyspark.ml.classification import LogisticRegression, OneVsRest, OneVsRestModel, SparkContext
from pyspark.mllib.evaluation import MulticlassMetrics

sc.setLogLevel("WARN")


class LogisticRegressionV:

    def __init__(self, model_path=None):
        self.hdfs_dataset = "hdfs://localhost:9000/emotions_dataset/"

        if model_path is None:
            self.data = self.get_train_data()
            print('TRAINNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN')
            self.path_model, self.logistic_model = self.train_model(self.data)
        else:
            self.logistic_model = OneVsRestModel.load(model_path)

    def get_train_data(self):
        # spc = SparkContext.getOrCreate()
        base_folder_features = './dataset/'
        images_path = []

        for key in emotions:
            images_names = glob.glob(os.path.join(base_folder_features + emotions[key] + "/*"))
            i = [(float(key), path_image) for path_image in images_names]
            images_path += i

        transformer = KerasImageFileTransformer(inputCol="uri", outputCol="features",
                                                modelFile='models/vgg16.hdf5',
                                                imageLoader=self.load_data,
                                                outputMode="vector")
        batch_size = 500
        schema = StructType([
            StructField("label", FloatType(), True),
            StructField("features", VectorUDT(), True)])

        features_df = spark.createDataFrame(sc.emptyRDD(), schema)
        # rdd = spc.emptyRDD()
        for i in range(0, len(images_path), batch_size):
            if i + batch_size < len(images_path):
                batch_data = images_path[i: i + batch_size]
            else:
                batch_data = images_path[i:]
            data_df = spark.createDataFrame(batch_data, ["label", "uri"])
            features = transformer.transform(data_df)
            data_frame = features.select("label", "features")
                            # .rdd.map(lambda x: LabeledPoint(x.label, self.l2_norm(x.features)))
            features_df = features_df.unionAll(data_frame)
            # rdd = rdd.union(data_frame)

        rdd = features_df.rdd
        # empty.limit(90000)
        print('=============SAVE FEATURES================')
        MLUtils.saveAsLibSVMFile(rdd, "./dataset/features/")

        base_folder_features = './dataset/features'
        features = glob.glob(os.path.join(base_folder_features, "part*"))

        input_data = spark.read.format("libsvm") \
            .load(features)
        input_data.show(n=10)

        return input_data

    def train_model(self, input_data):
        print('=============SPLIT DATA================')
        splits = input_data.randomSplit([0.70, 0.30])
        train = splits[0]
        test = splits[1]
        train.show()

        print('=============TRAIN MODEL DATA================')
        # instantiate the base classifier.
        lr = LogisticRegression(maxIter=1, tol=1E-6, regParam=0.1, fitIntercept=True)

        # instantiate the One Vs Rest Classifier.
        ovr = OneVsRest(classifier=lr)

        # train the multiclass model.
        ovr_model = ovr.fit(input_data.limit(10))

        # score the model on test data.
        predictions = ovr_model.transform(input_data.limit(10))
        prediction_and_labels = predictions.select(['prediction', 'label']).rdd
        metrics = MulticlassMetrics(prediction_and_labels)
        accuracy = metrics.accuracy

        # save model
        file_name = "LogisticRegression_model_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filepath = "./models/" + file_name + "_" + str(accuracy)
        ovr_model.write().overwrite().save(filepath)
        return filepath, ovr_model

    @staticmethod
    def load_data(uri):
        img = ImageSchema.readImages(uri)
        img = img.select('image.data').collect()
        img = np.reshape(img, (416, 416, 3))
        img = np.array(img, np.uint8)
        img = cv.resize(img, (128, 128))
        img = np.array(img, dtype=np.float32)
        image = np.expand_dims(img, axis=0)

        return preprocess_input(image)

    @staticmethod
    def load_data_predict(image):
        img = np.array(image)
        img = np.reshape(img, (416, 416, 3))
        img = np.array(img, np.uint8)
        img = cv.resize(img, (128, 128))
        img = np.array(img, dtype=np.float32)
        image = np.expand_dims(img, axis=0)

        return preprocess_input(image)

    @staticmethod
    def l2_norm(X):
        l2_norm = np.sqrt(np.sum(X * X, axis=0))
        custom_normalisation = np.true_divide(X, l2_norm)
        return custom_normalisation

    def predict(self, data):
        data = np.reshape(data, (-1, 416, 416, 3))
        transformer = KerasImageFileTransformer(inputCol="image", outputCol="features",
                                                modelFile='models/vgg16.hdf5',
                                                imageLoader=self.load_data_predict,
                                                outputMode="vector")

        schema = StructType([
            StructField("features", VectorUDT(), True)])

        empty_df = spark.createDataFrame(sc.emptyRDD(), schema)
        for image in data:
            image = image.reshape(-1, 416 * 416 * 3)
            image = image.tolist()
            data_df = spark.createDataFrame(map(lambda x: (x,), image), ["image"])
            data_df.show()
            keras_pred_df = transformer.transform(data_df)
            data_frame = keras_pred_df.select("features")
            empty_df = empty_df.unionAll(data_frame)

        empty_df.limit(90000)
        # score the model on test data.
        predictions = self.logistic_model.transform(empty_df)

        # return list of prediction
        predictions = predictions.select(['prediction']).collect()
        return predictions


def load_data_image(uri):
    image = img_to_array(load_img(uri, target_size=(416, 416)))
    return image


# #TRAIN
lg = LogisticRegressionV()
print(lg.data.count())
print(lg.path_model)
lg.data.show()

# PREDICT
# lg = LogisticRegressionV('./models/LogisticRegression_model_20200522-230614_1.0')
# images = []
# paths = ["./dataset/anger/anger154.jpg", "./dataset/happy/happy154.jpg"]
# for i in paths:
#     img = load_data_image(i)
#     images.append(img)
# images = np.array(images)
# prediction = lg.predict(images)
# print(prediction)


# df = np.concatenate([np.random.randint(0,2, size=(1000)), np.random.randn(1000), 3*np.random.randn(1000)+2, 6*np.random.randn(1000)-2]).reshape(1000,-1)
# print(df.shape)


# train = ml.get_train_data()

# images = sc.binaryFiles('./dataset/anger/')
# image_to_array = lambda rawdata: np.asarray(Image.open(StringIO(rawdata)))
# img = images.values().map(image_to_array).toDF().show()
# print(img)
# img = np.reshape(img, (416, 416, 3))
# img = np.array(img, np.uint8)
# cv.imshow('image', img)
# cv.waitKey(0)

# img = ImageSchema.readImages("./dataset/anger/anger154.jpg")
# img = img.select('image.data').collect()
# img = np.reshape(img, (416, 416, 3))
# img = np.array(img, np.uint8)
# cv.imshow('image', img)
# cv.waitKey(0)
