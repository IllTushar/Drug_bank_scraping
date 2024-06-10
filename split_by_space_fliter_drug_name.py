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

# Load the English tokenizer and the part-of-speech tagger from spaCy
nlp = spacy.load("en_core_web_sm")

if __name__ == '__main__':
    read_csv = pd.read_csv(r'C:\Users\gtush\Desktop\Splits_sets\filtered_interaction.csv')
    print(read_csv.columns)
    list1 = []
    for l in read_csv['Filter DrugName']:
        splits = l.split(" ")
        list1.extend(splits)  # Extend the list instead of appending a sublist

    # Perform part-of-speech tagging on the words using spaCy
    pos_tags = []
    for word in list1:
        if word.strip():  # Check if the word is non-empty
            doc = nlp(word)
            pos_tags.append((word, doc[0].pos_))

    # Create DataFrame from the list of tuples
    pos_df = pd.DataFrame(pos_tags, columns=['Word', 'Part of Speech'])

    # Save the DataFrame to a CSV file
    pos_df.to_csv(r'C:\Users\gtush\Desktop\Splits_sets\unique_values_with_pos.csv', index=False)

