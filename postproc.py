import pandas as pd
import re

df = pd.read_csv("new_profiles.csv", index_col=0)

# Function to clean the text
def clean_text(text):
    # Remove anything after a '.' or '(' using regular expressions
    text = re.split(r'\.|\(|->', text)[0]
    return text.strip()

# Apply the cleaning function to the 'Items' column
df['Profile'] = df['Profile'].apply(clean_text)


df.to_csv("cleaned_profiles.csv")