import os
from pathlib import Path
import filecontrol as fc

class MainControl:

    mod_dir = ""
    mod_folders = []
    current_mod_name = ""
    current_mod_path = ""
    

    def __init__(self, parent=None):
        print('init')

    #private
    def __populateModFolders(self, path):
       
        self.mod_folders = fc.getSubfolders(path)
        

    def setModDir(self, path : str):
        self.mod_dir = path

    

    def getModDataStructure(self):
      
        mod_dict = {}
        
        self.__populateModFolders(self.mod_dir)
        if (not self.mod_folders):
            print("mod folders empty")
            return
        for folder in self.mod_folders:
            if self.isFolderDisabled(folder):
                
                mod_dict[folder] = False
            else:
                mod_dict[folder] = True
            
        return mod_dict
    
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
    
    def setSelectedMod(self,path:str,name:str):
        self.current_mod_path = path
        self.current_mod_name = name
        
    def getSelectedMod(self):
        return self.current_mod_path, self.current_mod_name
        

        
    def isFolderDisabled(self,folder_name : str):
        return "DISABLED" in folder_name