import datetime
import random
import keras
import tensorflow as tf
import os
from classification_models.keras import Classifiers
from elephas.spark_model import SparkModel, load_spark_model
from keras.backend import set_session
from keras.callbacks import EarlyStopping
from pyspark.shell import spark
import cv2 as cv
import numpy as np
from pyspark.mllib.evaluation import MulticlassMetrics
from classification_models.scene_model import VGG16_Hybrid_1365
vgg16, preprocess_input_vgg = Classifiers.get('vgg16')
resnet18, preprocess_input_resnet = Classifiers.get('resnet18')


n_classes = 5


def load_data(uri):
    image = cv.imread(uri)
    image = cv.resize(image, (224, 224))
    return image.reshape((224, 224, 3))


emotions = {
    "0": "anger",
    "1": "fear",
    "2": "happy",
    "3": "horny",
    "4": "sad"
}
# ---prepare data---
root_path = "./dataset/"
data_source = []
for key in emotions:
    emotion_path = root_path + emotions[key] + "/"
    image_names = os.listdir(emotion_path)
    for image_name in image_names:
        data_source.append((key, emotion_path + image_name))

random.shuffle(data_source)
train_src = spark.createDataFrame(data_source, ["label", "uri"])
train_input = train_src.rdd.map(lambda value: (load_data(value.uri), float(value.label)))
splits = train_input.randomSplit([0.80, 0.15], random.seed())
train = splits[0]
test = splits[1]

# ---config gpu--
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.7
sess = tf.Session(config=config)
set_session(sess)


# ---build model---
class CustomSparkModel(SparkModel):
    @staticmethod
    def get_train_config(epochs, batch_size, verbose, validation_split):
        return {'epochs': epochs,
                'batch_size': batch_size,
                'verbose': 2,
                'callbacks': [earlyStopping],
                'validation_split': validation_split}


base_model = VGG16_Hybrid_1365(weights='places', include_top=False)
for layer in base_model.layers:
    layer.trainable = False
x = keras.layers.GlobalAveragePooling2D()(base_model.output)
output = keras.layers.Dense(n_classes, activation='softmax')(x)
model = keras.models.Model(inputs=[base_model.input], outputs=[output])
adam = keras.optimizers.Adam(lr=0.001)
model.compile(optimizer=adam, metrics=['accuracy'], loss='sparse_categorical_crossentropy')
earlyStopping = EarlyStopping(monitor='val_loss', patience=10, verbose=0, mode='min')
estimator = CustomSparkModel(model, frequency='batch', mode='synchronous')
print(model.summary())

# ---train---
estimator.fit(train, epochs=100, batch_size=32, validation_split=0.1)

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
