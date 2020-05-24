from keras_preprocessing.image import img_to_array, load_img
from logistic_regression.predict import predict


def load_data_image(uri):
    image = img_to_array(load_img(uri, target_size=(416, 416)))
    return image


images = []
paths = ["./dataset/anger/anger154.jpg", "./dataset/happy/happy154.jpg"]
for i in paths:
    img = load_data_image(i)
    images.append(img)
preds = predict(images, model_path="models/LogisticRegression_model_20200524-154144_0.7325102880658436")
