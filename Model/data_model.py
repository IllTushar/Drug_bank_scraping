class ModelClass:
    def __init__(self, drug_name_list=None, drug_interaction_list=None, drug_url_list=None):
        # Initialize the lists if they are not provided
        self._drug_name_list = drug_name_list if drug_name_list is not None else []
        self._drug_interaction_list = drug_interaction_list if drug_interaction_list is not None else []
        self._drug_url_list = drug_url_list if drug_url_list is not None else []

    def get_drug_list(self):
        # Combine the lists into a list of dictionaries for easy access
        drug_list = []
        for name, interaction, url in zip(self.drug_name_list, self.drug_interaction_list, self.drug_url_list):
            drug_list.append({
                'name': name,
                'interaction': interaction,
                'url': url
            })
        return drug_list

    @property
    def drug_name_list(self):
        return self._drug_name_list

    @property
    def drug_interaction_list(self):
        return self._drug_interaction_list

    @property
    def drug_url_list(self):
        return self._drug_url_list
