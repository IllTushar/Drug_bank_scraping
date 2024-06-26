import pandas as pd
import spacy
from spacy.tokenizer import Tokenizer
from spacy.util import compile_infix_regex
import re


# Function to load or download spaCy model
def load_spacy_model():
    try:
        nlp = spacy.load('en_core_web_sm')
    except OSError:
        from spacy.cli import download
        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")

    infix_re = compile_infix_regex(nlp.Defaults.infixes + [r'\b1,2-\b'])
    nlp.tokenizer = Tokenizer(nlp.vocab, infix_finditer=infix_re.finditer)
    return nlp


# Function to remove propositions and verbs from a given text
def remove_propositions_and_verbs(interaction, nlp):
    doc = nlp(interaction)
    filtered_tokens = [token.text_with_ws for token in doc if token.pos_ not in
                       ['VERB', 'AUX', 'ADP', 'ADV', 'DET', 'PRON', 'CCONJ', 'SCONJ'] and
                       token.text.lower() != 'combination']
    filtered_text = ''.join(filtered_tokens).strip()
    filtered_text = re.sub(r'\s+', ' ', filtered_text)
    return filtered_text


# Function to process each interaction and extract relevant details
def process_interaction(index, interaction, drug_name, nlp):
    keywords = ["increased", "decreased", "increase", "decrease"]
    for keyword in keywords:
        if keyword in interaction and drug_name in interaction:
            interaction = interaction.replace(keyword, "").replace(drug_name, "").strip()
            filtered_interaction = remove_propositions_and_verbs(interaction, nlp)
            return index, filtered_interaction, keyword
    return index, None, None


# Function to load data, process interactions, and create new columns
def filter_data_and_new_col(filepath):
    try:
        csv_data = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None

    interactions = csv_data['Interaction']
    drug_names = csv_data['Drug']
    csv_data["Filtered Interaction"] = None
    csv_data["Effect Type"] = None

    nlp = load_spacy_model()

    results = [process_interaction(index, interaction, drug_names.iloc[index], nlp)
               for index, interaction in enumerate(interactions)]

    for index, filtered_interaction, keyword in results:
        if filtered_interaction is not None:
            csv_data.loc[index, "Filtered Interaction"] = filtered_interaction
            csv_data.loc[index, "Effect Type"] = keyword

    csv_data['effect'] = ''
    csv_data['base_drug'] = ''
    return csv_data


# Function to update the filtered list with drug and effect information
def update_with_drug_and_effect_info(filter_list, drug_bank_filepath, effect_list_filepath):
    drug_bank_data = pd.read_csv(drug_bank_filepath)
    effect_list_data = pd.read_csv(effect_list_filepath)
    drug_names = drug_bank_data['Name'].tolist()
    effects = effect_list_data['effect'].tolist()

    for index, row in filter_list.iterrows():
        if row['Filtered Interaction'] is None:
            continue

        for drug_name in drug_names:
            if drug_name in row['Filtered Interaction']:
                filter_list.at[index, 'base_drug'] = drug_name
                row['Filtered Interaction'] = row['Filtered Interaction'].replace(drug_name, '').strip()
                break

        for effect in effects:
            if effect in row['Filtered Interaction']:
                filter_list.at[index, 'effect'] = effect
                row['Filtered Interaction'] = row['Filtered Interaction'].replace(effect, '').strip()
                break

    return filter_list


if __name__ == '__main__':
    for i in range(1, 101):
        file_path = fr'C:\Users\gtush\Desktop\SayaCsv\subset{i}.csv'
        drug_bank_filepath = r'C:\Users\gtush\Desktop\csv_folder\FinalMergeDrugBank.csv'
        effect_list_filepath = r'C:\Users\gtush\Desktop\SayaCsv\effect_list.csv'

        filter_list = filter_data_and_new_col(file_path)
        if filter_list is not None:
            filter_list = update_with_drug_and_effect_info(filter_list, drug_bank_filepath, effect_list_filepath)
            filter_list.to_csv(fr'C:\Users\gtush\Desktop\SayaCsv\effect_split{i}.csv', index=False)
        else:
            print("No data found.")
