#move.py
class Move:
    def __init__(self, name, level=0, type="None provided", is_damaging=False):
        self.name = name
        self.level = level
        self.type = type
        self.is_damaging = is_damaging
        self.decomp_name = self.cast_to_decomp_name(name)
    
    def cast_to_decomp_name(self, name):
        decomp_name = name.upper()
        if " " in decomp_name:
            decomp_name = decomp_name.replace(" ", "_")
        if "-" in decomp_name:
            decomp_name = decomp_name.replace("-", "_")
        decomp_name = "MOVE_" + decomp_name
        return decomp_name