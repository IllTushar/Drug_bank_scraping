import pandas as pd
import spacy
from spacy.tokenizer import Tokenizer
from spacy.util import compile_infix_regex
import re
import multiprocessing as mp


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


def remove_propositions_and_verbs(interaction, nlp):
    doc = nlp(interaction)
    filtered_tokens = [token.text_with_ws for token in doc if token.pos_ in ['NOUN', 'ADJ'] and token.text.lower() != 'combination']
    filtered_text = ''.join(filtered_tokens).strip()
    filtered_text = re.sub(r'\s+', ' ', filtered_text)
    return filtered_text


def process_interaction(index, interaction, drug_name, nlp):
    keywords = ["increased", "decreased", "increase", "decrease", "affect", "impact"]
    for keyword in keywords:
        if keyword in interaction and drug_name in interaction:
            interaction = interaction.replace(keyword, "").replace(drug_name, "").strip()
            filtered_interaction = remove_propositions_and_verbs(interaction, nlp)
            return index, filtered_interaction, keyword
    return index, None, None


def process_and_update(filepath, drug_bank_filepath, effect_list_filepath):
    try:
        csv_data = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None

    drug_bank_data = pd.read_csv(drug_bank_filepath)
    effect_list_data = pd.read_csv(effect_list_filepath)

    drug_names = drug_bank_data['Name']
    effect_list = effect_list_data['effect']

    interactions = csv_data['Interaction']
    drug_names_in_data = csv_data['Drug']
    csv_data["Filtered Interaction"] = None
    csv_data["Effect Type"] = None
    csv_data['effect'] = ''
    csv_data['base_drug'] = ''

    nlp = load_spacy_model()

    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.starmap(process_interaction, [(index, interaction, drug_names_in_data.iloc[index], nlp) for index, interaction in enumerate(interactions)])

    for index, filtered_interaction, keyword in results:
        if 33 <= index <= 45 and filtered_interaction is not None:
            csv_data.loc[index, "Filtered Interaction"] = filtered_interaction
            csv_data.loc[index, "Effect Type"] = keyword

    for index, row in csv_data.iterrows():
        if index < 33 or index > 45:
            continue

        if row['Filtered Interaction'] is None:
            continue

        for drug_name in drug_bank_data['Name']:
            if drug_name in row['Filtered Interaction']:
                csv_data.at[index, 'base_drug'] = drug_name
                csv_data.at[index, 'Filtered Interaction'] = csv_data.at[index, 'Filtered Interaction'].replace(
                    drug_name, '').strip()
                break

        for effect in effect_list:
            if effect in row['Filtered Interaction']:
                csv_data.at[index, 'effect'] = effect
                csv_data.at[index, 'Filtered Interaction'] = csv_data.at[index, 'Filtered Interaction'].replace(
                    effect, '').strip()
                break

    # Filter to include only rows between index 33 and 45
    csv_data = csv_data.iloc[33:46]

    return csv_data


if __name__ == '__main__':
    file_path = r'C:\Users\gtush\Desktop\SayaCsv\subset.csv'
    drug_bank_filepath = r'C:\Users\gtush\Desktop\SayaCsv\DrugBankData1.csv'
    effect_list_filepath = r'C:\Users\gtush\Desktop\SayaCsv\effect_list.csv'

    processed_data = process_and_update(file_path, drug_bank_filepath, effect_list_filepath)
    if processed_data is not None:
        processed_data.to_csv(r'C:\Users\gtush\Desktop\SayaCsv\effect3.csv', index=False)
    else:
        print("No data found.")
