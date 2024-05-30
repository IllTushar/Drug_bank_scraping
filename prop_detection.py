import pandas as pd
import spacy
from spacy.tokenizer import Tokenizer
from spacy.util import compile_infix_regex
import re

list_of_effect = []
generic_list = []


def filter_data_and_new_col(filepath):
    try:
        # Read CSV file with error handling
        csv_data = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    #
    csv_data = csv_data.head(n=99)

    # Extract Interaction and Drug columns
    interactions = csv_data['Interaction']
    drug_names = csv_data['Drug']

    # Create a new empty DataFrame column to store filtered interactions
    csv_data["Filtered Interaction"] = None

    for index, interaction in enumerate(interactions):
        # Check if "increased" or "decreased" is present and if drug name is anywhere in the interaction
        if (("increased" in interaction or "decreased" in interaction or 'increase' in interaction) and drug_names.iloc[index] in interaction):
            # Remove "increased" or "decreased" and drug name from the interaction
            interaction = interaction.replace("increased", "").replace("decreased", "").replace("increase",
                                                                                                "").replace(
                drug_names.iloc[index],
                "").strip()
            # Optional removal of verbs and prepositions using remove_proposition_and_verbs()
            filtered_interaction = remove_propositions_and_verbs(interaction)
            # print(f"-> {filtered_interaction},index -> {index}")
            csv_data.loc[index, "Filtered Interaction"] = filtered_interaction

    csv_data['effect'] = ''
    csv_data['base_drug'] = ''
    print(csv_data)

    # filtered_interaction_data = csv_data['Filtered Interaction'].head(n=100)
    # Print filtered interactions for debugging
    return csv_data


def remove_propositions_and_verbs(interaction):
    try:
        # Load the English model
        nlp = spacy.load('en_core_web_sm')
    except OSError:
        from spacy.cli import download
        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")

    # Customize the tokenizer to keep "1,2-Benzodiazepine" as a single token
    infix_re = compile_infix_regex(nlp.Defaults.infixes + [r'\b1,2-\b'])
    nlp.tokenizer = Tokenizer(nlp.vocab, infix_finditer=infix_re.finditer)

    # Process the text
    doc = nlp(interaction)

    # Create a list of tokens excluding verbs, auxiliaries, prepositions, adverbs, determiners, pronouns, conjunctions, and subordinating conjunctions
    filtered_tokens = [token.text_with_ws for token in doc if
                       token.pos_ not in ['VERB', 'AUX', 'ADP', 'ADV', 'DET', 'PRON', 'CCONJ', 'SCONJ'] and
                       token.text.lower() != 'combination']

    # Join the filtered tokens back into a string and remove extra spaces
    filtered_text = ''.join(filtered_tokens).strip()
    filtered_text = re.sub(r'\s+', ' ', filtered_text)
    return filtered_text


if __name__ == '__main__':
    file_path = r'C:\Users\gtush\Desktop\SayaCsv\subset.csv'
    read_interaction_subset_csv = pd.read_csv(file_path)
    filter_list = filter_data_and_new_col(file_path)
    # size_data_interaction_set = len(filter_list)
    # print(len(filter_list))

    filter_list.to_csv(r'C:\Users\gtush\Desktop\SayaCsv\effect2.csv', index=False)

    if filter_list is None:
        print("No data found.")
    else:
        # Ensure the correct string formatting for the search
        read_drug_bank_csv = pd.read_csv(r"C:\Users\gtush\Desktop\SayaCsv\DrugBankData1.csv")
        drug_name = read_drug_bank_csv['Name']
        pd_read_effect_csv = pd.read_csv(r'C:\Users\gtush\Desktop\SayaCsv\effect_list.csv')
        effect_list = pd_read_effect_csv['effect']

        filter_list = filter_list.reset_index()

        for index, row in filter_list.iterrows():
            if row['Filtered Interaction'] is None:
                continue  # Skip None items

            for drug_name_row in drug_name:
                if drug_name_row in row['Filtered Interaction']:
                    # filter_item_list = filter_item.split(drug_name_row)
                    # print(drug_name_row + filter_item)
                    # effect_list.append(filter_item_list[-2].strip())
                    filter_list.loc[filter_list.index[index], 'base_drug'] = drug_name_row
                    filter_list.loc[filter_list.index[index], 'Filtered Interaction'] = filter_list.loc[
                        filter_list.index[index], 'Filtered Interaction'].replace(drug_name_row, ' ')
                    print(filter_list.iloc[index])
                    break

            for effect in effect_list:
                if effect in row['Filtered Interaction']:
                    filter_list.loc[filter_list.index[index], 'effect'] = effect
                    filter_list.loc[filter_list.index[index], 'Filtered Interaction'] = filter_list.loc[
                        filter_list.index[index], 'Filtered Interaction'].replace(effect, ' ')
                    break

        filter_list.to_csv(r'C:\Users\gtush\Desktop\SayaCsv\effect3.csv', index=False)
