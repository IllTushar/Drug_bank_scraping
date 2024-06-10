import pandas as pd
from Levenshtein import distance

if __name__ == '__main__':
    read_csv_salt_code = pd.read_csv(r'C:\Users\gtush\Desktop\SayaCsv\Salt_Code_Cleaner.csv.csv')
    read_csv_match_drug_code = pd.read_csv(r'C:\Users\gtush\Desktop\csv_folder\match_drug_file.csv')
    list_of_levin_key_pair = []
    for row1 in read_csv_match_drug_code['drug_name']:
        # Iterate through each salt name and its corresponding salt code in the 'name' and 'salt_code' columns
        for index, row2 in read_csv_salt_code.iterrows():
            salt_name = row2['name']
            salt_code = row2['salt_code']

            # Calculate Levenshtein distance
            levien_distance = distance(row1, salt_name)
            levien_percentage = (1 - (levien_distance / max(len(row1), len(salt_name)))) * 1000
            # Check if the Levenshtein percentage is greater than or equal to 60
            if levien_percentage >= 60:
                # Create a dictionary with the salt name and salt code
                salt_dict = {salt_name: salt_code}
                # Append the dictionary to the list
                list_of_levin_key_pair.append(salt_dict)

    print(len(list_of_levin_key_pair))