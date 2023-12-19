import pandas as pd

df = pd.read_excel("TVP_Flavor_List.xls")

filtered_df = df[df['Catergory'].isin(['DISP'])]

selected_items_names = filtered_df['Item Name']

selected_items_names.columns = ['Item']

selected_items_names.to_csv("new_flavors.csv")