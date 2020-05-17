import math

from pyspark.ml.classification import LogisticRegression, OneVsRest, LinearSVC
from pyspark.mllib.evaluation import MulticlassMetrics


def train_model(input_data, path):
    splits = input_data.randomSplit([0.70, 0.30], 1234)
    train = splits[0]
    test = splits[1]

    # instantiate the base classifier.
    lr = LogisticRegression(maxIter=20, tol=1E-6, regParam=0.1, fitIntercept=True)

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
    ovr_model.write().overwrite().save(path + "_" + str(math.floor(accuracy * 1000) / 10))
    return path + "_" + str(math.floor(accuracy * 1000) / 10)
