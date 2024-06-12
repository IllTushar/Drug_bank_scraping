# import pandas as pd
#
# if __name__ == '__main__':
#     read_csv = pd.read_csv(r'C:\Users\gtush\Desktop\Splits_sets\filtered_interaction.csv')
#     print(read_csv.columns)
#     list1 = []
#     for l in read_csv['Filter DrugName']:
#         splits = l.split(" ")
#         list1.extend(splits)
#     unique_values = set(list1)  # Convert the flattened list to a set to get unique values
#     print(unique_values)
#     print(len(unique_values))
#     data_frame = pd.DataFrame({"effect": list(unique_values)})
#     data_frame.to_csv(r"C:\Users\gtush\Desktop\Splits_sets\effect_list2.csv", index=False)


import pandas as pd
import spacy
from datetime import datetime

if __name__ == '__main__':
    read_csv = pd.read_csv(r'C:\Users\gtush\Desktop\Splits_sets\filtered_interaction.csv')

    print(f'started time: {datetime.now().strftime('%H ::%M min::%S sec')}')
    # Load the English model
    nlp = spacy.load('en_core_web_sm')

    list_of_clean_sentence = []
    # The given sentence
    for sentence in read_csv['Filter DrugName']:
        # Process the sentence using spacy
        doc = nlp(sentence)

        # Specify the parts of speech to remove
        pos_to_remove = {'VERB', 'AUX', 'ADP', 'ADV', 'DET', 'PRON', 'CCONJ', 'SCONJ'}

        # Generate the cleaned sentence
        cleaned_sentence = ' '.join(
            [token.text for token in doc if token.pos_ not in pos_to_remove or token.text.lower() == 'combination'])

        list_of_clean_sentence.append(cleaned_sentence)

    data_frame = pd.DataFrame(
        {"unfiltered_data": read_csv['unfiltered_data'], "Filter DrugName": read_csv['Filter DrugName'],
         "clean_sentence": list_of_clean_sentence})
    data_frame.to_csv(r'C:\Users\gtush\Desktop\Splits_sets\filtered_interaction.csv', index=False)
    print(f'completion time: {datetime.now().strftime('%H ::%M min::%S sec')}')
