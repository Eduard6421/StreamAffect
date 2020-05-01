from pyspark.shell import spark
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array, load_img
import numpy as np
from pyspark.sql.types import StringType
from sparkdl import KerasImageFileTransformer


def load_data(uri):
    image = img_to_array(load_img(uri, target_size=(299, 299)))
    image = np.expand_dims(image, axis=0)
    return preprocess_input(image)


transformer = KerasImageFileTransformer(inputCol="uri", outputCol="predictions",
                                        modelFile='model-full.h5',
                                        imageLoader=load_data,
                                        outputMode="vector")

uri_df = spark.createDataFrame(["./data/plane.jpg"], StringType()).toDF("uri")
uri_df.show()

keras_pred_df = transformer.transform(uri_df)
keras_pred_df.select("uri", "predictions").show()
pred = np.array(keras_pred_df.select('predictions').collect())
print("*" * 100)
print("*" * 100)
print("*" * 100)
print(np.argmax(pred[0]))
print("*" * 100)
print("*" * 100)
print("*" * 100)
