from Levenshtein import distance
import pandas as pd

final_result = []


def find_salt_code(salt_code_clean, match_drug_code_file, desired_similarity=60.0):

    # Extract relevant columns
    name_salt_code_clean = salt_code_clean_csv[['name', 'generic_name']]
    drug_name_drug_code = match_drug_code_csv[['drug_name', 'generic_name', 'salt_code']]

    list_name_not_null = []
    results = []

    # Create a list of names with non-null generic names
    for idx, row in name_salt_code_clean.iterrows():
        drug_name = row['name']
        drug_generic_name = row['generic_name']
        if not pd.isnull(drug_generic_name):
            list_name_not_null.append(drug_name)

    # Create a list of tuples with (drug_name, generic_name, salt_code)
    generic_names = list(
        zip(drug_name_drug_code['drug_name'], drug_name_drug_code['generic_name'], drug_name_drug_code['salt_code'])
    )

    for drug_name in list_name_not_null:
        if not drug_name:
            continue

        most_similar_generic_name = None
        most_similar_salt_code = None
        highest_similarity = 0.0
        best_levenshtein_distance = None

        for drug_names, generic_name, salt_code in generic_names:
            combined_name = drug_names if not generic_name else f"{drug_names} {generic_name}"

            levenshtein_distance = distance(drug_name, combined_name)
            similarity_percentage = (1 - (levenshtein_distance / max(len(drug_name), len(combined_name)))) * 100

            if similarity_percentage > highest_similarity:
                most_similar_generic_name = drug_names
                most_similar_salt_code = salt_code
                highest_similarity = similarity_percentage
                best_levenshtein_distance = levenshtein_distance

        if highest_similarity >= desired_similarity:
            gen_dict = {'generic_name': most_similar_generic_name, "salt_code": most_similar_salt_code}
            results.append(gen_dict)

    for result in results:
        gen_name = result['generic_name']
        salt_code = result['salt_code']

        for idx, row in drug_name_drug_code.iterrows():
            drug_generic_name = row['generic_name']
            if drug_generic_name == gen_name:
                dict = {"modified_generic": gen_name, "salt_codes": salt_code}
                final_result.append(dict)
                break

    final_data_set = pd.DataFrame(final_result)
    return final_data_set


if __name__ == '__main__':
    salt_code_clean = r'C:\Users\gtush\Desktop\csv_folder\Salt_Code_Cleaner.csv.csv'
    match_drug_code_file = r'C:\Users\gtush\Desktop\csv_folder\match_drug_file.csv'

    # Read CSV files
    salt_code_clean_csv = pd.read_csv(salt_code_clean)
    match_drug_code_csv = pd.read_csv(match_drug_code_file)

    data_set = find_salt_code(salt_code_clean_csv, match_drug_code_csv)
    salt_code_clean_csv.insert(loc=11, column='NewG_NAMe', value=data_set['modified_generic'])
    salt_code_clean_csv.insert(loc=12, column='SName', value=data_set['salt_codes'])
    salt_code_clean_csv.to_csv(salt_code_clean,index=False)

