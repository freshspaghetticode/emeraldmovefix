# pokemon.py
class Pokemon:
    def __init__(self, name="", types=["None provided."]):
        self.name = name
        self.pokedex_number = 0
        self.url = ""
        self.types = types
        self.level_up_moves = []
        self.emerald_level_up_moves = []
        self.firered_level_up_moves = []
        self.tm_moves = []
        self.egg_moves = []
        self.emerald_tutor_moves = []
        self.firered_tutor_moves = []
        self.xd_tutor_moves = []
        self.purified_moves = []
        self.mass_outbreak_moves = []
        self.prior_moves = []
        self.event_moves = []

    def cast_to_decomp_learnset_pointer(self, name):
        decomp_learnset_pointer = name
        if decomp_learnset_pointer in ["Nidoran♀","Nidoran♂","Mr. Mime","Farfetch'd","Ho-oh"]:
            if decomp_learnset_pointer == "Nidoran♀":
                decomp_learnset_pointer = "NidoranF"
            if decomp_learnset_pointer == "Nidoran♂":
                decomp_learnset_pointer = "NidoranM"
            if decomp_learnset_pointer == "Mr. Mime":
                decomp_learnset_pointer = "Mrmime"
            if decomp_learnset_pointer == "Farfetch'd": 
                decomp_learnset_pointer = "Farfetchd"
            if decomp_learnset_pointer == "Ho-Oh":
                decomp_learnset_pointer = "HoOh"
        decomp_learnset_pointer = "s" + decomp_learnset_pointer + "LevelUpLearnset"
        return decomp_learnset_pointer