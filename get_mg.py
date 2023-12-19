import pandas as pd
import numpy as np
from fuzzywuzzy import process
from tqdm import tqdm

# Read the CSV file
data = pd.read_csv("out.csv", index_col=0)
final = pd.read_csv("final.csv", index_col=0)

# data = data['Item']

# Split the 'Product' column into separate columns
data["Item"] = data["Item"].str.replace(r"\d+ml", "", regex=True)


# Extracting mg values using regex
data["mg"] = data["Item"].str.extract(r"(\d+mg)")

# Group by 'Product' and get unique 'mg' values
grouped = data.groupby("Item")["mg"].unique().reset_index()

grouped["Item"] = grouped["Item"].str.extract(r"(.+)(?=\s\d+mg)")

grouped["mg"] = grouped["mg"].apply(
    lambda x: [item for sublist in x if isinstance(sublist, list) for item in sublist]
    if isinstance(x, list)
    else x
)
result = grouped.groupby("Item")["mg"].apply(list).reset_index().values.tolist()

final_items = final['Item'].values.tolist()

for item in tqdm(result):
    product_name = item[0]
    mgs = np.concatenate(item[1]).tolist()

    choice = process.extractOne(product_name, final_items)

    condition = (final['Item'] == choice[0])

    final.loc[condition, 'mgs'] = ",".join(mgs)

    print(final.sort_values(by='mgs'))

final.to_csv('final_w_mgs.csv')


