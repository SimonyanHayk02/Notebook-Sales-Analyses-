import pandas as pd


df1 = pd.read_csv("data_nout_am_new.csv")
df2 = pd.read_csv("data_nout_am.csv")
combined_data = pd.concat([df1,df2]).drop_duplicates().reset_index(drop=True)

combined_data.to_csv("data_nout_am_final.csv", index=False)