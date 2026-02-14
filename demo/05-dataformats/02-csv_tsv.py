import pandas as pd

my_csv_file = "squirrel-census.csv"
my_tsv_file = "squirrel-census.tsv"

df = pd.read_csv(my_csv_file, delimiter=",")
df.to_csv(my_tsv_file, sep="\t", index=False)