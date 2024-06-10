import pandas as pd
import re


# Function to filter drug names and remove keywords
def filter_drug_names_and_keywords(interaction):
    # Filter out drug names
    for drug_name in drug_names:
        interaction = interaction.replace(drug_name, '').strip()

    # Remove keywords
    keywords_regex = r'\b(?:increased|decreased|increase|decrease)\b'
    interaction = re.sub(keywords_regex, '', interaction).strip()

    return interaction


if __name__ == '__main__':
    # Read CSV files
    read_csv_file = pd.read_csv(r'C:\Users\gtush\Desktop\Splits_sets\unfiltered_interaction.csv')
    read_drug_bank_csv = pd.read_csv(r'C:\Users\gtush\Desktop\SayaCsv\DrugBankData.csv')

    # Extract drug names as a set
    drug_names = set(read_drug_bank_csv["Name"])

    # Apply the filter function to each row in the DataFrame
    read_csv_file['Filter DrugName'] = read_csv_file['unfiltered_data'].apply(filter_drug_names_and_keywords)

    # Save to a new CSV file to avoid overwriting the original
    read_csv_file.to_csv(r'C:\Users\gtush\Desktop\Splits_sets\filtered_interaction.csv', index=False)
