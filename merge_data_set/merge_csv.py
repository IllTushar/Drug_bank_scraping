import pandas as pd


def merge_data_set():
    read_file1 = pd.read_csv(r'D:\DrugBankCSV\InteractionData1.csv')
    read_file2 = pd.read_csv(r'D:\DrugBankCSV\InteractionData1.csv')
    combine_file = [read_file1, read_file2]

    concat_file = pd.concat(combine_file)

    concat_file.reset_index(drop=True, inplace=True)

    concat_file.to_csv(r'C:\Users\gtush\Desktop\csv_folder\Sample_file.csv', index=False)


if __name__ == '__main__':
    merge_data_set()
