from classification_models.scene_model import VGG16_Hybrid_1365

base_model = VGG16_Hybrid_1365(input_shape=(128, 128, 3), weights='places', include_top=False)
base_model.save("./models/vgg_scene.hdf5")



