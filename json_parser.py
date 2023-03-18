import json
import os

f = open('modinfo.json')
metadata_struct = json.load(f)

def getModInfo(path):
    
    modinfo_path = os.path.join(path, 'modinfo.json')
    if not os.path.isfile(modinfo_path):
        return metadata_struct
    
    fi = open(modinfo_path)
    populated_json = json.load(fi)
    
    return populated_json

def writeModInfo(path, json_obj):
    modinfo_path = os.path.join(path, 'modinfo.json')
    
    if not json_obj:
        json_obj = metadata_struct
    
    with open(modinfo_path, "w") as f:
        json.dump(json_obj,f)
    
