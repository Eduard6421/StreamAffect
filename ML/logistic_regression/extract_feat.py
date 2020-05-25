import sys

from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.util import MLUtils
from pyspark.shell import spark, sc
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array, load_img
import numpy as np
import os
from sparkdl import KerasImageFileTransformer

sys.path.append(os.getcwd() + '/.')
from classification_models.keras import Classifiers

emotions = {
    "0": "anger",
    "1": "fear",
    "2": "happy",
    "3": "horny",
    "4": "sad"
}

_, preprocess_input_resnet18  = Classifiers.get('resnet18')
_, preprocess_input_vgg_scene = Classifiers.get('vgg16')

def L2_NORM(X):
    L2_NORM = np.sqrt(np.sum(X * X, axis=0))
    custom_normalisation = np.true_divide(X, L2_NORM)
    return custom_normalisation


def load_data(uri):
    image = img_to_array(load_img(uri, target_size=(128, 128)))
    image = np.expand_dims(image, axis=0)
    return preprocess_input(image)

def load_data_resnet(uri):
    image = img_to_array(load_img(uri, target_size=(128, 128)))
    image = np.expand_dims(image, axis=0)
    return preprocess_input_resnet18(image)

def load_data_vgg_scene(uri):
    image = img_to_array(load_img(uri, target_size=(224, 224)))
    image = np.expand_dims(image, axis=0)
    return preprocess_input_vgg_scene(image)

transformer1 = KerasImageFileTransformer(inputCol="uri", outputCol="features",
                                        modelFile='./models/vgg16.hdf5',
                                        imageLoader=load_data,
                                        outputMode="vector")

transformer2 = KerasImageFileTransformer(inputCol="uri", outputCol="features",
                                        modelFile='./models/resnet18.hdf5',
                                        imageLoader=load_data_resnet,
                                        outputMode="vector")

transformer3 = KerasImageFileTransformer(inputCol="uri", outputCol="features",
                                        modelFile='./models/vgg_scene_224.hdf5',
                                        imageLoader=load_data_vgg_scene,
                                        outputMode="vector")
root_path = "./dataset/"
data_source = []
for key in emotions:
    emotion_path = root_path + emotions[key] + "/"
    image_names = os.listdir(emotion_path)
    for image_name in image_names:
        data_source.append((key, emotion_path + image_name))

batch_size = 500
# data_source=data_source[:batch_size]
yourRDD = sc.emptyRDD()
for i in range(0, len(data_source), batch_size):
    if i + batch_size < len(data_source):
        batch_data = data_source[i: i + batch_size]
    else:
        batch_data = data_source[i:]
    uri_df = spark.createDataFrame(batch_data, ["label", "uri"])
    keras_pred_df = transformer3.transform(uri_df)
    keras_pred_df.show()
    to_save = keras_pred_df.select("label", "features") \
        .rdd.map(lambda x: LabeledPoint(x.label, L2_NORM(x.features)))
    yourRDD = yourRDD.union(to_save)

#CHANGE PATH WHEN TRAINING
path_save_vgg = "./dataset/features_vgg/"
path_save_vgg_scene = "./dataset/features_vgg_scene/"
path_save_vgg_scene_dim = "./dataset/features_vgg_scene_224/"
path_save_resnet = "./dataset/features_resnet/"

MLUtils.saveAsLibSVMFile(yourRDD, path_save_vgg_scene_dim)
