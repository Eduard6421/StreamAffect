import glob
import os
from datetime import datetime

from pyspark.ml.classification import LogisticRegression, OneVsRest
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.shell import spark

base_folder_features = '../dataset/features'
features = glob.glob(os.path.join(base_folder_features, "part*"))

inputData = spark.read.format("libsvm") \
    .load(features)

inputData.show(n=10)


def train_model(input_data):
    splits = input_data.randomSplit([0.70, 0.30])
    train = splits[0]
    test = splits[1]
    train.show()

    # instantiate the base classifier.
    lr = LogisticRegression(maxIter=10, tol=1E-6, regParam=0.1, fitIntercept=True)

    # instantiate the One Vs Rest Classifier.
    ovr = OneVsRest(classifier=lr)

    # train the multiclass model.
    ovr_model = ovr.fit(train)

    # score the model on test data.
    predictions = ovr_model.transform(test)
    prediction_and_labels = predictions.select(['prediction', 'label']).rdd
    metrics = MulticlassMetrics(prediction_and_labels)
    accuracy = metrics.accuracy

    # save model
    file_name = "LogisticRegression_model_" + datetime.now().strftime("%Y%m%d-%H%M%S")
    filepath = "../models/" + file_name + "_" + str(accuracy)
    ovr_model.write().overwrite().save(filepath)
    return filepath, ovr_model


train_model(inputData)
