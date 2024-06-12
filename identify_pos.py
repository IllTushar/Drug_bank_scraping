import pandas as pd
import spacy
from datetime import datetime


def extract_stop_words_and_pos(text, stop_words):
    doc = nlp(text)
    stop_words_in_text = [token.text for token in doc if token.text.lower() in stop_words]
    pos_tags = [f"{token.text}->{token.pos_}" for token in doc if
                token.text.lower() not in stop_words and token.pos_ != "SPACE" and token.pos_ != "PUNCT"]
    return " ".join(stop_words_in_text), " ".join(pos_tags)


if __name__ == '__main__':
    # Read the CSV file
    read_csv_file = pd.read_csv(r"C:\Users\gtush\Desktop\Splits_sets\filtered_interaction.csv").head(n=10)

    print(f'start time: {datetime.now().strftime("%H :: %M min::%S seconds")}')

    # Load the spaCy model
    nlp = spacy.load("en_core_web_sm")
    stop_words = nlp.Defaults.stop_words

    # Process each sentence in the 'Filter DrugName' column
    extracted_data = read_csv_file['Filter DrugName'].apply(lambda x: extract_stop_words_and_pos(str(x), stop_words))
    stop_word_list, pos_tag_list = zip(*extracted_data)

    # Create final sets for stop words and POS tags
    final_stop_word_set = set()
    final_pos_tag_set = set()

    # Split each element in stop_word_list and add words to the set
    for stop_words in stop_word_list:
        split_words = stop_words.split(" ")
        for word in split_words:
            if word:
                final_stop_word_set.add(word)

    # Split each element in pos_tag_list and add words to the set
    for pos_tags in pos_tag_list:
        split_pos_tags = pos_tags.split(" ")
        for tag in split_pos_tags:
            if tag:
                final_pos_tag_set.add(tag)

    # Create lists to hold the stop words and POS tags with their labels
    final_formatted_pos_list = [f"{tag.split('->')[-2]}" for tag in final_pos_tag_set]
    combined_list = list(final_stop_word_set) + list(final_formatted_pos_list)
    stop_words_labels = ["stop_words"] * len(final_stop_word_set)
    formatted_pos_list = [f"{tag.split('->')[1]}->POS" for tag in final_pos_tag_set]

    # Create DataFrames with the results
    data_frame1 = pd.DataFrame({
        "stop_words/POS": combined_list,
        "SW/POS": stop_words_labels + formatted_pos_list
    })

    # Write the results to a new CSV file
    data_frame1.to_csv(r'C:\Users\gtush\Desktop\Splits_sets\combined_filtered_interaction_processed.csv',
                       index=False)

    print(f'end time: {datetime.now().strftime("%H :: %M min::%S seconds")}')
