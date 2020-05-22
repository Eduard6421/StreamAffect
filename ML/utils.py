import cv2 as cv
from elephas.spark_model import SparkModel
from keras.callbacks import EarlyStopping
import numpy as np

emotions = {
    "0": "anger",
    "1": "fear",
    "2": "happy",
    "3": "horny",
    "4": "sad"
}


class CustomSparkModel(SparkModel):
    @staticmethod
    def get_train_config(epochs, batch_size, verbose, validation_split):
        return {'epochs': epochs,
                'batch_size': batch_size,
                "shuffle": True,
                'verbose': 2,
                'callbacks': [EarlyStopping(monitor='val_loss', patience=10, verbose=0, mode='min')],
                'validation_split': validation_split}


def load_image_from_path(uri):
    image = cv.imread(uri)
    image = cv.resize(image, (224, 224))
    return image.reshape((224, 224, 3))


def preprocess_datas(datas):
    data = np.reshape(datas, (-1, 416, 416, 3))
    images = np.array(data, np.uint8)

    list_ = []
    for i in range(images.shape[0]):
        list_.append(cv.resize(images[i], (224, 224)))
    return np.array(list_, dtype=np.float32)


def preprocess_data(data):
    data = np.reshape(data, (416, 416, 3))
    image = np.array(data, np.uint8)
    image = cv.resize(image, (224, 224))
    return image.reshape((224, 224, 3))
