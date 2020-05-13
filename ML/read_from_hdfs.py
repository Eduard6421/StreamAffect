from pyspark.ml.image import ImageSchema
import numpy as np
import cv2 as cv

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('Operation').getOrCreate()
images = spark.read.format("image").load("hdfs://localhost:9000/emotions_dataset/anger/*")

image = images.select("image.data").take(10)[8][0]
image = np.reshape(image, (416, 416, 3))
image = np.array(image, np.uint8)
cv.imshow("image", image)
cv.waitKey(0)
