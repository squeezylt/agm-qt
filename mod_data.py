from PyQt5.QtCore import QUuid

class ModContainer:
    mod_list = []
    def __init__(self):
        pass

    def addMod(self, mod):
        self.mod_list.append(mod)
    
    def removeModById(self,id):
        for mod in self.mod_list:
            if mod.id() is id:
                self.mod_list.remove(mod)
                return mod
        return None
        
    def getModById(self, id):
        for mod in self.mod_list:
            if mod.id() == id:
                return mod
        return None
    def items(self):
        return self.mod_list
            
    
    

class ModClass:
    modname = ""
    modpath = ""
    modenabled = False
    #string list, in order
    categories = []
    uid = ""
    
    def __init__(self, name, path):
        self.modname = name
        self.modpath = path
        self.uid = QUuid.createUuid()
        
    def setCategories(self, categories):
        self.categories = categories
        
    def setEnable(self,toggle):
        self.modenabled=toggle
            
    def setName(self,new_name):
        self.modname = new_name
        
    def setPath(self,new_path):
        self.modpath = new_path
    
    def printId(self):
        print(self.uid.toString())
        
    def enabled(self):
        return self.modenabled
    def name(self):
        return self.modname
    def path(self):
        return self.modpath
    def id(self):
        return self.uid
        
    
def main():
    mu = ModClass("hi","path", "yes")
    mu.printId()
    

if __name__ == "__main__":
    main()