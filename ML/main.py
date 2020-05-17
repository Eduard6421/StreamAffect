from ml_tools import ML_Tools
import numpy as np
import cv2 as cv
from pyspark.shell import spark


def main():
    images = spark.read.format("image").load("hdfs://localhost:9000/emotions_dataset/anger/*")
    test_data = images.select('image.data').take(1)[0][0]
    test_image = np.reshape(test_data, (416, 416, 3))
    
    cv.imshow("image", np.array(test_image, np.uint8))
    cv.waitKey(0)
    
    ml_tools = ML_Tools(model_path="checkpoint/VGG16_Hybrid_1365_20200517-042722_0.7704918032786885.hdf5")
    y = ml_tools.predict(data=test_data)
    
    print(y)

if __name__ == "__main__":
    main()
