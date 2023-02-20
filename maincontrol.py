import os
from pathlib import Path
import filecontrol as fc
import mod_data

class MainControl:

    mod_dir = ""
    mod_folders = []
    selected_mod = None
    mod_container = mod_data.ModContainer()
    

    def __init__(self, parent=None):
        pass

    #private
    def __populateModFolders(self, path):
       
        self.mod_folders = fc.getSubfolders(path)
        

    def setModDir(self, path : str):
        self.mod_dir = path
        self.populateModDataStructure()
    

    def populateModDataStructure(self):
        
        self.__populateModFolders(self.mod_dir)
        if (not self.mod_folders):
            print("mod folders empty")
            return
        for mod in self.mod_folders:
            #print("populating mod")
            mod_class = mod_data.ModClass(os.path.basename(mod),mod)
            mod_class.setEnable(not self.isFolderDisabled(mod))
            if not mod_class.enabled():
                curr_name = os.path.basename(mod)
                item_stripped = curr_name.replace("DISABLED","")
                mod_class.setName(item_stripped)
            self.mod_container.addMod(mod_class)
    
    def getModDataStructure(self):
        return self.mod_container
    
    def toggleMod(self,mod_path, state):
        if not os.path.isdir(mod_path):
            return
        base_dir_name = os.path.basename(mod_path)

        if state:
            item_stripped = base_dir_name.replace("DISABLED","")
        else:
            item_stripped = "DISABLED" + base_dir_name

        print("item stripped is " + item_stripped)
        new_mod_path = fc.renameFolder(mod_path,item_stripped)
        return new_mod_path
    
    def toggleMod(self, mod_id, state):
        mod = self.mod_container.getModById(mod_id)
        if not mod:
            print("Couldn't find mod by id. Error. Id tried was " + mod_id.toString())
            return
        mod_path = mod.path()
        mod_name = mod.name()
        mod_state = mod.enabled()
        
        if not os.path.isdir(mod_path):
            return False
        if state is mod_state:
            return False

        if not mod_state:
            item_stripped = mod_name.replace("DISABLED","")
        else:
            item_stripped = "DISABLED" + mod_name
        
        new_mod_path = fc.renameFolder(mod_path,item_stripped)
        mod.setPath(new_mod_path)
        mod.setEnable(state)
        return True
    
    def setSelectedMod(self,id):
        self.selected_mod = self.mod_container.getModById(id)
        
    def getSelectedMod(self):
        return self.selected_mod
        

        
    def isFolderDisabled(self,folder_name : str):
        return "DISABLED" in folder_name
