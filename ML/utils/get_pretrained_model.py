from classification_models.keras import Classifiers

ResNet18, preprocess_input = Classifiers.get('resnet18')
model = ResNet18(input_shape=(224, 224, 3), weights='imagenet', include_top=False)
print(model.summary())
model.save("resnet18.hdf5")

