from Levenshtein import distance
import pandas as pd


def calculate_levenshtein_distances(generic_names, drug_names, desired_similarity=50.0):
    results = []

    for drug_name in drug_names:
        # Handle empty strings
        if not drug_name:
            continue  # Skip empty drug names

        # Initialize variables to track the most similar generic name
        most_similar_generic_name = None
        highest_similarity = 0.0
        best_levenshtein_distance = None

        for generic_name in generic_names:
            # Handle empty generic names
            if not generic_name:
                continue  # Skip empty generic names

            # Calculate Levenshtein distance
            levenshtein_distance = distance(drug_name, generic_name)
            similarity_percentage = (
                                            1 - (levenshtein_distance / max(len(drug_name), len(generic_name)))
                                    ) * 100

            if similarity_percentage > highest_similarity:
                most_similar_generic_name = generic_name
                highest_similarity = similarity_percentage
                best_levenshtein_distance = levenshtein_distance

        # Only include results meeting the desired similarity threshold
        if highest_similarity >= desired_similarity:
            result = {
                "drug_name": drug_name,
                "generic_name": most_similar_generic_name,  # Could be None
                "levenshtein_distance": best_levenshtein_distance if most_similar_generic_name else None,
                "similarity_percentage": highest_similarity,
            }
            results.append(result)

    # Convert results to a DataFrame
    data_set = pd.DataFrame(results)
    return data_set


if __name__ == "__main__":
    # Assuming CSV files have 'Name' and 'Drug' columns respectively
    drug_bank_data = pd.read_csv(r"C:\Users\gtush\Desktop\SayaCsv\DrugBankData1.csv")
    generic_names = drug_bank_data["Name"].tolist()

    effect_data = pd.read_csv(r"C:\Users\gtush\Desktop\SayaCsv\effect3.csv")
    drug_names = effect_data["Drug"].tolist()

    results = calculate_levenshtein_distances(generic_names, drug_names)
    results.to_csv(r"C:\Users\gtush\Desktop\SayaCsv\distance_csv.csv", index=False)
