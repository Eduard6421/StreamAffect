import glob
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from ipywidgets import interact, fixed
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.util import MLUtils
from pyspark.shell import spark
from pyspark.sql import Window
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from pyspark.sql.functions import monotonically_increasing_id, row_number

def get_data():
    from pyspark.shell import spark
    base_folder_features = '../dataset/features'
    features = glob.glob(os.path.join(base_folder_features, "part*"))

    inputData = spark.read.format("libsvm") \
        .load(features)
    inputData = inputData.rdd.map(lambda x: (x[0], x[1].toArray()))
    samples = inputData.collect()

    yClass = []
    data = []
    for sample in samples:
        data.append(sample[1])
        yClass.append(sample[0])
    return data, yClass


def plot_3D(elev, azim, X, y, title):
    ax = plt.subplot(projection='3d')
    ax.scatter3D(X[:, 0], X[:, 1], X[:, 2], c=y, s=50)
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.title(title)
    plt.savefig(title + ".png")


def plotInteractive(X, y, title):
    plot_3D(elev=45, azim=45,
            X=X, y=y, title=title)


data, yClass = get_data()
pca = PCA(n_components=2000)
principalComponents = pca.fit_transform(np.array(data))
print(principalComponents)
#Plotting the Cumulative Summation of the Explained Variance
plt.figure()
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('Number of Components')
plt.ylabel('Variance (%)') #for each component
plt.title('Emotions Dataset Explained Variance')
plt.show()
plotInteractive(principalComponents, yClass, 'PCA')
tsne_result = TSNE(n_components=3).fit_transform(np.array(data))
plotInteractive(tsne_result, yClass, 't-SNE')

#######################################################################
def save_pca_features(principalComponents):

    principalComponents = principalComponents.tolist()
    data_df = spark.createDataFrame(map(lambda x: (x,), principalComponents), ["features"])
    data_label_df = spark.createDataFrame([(l,) for l in yClass], ["label"])
    data_df = data_df.withColumn("row_idx", row_number().over(Window.orderBy(monotonically_increasing_id())))
    data_label_df = data_label_df.withColumn("row_idx", row_number().over(Window.orderBy(monotonically_increasing_id())))

    final_df = data_label_df.join(data_df, data_label_df.row_idx == data_df.row_idx).\
                 drop("row_idx")
    final_df.show()
    final_df = final_df.rdd.map(lambda x: LabeledPoint(x.label, x.features))
    t = final_df.count()
    MLUtils.saveAsLibSVMFile(final_df, "../dataset/features_pca_2/")

