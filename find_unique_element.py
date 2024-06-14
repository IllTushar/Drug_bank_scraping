import pandas as pd
import numpy as np
import spacy
from datetime import datetime
import nltk

if __name__ == '__main__':
    # Read the CSV file
    read_csv_file = pd.read_csv(
        r"C:\Users\gtush\Desktop\Splits_sets\filtered_interaction.csv")

    print(f'Start time: {datetime.now().strftime("%H :: %M min::%S seconds")}')

    # Load the spaCy model
    nlp = spacy.load("en_core_web_sm")
    stop_words = nlp.Defaults.stop_words

    combined_string = read_csv_file['clean_sentence'].str.cat(sep=' ')
    word_list = combined_string.split()
    word_list = [x.lower() for x in word_list]
    unique_words = set(word_list)

    df = pd.DataFrame(unique_words)
    df['POS'] = np.nan
    df['stop'] = False

    df.rename({0: 'word'}, axis=1, inplace=True)

    for index, row in df.iterrows():
        word = df.iloc[index]['word']
        if word in stop_words:
            df.at[index, 'stop'] = True

    pos = nltk.pos_tag(df['word'])
    pos = [x[1] for x in pos]
    df['POS'] = pos

    # Write the results to a new CSV file
    df.to_csv(
        r'C:\Users\gtush\Desktop\Splits_sets\combined_filtered_interaction_processed.csv',
        index=False)

    print(f'End time: {datetime.now().strftime("%H :: %M min::%S seconds")}')
