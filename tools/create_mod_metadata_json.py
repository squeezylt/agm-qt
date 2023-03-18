import json
import os

modinfo_blank = '''{
  "info": {
    "name": "",
    "description": "",
    "urls": [],
    "images": [],
    "videos": [],
    "version": ""
  },
  "author": {
    "name": "",
    "urls": [],
    "sponsor": []
  },
  "categories": [],
  "tags": [],
  "order": null,
  "like": false
}'''

def writeField(modinfo, section, value):
    modinfo[section] = value

if __name__ == "__main__":
    mod_info = json.loads(modinfo_blank)
    print("Welcome. Enter blank to add empty entry, control+c to quit. \n modinfo.json will be written to current directory")
    txt = input("Enter mod name: ")
    writeField(mod_info['info'], "name", str(txt))
    txt = input("Enter short mod description: ")
    writeField(mod_info['info'], "description", str(txt))
    
    
    txt = input("Enter mod URL, or enter multiple separated by a comma: ")
    list = txt.split(',')
    writeField(mod_info['info'], "urls", list)
    
    #todo, images field. unsure of link format
    
    #todo videos field
    txt = input("Enter mod version number. (Ex 1.3, or 0.4.6): ")
    writeField(mod_info['info'], "version", str(txt))
    
    txt = input("Enter mod author's name/nickname: ")
    writeField(mod_info['author'], "name", str(txt))
    
    #todo other author metadata
    
    txt = input("Enter Mod Categories. Separate each category with a comma. This is used for sorting, \nfirst category is top level: ")
    list = txt.split(',')
    writeField(mod_info, "categories", list)
    
    txt = input("Enter Mod Tags. Separate each category with a comma. This is used searching/grouping/sorting, \nput as many as you like: ")
    list = txt.split(',')
    writeField(mod_info, "tags", list)
    
    print('All set, writing categories to current directory as modinfo.json')
    modinfo_path = os.path.join(os.getcwd(), 'modinfo.json')
    
    with open(modinfo_path, "w") as f:
        json.dump(mod_info, f, ensure_ascii=False, indent=4)
    
    
    
