import pandas as pd

if __name__ == '__main__':
    name_data = []
    read_file = pd.read_csv(r'C:\Users\gtush\Desktop\SayaCsv\DrugBankData.csv')

    data = read_file['Name']
    print(read_file.columns)
    for l in data:
        name_data.append(l.lower())
    read_file.insert(loc=1, column='Modified Name', value=name_data)
    read_file.to_csv(r'C:\Users\gtush\Desktop\SayaCsv\DrugBankData.csv',index=False)
