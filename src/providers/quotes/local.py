import csv
import yaml
import random
from src.interfaces import QuoteProvider

class CsvQuoteProvider(QuoteProvider):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_quote(self, profile_content: str) -> str:
        try:
            with open(self.file_path, 'r') as f:
                reader = csv.reader(f)
                quotes = list(reader)
                if not quotes:
                    return "No quotes found in CSV."
                # Assume quote is in the first column
                return random.choice(quotes)[0]
        except Exception as e:
            return f"Error reading CSV: {e}"

class YamlQuoteProvider(QuoteProvider):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_quote(self, profile_content: str) -> str:
        try:
            with open(self.file_path, 'r') as f:
                data = yaml.safe_load(f)
                if isinstance(data, list):
                    item = random.choice(data)
                    if isinstance(item, str):
                        return item
                    elif isinstance(item, dict) and 'text' in item:
                        return item['text']
                    else:
                         return str(item)
                return "Invalid YAML format. Expected a list."
        except Exception as e:
             return f"Error reading YAML: {e}"
