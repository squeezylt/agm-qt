import os
from pathlib import Path

def getSubfolders(parent_folder_path: str, depth = 1):
    if not os.path.isdir(parent_folder_path):
            return
    sub_folders = []
    for file in os.listdir(parent_folder_path):
        d = os.path.join(parent_folder_path, file)
        if os.path.isdir(d):
            #print(d)
            sub_folders.append(d)
    return sub_folders
        

def renameFolder(input_folder_path:str, new_folder_name:str):
    if not os.path.isdir(input_folder_path):
            return
    
    base_path_name = Path(input_folder_path).parent
            

    new_mod_path = os.path.join(base_path_name,new_folder_name)

    try:
        os.rename(input_folder_path,new_mod_path)
    except IOError as e:
        print(e.errno)
        print("IO ERROR RENAMING")
        print ('error message:'), os.strerror(e.errno)
        return ""
    
    return new_mod_path
        


    
    