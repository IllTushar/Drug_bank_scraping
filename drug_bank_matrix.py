import pandas as pd

if __name__ == '__main__':
    # Read the CSV file
    read_file = pd.read_csv(r'C:\Users\gtush\Desktop\csv_folder\FinalMergeDrugBank.csv')
    name = read_file['Name']
    data_frame = pd.DataFrame(columns=name, index=name)
    # Save the DataFrame to a CSV file
    data_frame.to_csv(r'C:\Users\gtush\Desktop\csv_folder\DrugMatrixBankData.csv')
