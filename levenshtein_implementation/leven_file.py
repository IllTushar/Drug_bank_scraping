import pandas as pd
from Levenshtein import distance  # Ensure you have the python-Levenshtein package installed


def calculate_levenshtein_distances(generic_names, drug_names, desired_similarity=70.0):
    results = []

    for drug_name in drug_names:
        # Handle empty strings
        if not drug_name:
            continue  # Skip empty drug names

        # Initialize variables to track the most similar generic name
        most_similar_generic_name = None
        most_similar_salt_code = None
        highest_similarity = 0.0
        best_levenshtein_distance = None

        for generic_name, salt_code in generic_names:
            # Handle empty generic names
            if not generic_name:
                continue  # Skip empty generic names

            # Concatenate generic_name and salt_code for distance calculation
            combined_name = f"{generic_name} {salt_code}" if salt_code else generic_name

            # Calculate Levenshtein distance
            levenshtein_distance = distance(drug_name.lower(), combined_name.lower())
            similarity_percentage = (
                                            1 - (levenshtein_distance / max(len(drug_name.lower()),
                                                                            len(combined_name.lower())))
                                    ) * 100

            if similarity_percentage > highest_similarity:
                most_similar_generic_name = generic_name
                most_similar_salt_code = salt_code
                highest_similarity = similarity_percentage
                best_levenshtein_distance = levenshtein_distance

        # Only include results meeting the desired similarity threshold
        if highest_similarity >= desired_similarity:
            result = {
                "drug_name": drug_name.lower(),
                "generic_name": most_similar_generic_name,  # Could be None
                "salt_code": most_similar_salt_code,  # Could be None
                "levenshtein_distance": best_levenshtein_distance if most_similar_generic_name else None,
                "similarity_percentage": highest_similarity,
            }
            results.append(result)

    # Convert results to a DataFrame
    data_set = pd.DataFrame(results)
    return data_set


if __name__ == "__main__":
    # Assuming CSV files have 'generic_name' and 'salt_code' columns respectively
    drug_bank_data = pd.read_csv(r"C:\Users\gtush\Desktop\SayaCsv\Salt_Codes.csv.csv")

    # Combine 'generic_name' and 'salt_code' into a tuple for each entry
    generic_names = list(zip(drug_bank_data['generic_name'], drug_bank_data['salt_code']))
    print(generic_names)

    effect_data = pd.read_csv(r"C:\Users\gtush\Desktop\SayaCsv\DrugBankData.csv")

    drug_names = effect_data["Name"].tolist()

    results = calculate_levenshtein_distances(generic_names, drug_names)
    results.to_csv(r"C:\Users\gtush\Desktop\SayaCsv\distance_csv.csv", index=False)
