import pandas as pd
import pickle

df = pd.read_csv("common_passwords.csv")

common_passwords = set(df.iloc[:,0].astype(str))

# store hash table
with open("password_hash_table.pkl", "wb") as f:
    pickle.dump(common_passwords, f)