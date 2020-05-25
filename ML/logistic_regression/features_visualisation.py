import glob
import os
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from ipywidgets import interact, fixed
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


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
pca = PCA(n_components=5)
principalComponents = pca.fit_transform(np.array(data))
plotInteractive(principalComponents, yClass, 'PCA')
tsne_result = TSNE(n_components=3).fit_transform(np.array(data))
plotInteractive(tsne_result, yClass, 't-SNE')
