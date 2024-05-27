import pandas as pd
import spacy


def filter_data_and_new_col(filepath):
    try:
        # Read CSV file with error handling
        csv_data = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None

    # Extract Interaction and Drug columns
    interactions = csv_data['Interaction']
    drug_names = csv_data['Drug']

    # Create a new empty DataFrame column to store filtered interactions
    csv_data["Filtered Interaction"] = None

    for index, interaction in enumerate(interactions[:100]):
        # Check if "increased" or "decreased" is present and if drug name is anywhere in the interaction
        if (("increased" in interaction or "decreased" in interaction) and drug_names.iloc[index] in interaction):
            # Remove "increased" or "decreased" and drug name from the interaction
            interaction = interaction.replace("increased", "").replace("decreased", "").replace(drug_names.iloc[index], "").strip()
            # Optional removal of verbs and prepositions using remove_proposition_and_verbs()
            filtered_interaction = remove_proposition_and_verbs(interaction)
            csv_data.loc[index, "Filtered Interaction"] = filtered_interaction

    # Print filtered interactions for debugging
    print(csv_data['Filtered Interaction'].head(100).tolist())


# if len(i.split()) > 1:
#     if i.split()[-1] == drug_name[index]:  # Check for multiple words and last element
#         new_data_list.append()
# else:
#     print(i)


def remove_proposition_and_verbs(interaction):
    try:
        # Load the English model (lazy loading)
        nlp = spacy.load('en_core_web_sm')
    except OSError:
        from spacy.cli import download
        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")

    # Process the text
    doc = nlp(interaction)

    # Create a list of tokens excluding verbs and prepositions
    filtered_tokens = [token.text for token in doc if
                       token.pos_ not in ['VERB', 'AUX', 'ADP', 'ADV', 'DET', 'PRON', 'CONJ', 'SCONJ']]

    # Join the filtered tokens back into a string
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


if __name__ == '__main__':
    file_path = r'C:\Users\gtush\Desktop\SayaCsv\interactions_subset.csv.csv'
    filter_data_and_new_col(file_path)
