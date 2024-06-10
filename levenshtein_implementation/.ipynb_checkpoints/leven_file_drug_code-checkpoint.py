from Levenshtein import distance
import pandas as pd

final_result = []

if __name__ == '__main__':
    salt_code_clean = r'C:\Users\gtush\Desktop\csv_folder\Salt_Code_Cleaner.csv.csv'
    match_drug_code_file = r'C:\Users\gtush\Desktop\csv_folder\match_drug_file.csv'

    # Read CSV files
    salt_code_clean_csv = pd.read_csv(salt_code_clean)
    match_drug_code_csv = pd.read_csv(match_drug_code_file)
    print(salt_code_clean_csv)
    print(match_drug_code_csv)
