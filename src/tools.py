import json
from pathlib import Path

def print_dict(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def get_raw_file(filename: str) -> Path:
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    file_path = data_dir / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    return file_path

def get_processed_file(filename: str) -> Path:
    data_dir = Path(__file__).parent.parent / "data" / "processed"
    file_path = data_dir / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    return file_path