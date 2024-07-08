import pandas as pd

if __name__ == '__main__':
    # Read the CSV file
    read_csv = pd.read_csv(r'C:\Users\gtush\Desktop\SayaCsv\effect3.csv')

    # Drop the 'Unnamed: 0' column and update the DataFrame
    delete_col = read_csv.drop('Unnamed: ', axis=1)

    delete_col.to_csv(r'C:\Users\gtush\Desktop\SayaCsv\effect3.csv', index=False)

    # Print the columns of the updated DataFrame
    print(delete_col.columns)
