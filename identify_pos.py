import pandas as pd
import spacy
from datetime import datetime


def extract_stop_words_and_pos(text, stop_words):
    doc = nlp(text)
    stop_words_in_text = [token.text for token in doc if token.text.lower() in stop_words]
    pos_tags = [f"{token.text}->{token.pos_}" for token in doc if
                token.text.lower() not in stop_words and token.pos_ not in ["SPACE", "PUNCT"]]
    return " ".join(stop_words_in_text), " ".join(pos_tags)


if __name__ == '__main__':
    # Read the CSV file
    read_csv_file = pd.read_csv(r"C:\Users\gtush\Desktop\Splits_sets\filtered_interaction.csv").head(n=1000)

    print(f'Start time: {datetime.now().strftime("%H :: %M min::%S seconds")}')

    # Load the spaCy model
    nlp = spacy.load("en_core_web_sm")
    stop_words = nlp.Defaults.stop_words

    # Process each sentence in the 'Filter DrugName' column
    extracted_data = read_csv_file['Filter DrugName'].apply(lambda x: extract_stop_words_and_pos(str(x), stop_words))
    stop_word_list, pos_tag_list = zip(*extracted_data)

    # Create final sets for stop words and POS tags
    final_stop_word_set = {word for stop_words in stop_word_list for word in stop_words.split() if word}
    final_pos_tag_set = {tag for pos_tags in pos_tag_list for tag in pos_tags.split() if tag}

    # Create lists to hold the stop words and POS tags with their labels
    combined_list = list(final_stop_word_set) + [tag.split('->')[0] for tag in final_pos_tag_set]
    labels_list = ["stop_words"] * len(final_stop_word_set) + [f"{tag.split('->')[1]}->POS" for tag in final_pos_tag_set]

    # Create DataFrame with the results
    data_frame1 = pd.DataFrame({
        "stop_words/POS": combined_list,
        "SW/POS": labels_list
    })

    # Write the results to a new CSV file
    data_frame1.to_csv(r'C:\Users\gtush\Desktop\Splits_sets\combined_filtered_interaction_processed.csv', index=False)

    print(f'End time: {datetime.now().strftime("%H :: %M min::%S seconds")}')
