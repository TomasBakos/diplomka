import pandas as pd


data = pd.read_csv('data/tanks_payments1.csv', engine='python', header=0, parse_dates=["client_timestamp"])
data_timestamp = 1547652900

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

agg_data.to_csv("data/rfm_kmeans_cumsum.csv")