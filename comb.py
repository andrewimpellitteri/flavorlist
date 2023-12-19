import pandas as pd

df1 = pd.read_csv("/Users/andrew/Documents/dev/vaporplace/llama_profiles_disp.csv")
df2 = pd.read_csv("/Users/andrew/Documents/dev/vaporplace/llama_profiles.csv")

df = pd.concat([df1, df2])
# Drop the "Unnamed: 0" column
df.drop(columns=["Unnamed: 0"], inplace=True)

# Reset the index to create a new continuous integer index
df.reset_index(drop=True, inplace=True)

df.to_csv('final.csv')