import glob
import os
from datetime import datetime

from pyspark.ml.classification import LogisticRegression, OneVsRest
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.shell import spark, sc

sc.setLogLevel("WARN")

base_folder_features          = './dataset/features'
base_folder_features_resnet   = './dataset/features_resnet'
base_folder_features_vgg_scene = './dataset/features_vgg_scene'
base_folder_features_vgg_scene_224 = './dataset/features_vgg_scene_224'

#CHANGE BASE FOLDER TO SELECT FEATURES TO TRAIN
features = glob.glob(os.path.join(base_folder_features_vgg_scene_224, "part*"))
print(features)
inputData = spark.read.format("libsvm") \
    .load(features)

inputData.show(n=10)


def train_model(input_data):
    splits = input_data.randomSplit([0.70, 0.30])
    train = splits[0]
    test = splits[1]
    train.show()

    # instantiate the base classifier.
    lr = LogisticRegression(maxIter=10, tol=1E-5, regParam=0.0, fitIntercept=True)

    # instantiate the One Vs Rest Classifier.
    ovr = OneVsRest(classifier=lr)

    # train the multiclass model.
    ovr_model = ovr.fit(train)

    # score the model on test data.
    predictions = ovr_model.transform(test)
    predictions.show()
    prediction_and_labels = predictions.select(['prediction', 'label']).rdd
    metrics = MulticlassMetrics(prediction_and_labels)
    accuracy = metrics.accuracy

    # save model
    model_type = 'vgg_scene_224'
    file_name = "LogisticRegression_model_" + model_type + datetime.now().strftime("%Y%m%d-%H%M%S")
    filepath = "./models/" + file_name + "_" + str(accuracy)
    ovr_model.write().overwrite().save(filepath)
    return filepath, ovr_model


file, model = train_model(inputData)
print(file)

#max_iter  tol    regParam
# 10       1E-5   0.0     => 0.70
# 10       1E-7   0.0     => 0.72


# 10       1E-5   0.15     => 0.73
# 10       1E-7   0.15     => 0.71

#resnet
# 10       1E-5   0.0     => 0.73
# 10       1E-7   0.0     => 0.73

# 10       1E-5   0.15     => 0.72
# 10       1E-7   0.15     => 0.77

#vgg scene
# 10       1E-5   0.0     => 0.78
# 10       1E-7   0.0     => 0.76

# 10       1E-5   0.15     => 0.76
# 10       1E-7   0.15     => 0.77

#vgg scene 224

