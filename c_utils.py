# This script should be renamed
import json

def load_json(filename):
    with open(filename,'r') as file:
        data = json.load(file)
    
    return data

def load_config():
    config_dict = load_json('config.json')
    return config_dict