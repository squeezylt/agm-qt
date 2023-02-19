class ModClass:
    modname = ""
    modpath = ""
    enabled = False
    
    def __init__(self, name, path, enabled):
        self.modname = name
        self.modpath = path
        self.enabled = enabled