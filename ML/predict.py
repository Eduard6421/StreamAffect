from pyspark.ml.classification import OneVsRestModel

def load_model_and_predict(sample, path_model):
    # load model
    model = OneVsRestModel.load(path_model)

    # score the model on test data.
    predictions = model.transform(sample)

    # return list of prediction
    prediction = predictions.select(['prediction']).collect()
    return prediction
