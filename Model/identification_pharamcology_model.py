class Model:
    def __init__(self, drug_title, generic, type_drug, background, base_url, indication, pharmacodynamics, mechanism,
                 absorption, half_life, toxicity):
        self.drug_title = drug_title
        self.generic = generic
        self.type_drug = type_drug
        self.background = background
        self.base_url = base_url
        self.indication = indication
        self.pharamacodynamics = pharmacodynamics
        self.mechanism = mechanism
        self.absorption = absorption
        self.half_life = half_life
        self.toxicity = toxicity

    @property
    def get_drug_title(self):
        return self.drug_title

    @property
    def get_generic(self):
        return self.generic

    @property
    def get_type_drug(self):
        return self.type_drug

    @property
    def get_background(self):
        return self.background

    @property
    def get_base_url(self):
        return self.base_url

    @property
    def get_indication(self):
        return self.indication

    @property
    def get_pharmacodynamics(self):
        return self.pharamacodynamics

    @property
    def get_mechanism(self):
        return self.mechanism

    @property
    def get_absorption(self):
        return self.absorption

    @property
    def get_half_life(self):
        return self.half_life

    @property
    def get_toxicity(self):
        return self.toxicity
