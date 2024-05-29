import pandas as pd

if __name__ == '__main__':
    read_csv = pd.read_csv(r'C:\Users\gtush\Desktop\SayaCsv\interactions_subset.csv.csv.crdownload')
    # Select the first 100 rows
    sub_set = read_csv.head(100)
    sub_set.to_csv(r"C:\Users\gtush\Desktop\SayaCsv\subset.csv")
