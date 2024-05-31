import pandas as pd
import spacy
from spacy.tokenizer import Tokenizer
from spacy.util import compile_infix_regex
import re
import multiprocessing as mp

def process_interaction(index, interaction, drug_name):
    if (("increased" in interaction or "decreased" in interaction or 'increase' in interaction) and drug_name in interaction):
        # Remove "increased" or "decreased" and drug name from the interaction
        interaction = interaction.replace("increased", "").replace("decreased", "").replace("increase", "").replace(drug_name, "").strip()
        filtered_interaction = remove_propositions_and_verbs(interaction)
        return index, filtered_interaction
    return index, None

def filter_data_and_new_col(filepath):
    try:
        # Read CSV file with error handling
        csv_data = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None

    csv_data = csv_data.head(n=99)

    # Extract Interaction and Drug columns
    interactions = csv_data['Interaction']
    drug_names = csv_data['Drug']

    # Create a new empty DataFrame column to store filtered interactions
    csv_data["Filtered Interaction"] = None

    # Use multiprocessing to process the data
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.starmap(process_interaction, [(index, interaction, drug_names.iloc[index]) for index, interaction in enumerate(interactions)])

    # Update DataFrame with results
    for index, filtered_interaction in results:
        if filtered_interaction is not None:
            csv_data.loc[index, "Filtered Interaction"] = filtered_interaction

    csv_data['effect'] = ''
    csv_data['base_drug'] = ''
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
    filter_list = filter_data_and_new_col(file_path)

    if filter_list is None:
        print("No data found.")
    else:
        filter_list.to_csv(r'C:\Users\gtush\Desktop\SayaCsv\effect2.csv', index=False)

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
                    filter_list.loc[filter_list.index[index], 'base_drug'] = drug_name_row
                    filter_list.loc[filter_list.index[index], 'Filtered Interaction'] = filter_list.loc[filter_list.index[index], 'Filtered Interaction'].replace(drug_name_row, ' ')
                    print(filter_list.iloc[index])
                    break

            for effect in effect_list:
                if effect in row['Filtered Interaction']:
                    filter_list.loc[filter_list.index[index], 'effect'] = effect
                    filter_list.loc[filter_list.index[index], 'Filtered Interaction'] = filter_list.loc[filter_list.index[index], 'Filtered Interaction'].replace(effect, ' ')
                    break

        filter_list.to_csv(r'C:\Users\gtush\Desktop\SayaCsv\effect3.csv', index=False)
