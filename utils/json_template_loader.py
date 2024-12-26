import json

def load_templates(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)
