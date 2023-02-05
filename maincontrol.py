import os
from pathlib import Path

class MainControl:

    mod_dir = str
    mod_folders = []

    def __init__(self, parent=None):
        print('init')

    #private
    def __populateModFolders(self, path = mod_dir):
        mod_folders = []
        for file in os.listdir(self.mod_dir):
            d = os.path.join(self.mod_dir, file)
            if os.path.isdir(d):
                #print(d)
                mod_folders.append(d)
        self.mod_folders = mod_folders
        

    def setModDir(self, path : str):
        self.mod_dir = path

    

    def getModDataStructure(self):
      
        mod_dict = {}
        
        self.__populateModFolders()
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
        base_path_name = Path(mod_path).parent
        if state:
            item_stripped = base_dir_name.replace("DISABLED","")
        else:
            item_stripped = "DISABLED" + base_dir_name
            
        #os.name(mod_path, )
        new_mod_path = os.path.join(base_path_name,item_stripped)
        
        print("renaming " + mod_path + " to " + new_mod_path)
        os.rename(mod_path,new_mod_path)
        return new_mod_path
        

        
    def isFolderDisabled(self,folder_name : str):
        return "DISABLED" in folder_name