import pandas as pd


# interaction table url
def get_data_from_interaction_table(file_path):
    read_file = pd.read_csv(file_path)
    url = read_file['Base.Drug']
    url_list = list(url)
    return url_list


# drug bank table url
def get_drug_bank_data(file_path):
    read_file = pd.read_csv(file_path)
    drug_url = read_file['Drug URL']
    my_drug_list_url = list(drug_url)
    return my_drug_list_url


def print_unique_url(interaction_data, drug_bank_data, drug_bank_data_file):
    list_of_url = []
    count = 0
    for interaction_url in interaction_data:
        for drug_url in drug_bank_data:
            if interaction_url == drug_url:
                count += 1
                list_of_url.append(drug_url)
    read_file = pd.read_csv(drug_bank_data_file)
    name_drug = read_file['Name']
    drug_url = read_file['Drug URL']
    drug_url_map = dict(zip(drug_url, name_drug))
    count = 0
    for list_url in list_of_url:
        if list_url in drug_url_map:
            count += 1
            print(drug_url_map[list_url])
    print(count)


if __name__ == '__main__':
    file_path = r'C:\Users\gtush\Desktop\SayaCsv\interactions_subset.csv.csv'
    interaction_data = get_data_from_interaction_table(file_path)
    read_file1 = pd.read_csv(file_path)

    drug_bank_data_file = r'C:\Users\gtush\Desktop\SayaCsv\DrugBankData.csv'
    drug_bank_data = get_drug_bank_data(drug_bank_data_file)

    read_file = pd.read_csv(drug_bank_data_file)
    name_drug = read_file['Name']
    print(len(name_drug))
    drug_url = read_file['Drug URL']
    drug_url_map = dict(zip(drug_url, name_drug))

    count = 0
    matching_drug_names = []

    for interaction_url in interaction_data:
        if interaction_url in drug_url_map:
            count += 1
            matching_drug_names.append(drug_url_map[interaction_url])

    print(f"Number of matches: {count}")
    print("Matching drug names:")
    # Step 2: Add the new column to the DataFrame
    read_file1['Generic Name'] = matching_drug_names
    # Step 3: Save the modified DataFrame back to the CSV file
    read_file1.to_csv(file_path, index=False)
