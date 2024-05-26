import pandas as pd


def filter_data_and_new_col():
    csv_data = pd.read_csv(r"C:\Users\gtush\Desktop\SayaCsv\interactions_subset.csv.csv")
    # Extract the 'Interaction' column and split each element by spaces
    split_interaction = csv_data['Interaction']
    count_in = 0
    count_de = 0
    list_direction_interaction = []
    for index, data in enumerate(split_interaction):
        # Check if "increase" or "decrease" is in the data list
        if "increase" in data:
            count_in += 1
            list_direction_interaction.append("increase")
        elif "decrease" in data:
            count_de += 1
            list_direction_interaction.append("decrease")

    data_frame = pd.DataFrame({"Drug": csv_data['Drug'], "Interaction": split_interaction, "URL": csv_data['URL'],
                               "Base_Drug": csv_data['Base.Drug'], "Interaction Direction": list_direction_interaction})
    data_frame.to_csv(r"C:\Users\gtush\Desktop\SayaCsv\direction_interaction_data.csv")


if __name__ == '__main__':
    filter_data_and_new_col()
