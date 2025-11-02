import json
from pathlib import Path

def print_dict(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def get_raw_file(filename):
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    data_dir.mkdir(parents=True, exist_ok=True) 
    return data_dir / filename

def get_processed_file(filename):
    data_dir = Path(__file__).parent.parent / "data" / "processed"
    data_dir.mkdir(parents=True, exist_ok=True) 
    return data_dir / filename