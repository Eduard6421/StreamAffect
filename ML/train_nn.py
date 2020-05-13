import datetime
import keras
import tensorflow as tf
import os
from classification_models.keras import Classifiers
from elephas.spark_model import SparkModel, load_spark_model
from keras.backend import set_session
from pyspark.shell import spark
import cv2 as cv

vgg16, preprocess_input = Classifiers.get('vgg16')
n_classes = 5


def load_data(uri):
    image = cv.imread(uri)
    image = cv.resize(image, (224, 224))
    im_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    return preprocess_input(im_rgb).reshape((224, 224, 3))


emotions = {
    "0": "anger",
    "1": "fear",
    "2": "happy",
    "3": "horny",
    "4": "sad"
}

root_path = "./dataset/"
data_source = []
for key in emotions:
    emotion_path = root_path + emotions[key] + "/"
    image_names = os.listdir(emotion_path)
    for image_name in image_names:
        data_source.append((key, emotion_path + image_name))
train_src = spark.createDataFrame(data_source, ["label", "uri"])
train_input = train_src.rdd.map(lambda value: (load_data(value.uri), value.label))

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.05
sess = tf.Session(config=config)
set_session(sess)

# build model
base_model = vgg16(input_shape=(224, 224, 3), weights='imagenet', include_top=False)
x = keras.layers.GlobalAveragePooling2D()(base_model.output)
output = keras.layers.Dense(n_classes, activation='softmax')(x)
model = keras.models.Model(inputs=[base_model.input], outputs=[output])
adam = keras.optimizers.Adam(lr=0.00001)
model.compile(optimizer=adam, metrics=['accuracy'], loss='sparse_categorical_crossentropy')
print(model.summary())
estimator = SparkModel(model, frequency='batch', mode='synchronous')

# train
estimator.fit(train_input, epochs=10, batch_size=32, verbose=2, validation_split=0.15)

# save_model
file_name = "vgg16_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
filepath = "./checkpoint/" + file_name
estimator.save(filepath)

estimator = load_spark_model(filepath)
