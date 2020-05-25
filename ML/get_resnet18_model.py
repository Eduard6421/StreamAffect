import numpy as np
from skimage.io import imread
from skimage.transform import resize
from keras.applications.imagenet_utils import decode_predictions
from classification_models.keras import Classifiers

ResNet18, preprocess_input = Classifiers.get('resnet18')
model = ResNet18(input_shape=(128, 128, 3), weights='imagenet', include_top=False)
model.save("./models/resnet18.hdf5")
