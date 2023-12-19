import pandas as pd
from llama_cpp import Llama
import re
# Create an empty DataFrame
df = pd.DataFrame(columns=["Item", "Profile", "mgs"])

def extract_product_name(input_str):
    # Define a regular expression pattern to match the prefixes and patterns to remove
    pattern = r'\b(SUB|SALT|\d+ML|\d+MG)\b'  # Updated pattern

    # Use re.sub to remove the matched prefixes and patterns
    cleaned_name = re.sub(pattern, '', input_str, flags=re.IGNORECASE).strip()

    # Split the cleaned name by spaces and remove the last word
    cleaned_name_parts = cleaned_name.split()
    if len(cleaned_name_parts) > 1:
        cleaned_name_parts.pop()  # Remove the last word

    return ' '.join(cleaned_name_parts)


names = pd.read_excel("TVP_Flavor_List.xls")

names.columns = ['Item']

names['Item'] = names['Item'].str.replace(r'(\d+MG)', lambda x: x.group(0).lower(), regex=True)

names = names['Item'].tolist()

# model = "/Users/andrew/Documents/dev/text-generation-webui/models/Wizard-Vicuna-7B-Uncensored.Q4_K_M.gguf"

model = "/Users/andrew/Documents/dev/text-generation-webui/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"

disp = True

llm = Llama(model_path=model, use_mlock=True)

# if disp:
#     names = pd.read_csv("disp.csv")
# else:
#     names = pd.read_csv("out.csv")



# names = names["Item"].tolist()
# if not disp:
#     names = [extract_product_name(name) for name in names]

# print(len(names))
# names = list(set(names))
# print(len(names))


for name in names:
    example = " (for example 7 Daze Fusion Kiwi Passionfruit Guava should give a response of Kiwi, Passionfruit, Guava)"

    if_unsure = "If you are unsure what then simply reply with: 'none'"
    input_q = f"Describe the flavor profile of this product using only single words seperated by commas: {name}. {example}. {if_unsure}"    
    prompt = f"[INST] <<SYS>> You are a helpful, respectful and honest assistant. Be short and succinct and do not start with any description. Always answer as helpfully as possible. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information. <</SYS>>{input_q}[/INST]"
    
    output = llm(prompt, max_tokens=64, stop=["Q:"], echo=True)

    output = output['choices'][0]

    ans_index = output['text'].find("[/INST]")

    answer = output['text'][ans_index+7:]

    print(name)
    print(answer)

    if ":" in answer:
        answer = answer.split(":")[1]

    answer = answer.strip('.')
    answer = answer.strip("  ")
    answer = answer.strip("\n")

    df = pd.concat([df, pd.DataFrame({"Item": [name], "Profile": [answer]})], ignore_index=True)

    df.to_csv("new_profiles.csv")
