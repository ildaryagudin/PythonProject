import json
from typing import List, Dict


def load_transactions(file_path: str) -> List[Dict]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if isinstance(data, list):
            return data
        else:
            print(f'Warning: {file_path} does not contain a valid list of transactions.')

    except FileNotFoundError:
        print(f'File {file_path} was not found.')
    except json.JSONDecodeError:
        print(f'{file_path} contains invalid JSON format.')

    return []