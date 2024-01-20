import pandas as pd

df = pd.read_excel('final2024.xlsx')

df.columns = ['Item', 'Profile']

df.to_csv("final_edited2024.csv", index=False)