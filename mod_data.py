from PyQt5.QtCore import QUuid
import json
import json_parser as jp

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
    def clear(self):
        self.mod_list.clear()
        
            
    
    

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
        self.readAndPopulateMetadata()

        
    def setCategories(self, categories):
        self.categories = categories
        
    def getCategories(self):
        return self.categories
    
    def getCategory(self,level):
        if len(self.categories) <= level:
            return None
        if not self.categories:
            return None
        #print("returning level " + str(level))
        return self.categories[level]
        
    def setEnable(self,toggle):
        self.modenabled=toggle
            
    def setName(self,new_name):
        self.modname = new_name
        
    def setPath(self,new_path):
        self.modpath = new_path
    
    def printId(self):
        print(self.uid.toString())
        
    def readAndPopulateMetadata(self):
        self.metadata = jp.getModInfo(str(self.path()))
        cat = self.metadata['categories']
        if not cat:
            return

        self.categories = cat  
        
    def enabled(self):
        return self.modenabled
    def name(self):
        return self.modname
    def path(self):
        return self.modpath
    def id(self):
        return self.uid
    
    def updateJsonModInfoFile(self):
        jp.writeModInfo(str(self.path()), self.metadata)
    
    def writeMetaDataSection(self,section,value):
        #def writeField(modinfo, section, value):
        self.metadata[section] = value
        self.updateJsonModInfoFile()
        
        #callback to reupdate class info from file
        self.readAndPopulateMetadata()
        
    def appendCategories(self, level, value):
        if len(self.categories) <= 0 or level >= len(self.categories):
            self.categories.append(value)
        else:    
            self.categories[level] = value
        self.writeMetaDataSection('categories',self.categories)
        
    
def main():
    mu = ModClass("hi","path", "yes")
    mu.printId()
    

if __name__ == "__main__":
    main()