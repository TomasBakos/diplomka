import numpy as np
import keras
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import seaborn as sns; sns.set()
from datetime import datetime
import time
from sklearn.cluster import KMeans


data = pd.read_csv('C:/Users/Tomáš Bakoš/PycharmProjects/diplo/data/tanks_payments1.csv', engine='python', header=0, parse_dates=["client_timestamp"])
data_timestamp = 1547652900

for i in range(data.shape[0]):
    if data.loc[i, "platform"] == "IOS":
        data.loc[i, "platform"] = 0
    else:
        data.loc[i, "platform"] = 1
    if data['tanksalot_uid'][i] == 5306220:
        print(data.iloc[i, 0:4])


agg_data = data.groupby("tanksalot_uid", as_index=False).agg({"base_cost":"sum", "country":"count", "client_timestamp": "max"})
agg_data = agg_data.rename(index=str, columns={"base_cost": "pay_sum", "country": "pay_count", "client_timestamp": "pay_latest"})
agg_data = agg_data.reset_index(drop=True)
agg_data = agg_data.drop("tanksalot_uid", axis=1)

for i in range(agg_data.shape[0]):
    date_diff = data_timestamp - agg_data.loc[i, "pay_latest"].timestamp()
    day_diff = date_diff/86400
    if day_diff < 7: agg_data.loc[i, "pay_latest"] = 0
    elif day_diff < 14: agg_data.loc[i, "pay_latest"] = 1
    elif day_diff < 28: agg_data.loc[i, "pay_latest"] = 2
    elif day_diff < 35: agg_data.loc[i, "pay_latest"] = 3
    elif day_diff < 42: agg_data.loc[i, "pay_latest"] = 4
    elif day_diff < 49: agg_data.loc[i, "pay_latest"] = 5
    elif day_diff < 56: agg_data.loc[i, "pay_latest"] = 6
    elif day_diff < 63: agg_data.loc[i, "pay_latest"] = 7
    elif day_diff < 70: agg_data.loc[i, "pay_latest"] = 8
    elif day_diff < 77: agg_data.loc[i, "pay_latest"] = 9
    elif day_diff < 84: agg_data.loc[i, "pay_latest"] = 10
    else: agg_data.loc[i, "pay_latest"] = 11


plt.rcParams['figure.figsize'] = (16, 9)
# plt.style.use('ggplot')
# plot_base_cost = sns.distplot(agg_data.loc[:, "pay_sum"])
# plot_count = sns.distplot(agg_data.loc[:, "pay_count"])
# plot_count = sns.distplot(agg_data.loc[:, "pay_latest"])
# plt.xlabel("base_cost / count")
# plt.show()

wcss = []
for i in range(1,11):
    km=KMeans(n_clusters=i,init='k-means++', max_iter=300, n_init=10, random_state=0)
    km.fit(agg_data)
    wcss.append(km.inertia_)
plt.plot(range(1,11),wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('wcss')
plt.show()


agg_data = agg_data.values
##Fitting kmeans to the dataset - k=6
km6=KMeans(n_clusters=5,init='k-means++', max_iter=300, n_init=10, random_state=0)
y_means = km6.fit_predict(agg_data)
#Visualizing the clusters
fig = plt.figure()
ax = Axes3D(fig)

ax.scatter(agg_data[y_means==0,0],agg_data[y_means==0,1],agg_data[y_means==0,2],s=50, c='purple',label='Cluster1')
ax.scatter(agg_data[y_means==1,0],agg_data[y_means==1,1],agg_data[y_means==1,2],s=50, c='blue',label='Cluster2')
ax.scatter(agg_data[y_means==2,0],agg_data[y_means==2,1],agg_data[y_means==2,2],s=50, c='green',label='Cluster3')
ax.scatter(agg_data[y_means==3,0],agg_data[y_means==3,1],agg_data[y_means==3,2],s=50, c='cyan',label='Cluster4')
ax.scatter(agg_data[y_means==4,0],agg_data[y_means==4,1],agg_data[y_means==4,2],s=50, c='magenta',label='Cluster5')
#ax.scatter(agg_data[y_means==5,0],agg_data[y_means==5,1],agg_data[y_means==5,2],s=50, c='orange',label='Cluster6')
ax.scatter(km6.cluster_centers_[:,0], km6.cluster_centers_[:,1],km6.cluster_centers_[:,2],s=200,marker='s', c='red', alpha=0.7, label='Centroids')
plt.title('Customer segments')
plt.xlabel('Customer spend')
plt.ylabel('Customer spend frequency')
ax.set_zlabel("Customer spend recency")
plt.legend()
plt.tight_layout()
plt.show()


