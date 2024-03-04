import pandas as pd

# Load the CSV data into DataFrames
data1 = pd.read_csv("data_buylaptop.csv")
data2 = pd.read_csv("data_notebookcentre.csv")
data3 = pd.read_csv("data_nout_am.csv")
data4 = pd.read_csv("data_magic_notebooks.csv")

# print("data1 columns:", data1.columns)
# print("data2 columns:", data2.columns)
# print("data3 columns:", data3.columns)
# print("data4 columns:", data3.columns)

# Concatenate the DataFrames vertically
combined_data = pd.concat([data1, data2, data3, data4], ignore_index=True)

# Save the concatenated DataFrame to a new CSV file
combined_data.to_csv("data_notebooks.csv", index=False)
