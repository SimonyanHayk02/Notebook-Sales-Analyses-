import pandas as pd
import random
import csv
import numpy as np

# Load the CSV data into DataFrames
data1 = pd.read_csv("data_buylaptop.csv")
data2 = pd.read_csv("data_notebookcentre.csv")
data3 = pd.read_csv("data_nout_am.csv")

loop_list = [data1, data2, data3]

with open("./data_magic_notebooks.csv", "w", encoding="UTF8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        (
            "Company",
            "Model",
            "Display Height",
            "Display Width",
            "Display Size",
            "Display Quality",
            "Display Type",
            "Processor Name",
            "Processor Generation",
            "Memory",
            "Ram",
            "Videocard",
            "Videocard Storage",
            "Illuminated keyboard",
            "Price",
            "Website index",
        )
    )


def data_creator(dataframe):
    dataframe = dataframe.replace(np.nan, None)

    for i in range(0, len(dataframe)):
        print(dataframe["Company"][i])
        new_price = dataframe["Price"][i] * random.uniform(0.9, 1.1)
        new_price = int((new_price // 100) * 100)
        print(dataframe["Price"][i], new_price)

        with open("./data_magic_notebooks.csv", "a", encoding="UTF8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                (
                    dataframe["Company"][i],
                    dataframe["Model"][i],
                    dataframe["Display Height"][i],
                    dataframe["Display Width"][i],
                    dataframe["Display Size"][i],
                    dataframe["Display Quality"][i],
                    dataframe["Display Type"][i],
                    dataframe["Processor Name"][i],
                    dataframe["Processor Generation"][i],
                    dataframe["Memory"][i],
                    dataframe["Ram"][i],
                    dataframe["Videocard"][i],
                    dataframe["Videocard Storage"][i],
                    dataframe["Illuminated keyboard"][i],
                    new_price,
                    4,
                )
            )


for i in loop_list:
    data_creator(i)
