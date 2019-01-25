import pandas as pd


data = pd.read_csv('data/tanks_payments1.csv', engine='python', header=0, parse_dates=["client_timestamp"])
data = data.drop(["client_timestamp", "country", "platform"], axis=1)

agg_data = data.groupby(["tanksalot_uid","type"]).agg({"base_cost":["sum","count"]})
ids = data.tanksalot_uid.unique()
agg_data["gems_revenue_pct"] = 0
agg_data["gems_count_pct"] = 0
agg_data["bundle_revenue_pct"] = 0
agg_data["bundle_count_pct"] = 0

for id in ids:

    revenue_sum = 0
    count_sum = 0
    gems_revenue = 0
    gems_count = 0
    bundle_revenue = 0
    bundle_count = 0

    gems = True
    bundle = True
    try:
        revenue_sum += agg_data.loc[(id, "Gems"), ("base_cost","sum")]
        gems_revenue = agg_data.loc[(id, "Gems"), ("base_cost","sum")]
        count_sum += agg_data.loc[(id, "Gems"), ("base_cost", "count")]
        gems_count = agg_data.loc[(id, "Gems"), ("base_cost", "count")]
    except KeyError:
        gems = False

    try:
        revenue_sum += agg_data.loc[(id, "Bundle"), ("base_cost", "sum")]
        bundle_revenue = agg_data.loc[(id, "Bundle"), ("base_cost", "sum")]
        count_sum += agg_data.loc[(id, "Bundle"), ("base_cost", "count")]
        bundle_count = agg_data.loc[(id, "Bundle"), ("base_cost", "count")]
    except KeyError:
        bundle = False

    if gems:
        agg_data.loc[(id, "Gems"), ("gems_revenue_pct", "")] = gems_revenue / revenue_sum
        agg_data.loc[(id, "Gems"), ("bundle_revenue_pct", "")] = bundle_revenue / revenue_sum
        agg_data.loc[(id, "Gems"), ("gems_count_pct", "")] = gems_count / count_sum
        agg_data.loc[(id, "Gems"), ("bundle_count_pct", "")] = bundle_count / count_sum


    if bundle:
        agg_data.loc[(id, "Bundle"), ("gems_revenue_pct", "")] = gems_revenue / revenue_sum
        agg_data.loc[(id, "Bundle"), ("bundle_revenue_pct", "")] = bundle_revenue / revenue_sum
        agg_data.loc[(id, "Bundle"), ("gems_count_pct", "")] = gems_count / count_sum
        agg_data.loc[(id, "Bundle"), ("bundle_count_pct", "")] = bundle_count / count_sum

    #questionable
    if bundle and gems:
        agg_data = agg_data.drop((id, "Bundle"))

agg_data = agg_data.reset_index()
agg_data = agg_data.drop([('tanksalot_uid', ''), ('type', ''), ('base_cost', 'sum'), ('base_cost', 'count')], axis=1)
agg_data.to_csv("data/spend_habbits.csv")

