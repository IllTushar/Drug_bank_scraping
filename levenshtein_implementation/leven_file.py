import pandas as pd
from Levenshtein import distance


def calculate_levenshtein_distances(generic_names, drug_names, desired_similarity=70.0):
    results = []

    for drug_name in drug_names:
        # Handle empty strings
        if not drug_name:
            continue

        # Check for identical drug name before distance calculation
        if drug_name in [name for name, _ in generic_names]:  # Check drug_name exists in list of generic names
            most_similar_generic_name = drug_name
            most_similar_salt_code = None
            highest_similarity = 100.0  # Set similarity to 100% for identical match
            best_levenshtein_distance = 0  # Distance is 0 for identical strings

            # Separate loop to find salt code for identical matches
            for generic_name, salt_code in generic_names:
                if generic_name == drug_name:
                    most_similar_salt_code = salt_code
                    break  # Exit loop after finding matching salt code

        else:
            # Initialize variables
            most_similar_generic_name = None
            most_similar_salt_code = None
            highest_similarity = 0.0
            best_levenshtein_distance = None

            for generic_name, salt_code in generic_names:
                # Handle empty salt codes before concatenation
                combined_name = generic_name if not salt_code else f"{generic_name} {salt_code}"

                # Calculate Levenshtein distance
                levenshtein_distance = distance(drug_name, combined_name)
                similarity_percentage = (
                                                1 - (levenshtein_distance / max(len(drug_name),
                                                                                len(combined_name)))
                                        ) * 100

                if similarity_percentage > highest_similarity:
                    most_similar_generic_name = generic_name
                    most_similar_salt_code = salt_code
                    highest_similarity = similarity_percentage
                    best_levenshtein_distance = levenshtein_distance

        # Only include results meeting the desired similarity threshold
        if highest_similarity >= desired_similarity:
            pass
        else:
            result = {
                "drug_name": drug_name,
                "generic_name": most_similar_generic_name,  # Could be None
                "salt_code": most_similar_salt_code,  # Will include salt code for identical matches
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

    effect_data = pd.read_csv(r"C:\Users\gtush\Desktop\SayaCsv\DrugBankData.csv")

    drug_names = effect_data["Modified Name"].tolist()

    results = calculate_levenshtein_distances(generic_names, drug_names)
    results.to_csv(r"C:\Users\gtush\Desktop\SayaCsv\distance_less_match.csv",index=False)
