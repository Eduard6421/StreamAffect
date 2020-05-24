import cv2 as cv
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing.image import img_to_array, load_img
from pyspark.ml.linalg import VectorUDT
from pyspark.shell import spark, sc
from pyspark.sql.types import StructType, StructField
import numpy as np
from sparkdl import KerasImageFileTransformer
from pyspark.ml.classification import OneVsRestModel


def load_data_predict(image):
    img = np.array(image)
    img = np.reshape(img, (416, 416, 3))
    img = np.array(img, np.uint8)
    img = cv.resize(img, (128, 128))
    img = np.array(img, dtype=np.float32)
    image = np.expand_dims(img, axis=0)

    return preprocess_input(image)


def predict(data, model_path):
    logistic_model = OneVsRestModel.load(model_path)
    data = np.reshape(data, (-1, 416, 416, 3))

    print(data.shape)
    print("*" * 100)

    transformer = KerasImageFileTransformer(inputCol="image", outputCol="features",
                                            modelFile='./models/vgg16.hdf5',
                                            imageLoader=load_data_predict,
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
    predictions = logistic_model.transform(empty_df)
    predictions = predictions.select(['prediction']).collect()

    list_pred = []
    for pred in predictions:
        new = np.zeros((5))
        new[int(pred[0])] = 1
        list_pred.append(new)
    return list_pred
