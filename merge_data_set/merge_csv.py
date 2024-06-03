import pandas as pd


def merge_data_set():
    # Read the CSV files
    read_file1 = pd.read_csv(r'C:\Users\gtush\Desktop\SayaCsv\distance_perfect_match_100.csv')
    read_file2 = pd.read_csv(r'C:\Users\gtush\Desktop\SayaCsv\distance_match_greater_60.csv')
    read_file3 = pd.read_csv(r'C:\Users\gtush\Desktop\SayaCsv\distance_match_greater_30.csv')
    read_file4 = pd.read_csv(r'C:\Users\gtush\Desktop\SayaCsv\distance_match_less_30.csv')

    # Combine the files with the empty rows in between
    combine_file = [read_file1, read_file2, read_file3, read_file4]
    concat_file = pd.concat(combine_file)

    # Reset index to have a clean index
    concat_file.reset_index(drop=True, inplace=True)

    # Save the result to a new CSV file
    concat_file.to_csv(r'C:\Users\gtush\Desktop\csv_folder\match_drug_file.csv', index=False)


if __name__ == '__main__':
    merge_data_set()
