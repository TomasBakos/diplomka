import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import seaborn as sns; sns.set()
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage, cophenet, fcluster
from scipy.spatial.distance import pdist
import sklearn.metrics as sm

data = pd.read_csv('data/spend_habbits.csv', engine='python', header=0, index_col=0)
data = data.values

# z = linkage(data, "ward")
# c, coph_dists = cophenet(z, pdist(data))

# # calculate full dendrogram
# plt.figure(figsize=(25, 10))
# plt.title('Hierarchical Clustering Dendrogram')
# plt.xlabel('sample index')
# plt.ylabel('distance')
# dendrogram(
#     z,
#     truncate_mode="lastp",
#     p=50,
#     leaf_rotation=90.,  # rotates the x axis labels
#     leaf_font_size=20.,  # font size for the x axis labels
# )
# plt.axhline(y=20)
# plt.show()

cluster = AgglomerativeClustering(n_clusters=3, affinity="euclidean", linkage="ward")
y_data = cluster.fit(data)
#y_data = cluster.fit_predict(data)


sm.accuracy_score()