import numpy as np
import keras
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import seaborn as sns; sns.set()
from datetime import datetime
import time
from sklearn.cluster import KMeans


data = pd.read_csv('data/rfm_kmeans_maxbuy.csv', engine='python', header=0, index_col=0)

plt.rcParams['figure.figsize'] = (16, 9)
wcss = []
for i in range(1,11):
    km=KMeans(n_clusters=i,init='k-means++', max_iter=300, n_init=10, random_state=0)
    km.fit(data)
    wcss.append(km.inertia_)
plt.plot(range(1,11),wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('wcss')
plt.show()


data = data.values
##Fitting kmeans to the dataset - k=6
km6=KMeans(n_clusters=5,init='k-means++', max_iter=300, n_init=10, random_state=0)
y_means = km6.fit_predict(data)
#Visualizing the clusters
fig = plt.figure()
ax = Axes3D(fig)

ax.scatter(data[y_means==0,0],data[y_means==0,1],data[y_means==0,2],s=50, c='purple',label='Cluster1')
ax.scatter(data[y_means==1,0],data[y_means==1,1],data[y_means==1,2],s=50, c='blue',label='Cluster2')
ax.scatter(data[y_means==2,0],data[y_means==2,1],data[y_means==2,2],s=50, c='green',label='Cluster3')
ax.scatter(data[y_means==3,0],data[y_means==3,1],data[y_means==3,2],s=50, c='cyan',label='Cluster4')
ax.scatter(data[y_means==4,0],data[y_means==4,1],data[y_means==4,2],s=50, c='magenta',label='Cluster5')
#ax.scatter(data[y_means==5,0],data[y_means==5,1],data[y_means==5,2],s=50, c='orange',label='Cluster6')
ax.scatter(km6.cluster_centers_[:,0], km6.cluster_centers_[:,1],km6.cluster_centers_[:,2],s=200,marker='s', c='red', alpha=0.7, label='Centroids')
plt.title('Customer segments')
plt.xlabel('Customer spend')
plt.ylabel('Customer spend frequency')
ax.set_zlabel("Customer spend recency")
plt.legend()
plt.tight_layout()
plt.show()


