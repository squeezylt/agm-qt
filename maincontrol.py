import os
from pathlib import Path
import filecontrol as fc
import mod_data
import cat_parser as cat
import json_parser as jp

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
        
    def writeModCategory(self, id, level, category_text):
        mod = self.mod_container.getModById(id)
        path = mod.path()
        #cat.writeCategory(path,level,category_text)
        #mod.categories[level] = category_text
        mod.appendCategories(level,category_text)

    def populateModDataStructure(self):
        self.mod_container.clear()
        self.__populateModFolders(self.mod_dir)
        
        if (not self.mod_folders):
            print("mod folders empty")
            return
        for mod in self.mod_folders:
            #print("populating mod")
            mod_class = mod_data.ModClass(os.path.basename(mod),mod)
            mod_class.setEnable(not self.isFolderDisabled(mod))
            #mod_class.setMetadata(jp.getModInfo(mod))
            #mod_class.setCategories(cat.getCategories(mod))
            #print("Categories this this mod are " + self.getCategories(mod))
            if not mod_class.enabled():
                curr_name = os.path.basename(mod)
                item_stripped = curr_name.replace("DISABLED","")
                mod_class.setName(item_stripped)
            self.mod_container.addMod(mod_class)
    
    def getModDataStructure(self):
        return self.mod_container
    
    def getCategories(self,id):
        mod = self.mod_container.getModById(id)
        categories = mod.getCategories()
        return categories
    
    def getCategory(self, mod_id, level):
        mod = self.mod_container.getModById(mod_id)
        category = mod.getCategory(level)
        return category
        
    
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
            
        #verbose lol    
        mod.setEnable(state)
        disable_handled_name_for_path = self.handleDisablePathFormat(mod_id,mod_name)
        
        new_mod_path = fc.renameFolder(mod_path,disable_handled_name_for_path)
        mod.setPath(new_mod_path)
        return True
    
    def setSelectedMod(self,id):
        self.selected_mod = self.mod_container.getModById(id)
        
    def getSelectedMod(self):
        return self.selected_mod
    
    def renameMod(self,id,new_name):
        mod = self.mod_container.getModById(id)
        mod_path = mod.path()
        disable_handled_name_for_path = self.handleDisablePathFormat(id,new_name)
        new_path =fc.renameFolder(mod_path,disable_handled_name_for_path)
        mod.setName(new_name)
        mod.setPath(new_path)
        
    def getModName(self, id):
        mod = self.mod_container.getModById(id)
        return mod.name()
        
    def isFolderDisabled(self,folder_name : str):
        return "DISABLED" in folder_name
    
    #given a original path, and a new name,
    #format the new path, and add the 'DISABLED' line if needed

    def handleDisablePathFormat(self, id, mod_name):
        mod = self.mod_container.getModById(id)
        mod_state = mod.enabled()
        if not mod:
            print("Couldn't find mod by id. Error. Id tried was " + id.toString())
            return
   
        #if mod is enabled.
        if not mod_state:
            return "DISABLED" + mod_name
            
        return mod_name
    
    