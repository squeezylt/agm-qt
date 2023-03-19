import configparser
import os
from collections import OrderedDict

def writeCategory(mod_folder_path, level, label):
    config = configparser.ConfigParser()
    path = os.path.join(mod_folder_path,'categories.cat')
    config.read(path)
    if not config.has_section("CATEGORIES"):
        config.add_section("CATEGORIES")
    config.set("CATEGORIES", "Level" + str(level), label)
    
    #Order the content of each section alphabetically
    for section in config._sections:
        config._sections[section] = OrderedDict(sorted(config._sections[section].items(), key=lambda t: t[0]))
    
    with open(path, 'w') as configfile:
        config.write(configfile)

def getCategories(mod_folder_path):
    categories = []
    config = configparser.ConfigParser()
    path = os.path.join(mod_folder_path,'categories.cat')
    config.read(path)
    
    for each_section in config.sections():
        for (each_key, each_val) in config.items(each_section):
            categories.append(each_val)
    return categories

def main():
    pass #debug

if __name__ == "__main__":
    main()