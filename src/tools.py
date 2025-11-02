import json

def print_dict(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))