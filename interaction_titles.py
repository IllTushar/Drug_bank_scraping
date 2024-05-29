import pandas as pd


def get_interactions(file_path):
    path = pd.read_csv(file_path)
    col = path['Interaction']
    print(len(col))
    my_set = set()
    for row in col[:30]:
        my_set.add(row)
    print(my_set)


if __name__ == '__main__':
    get_interactions(r'C:\Users\gtush\Desktop\SayaCsv\interactions_subset.csv.csv.crdownload')
