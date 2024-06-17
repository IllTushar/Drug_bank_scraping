import pandas as pd


def split_csv_with_pandas(input_file, rows_per_file):
    df = pd.read_csv(input_file)
    total_rows = len(df)
    num_files = total_rows // rows_per_file + (1 if total_rows % rows_per_file else 0)

    for i in range(num_files):
        start_row = i * rows_per_file
        end_row = start_row + rows_per_file
        split_df = df[start_row:end_row]
        output_file = fr'C:\Users\gtush\Desktop\split_files\split_file_{i + 1}.csv'
        split_df.to_csv(output_file, index=False)


if __name__ == '__main__':
    # Example usage
    input_file = r'C:\Users\gtush\Desktop\csv_folder\FinalMergeDrugBank.csv'
    rows_per_file = 150  # Number of rows per split file
    split_csv_with_pandas(input_file, rows_per_file)
