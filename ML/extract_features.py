from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.util import MLUtils
from pyspark.shell import spark, sc
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array, load_img
import numpy as np
import os
from sparkdl import KerasImageFileTransformer

emotions = {
    "0": "anger",
    "1": "fear",
    "2": "happy",
    "3": "horny",
    "4": "sad"
}


def L2_NORM(X):
    L2_NORM = np.sqrt(np.sum(X * X, axis=0))
    custom_normalisation = np.true_divide(X, L2_NORM)
    return custom_normalisation


def load_data(uri):
    image = img_to_array(load_img(uri, target_size=(128, 128)))
    image = np.expand_dims(image, axis=0)
    return preprocess_input(image)


transformer = KerasImageFileTransformer(inputCol="uri", outputCol="features",
                                        modelFile='models/vgg16.hdf5',
                                        imageLoader=load_data,
                                        outputMode="vector")

root_path = "./dataset/"
data_source = []
for key in emotions:
    emotion_path = root_path + emotions[key] + "/"
    image_names = os.listdir(emotion_path)
    for image_name in image_names:
        data_source.append((key, emotion_path + image_name))

batch_size = 500
yourRDD = sc.emptyRDD()
for i in range(0, len(data_source), batch_size):
    if i + batch_size < len(data_source):
        batch_data = data_source[i: i + batch_size]
    else:
        batch_data = data_source[i:]
    print('==+')
    uri_df = spark.createDataFrame(batch_data, ["label", "uri"])
    keras_pred_df = transformer.transform(uri_df)
    to_save = keras_pred_df.select("label", "features") \
        .rdd.map(lambda x: LabeledPoint(x.label, L2_NORM(x.features)))
    yourRDD = yourRDD.union(to_save)
print('++++++++++++++++++++++++++++++++DAAAAAAAAAAAAAAAAA+++++++++++++++++++++++++++')
# MLUtils.saveAsLibSVMFile(yourRDD, "./dataset/features/")
