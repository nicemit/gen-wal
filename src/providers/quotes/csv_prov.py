import csv
import random
import os
from src.providers.base import QuoteProvider, register_provider
from src.config import XDG_DATA_HOME

class CsvQuoteProvider(QuoteProvider):
    def __init__(self, config):
        self.config = config
        
    @classmethod
    def name(cls):
        return "csv"
        
    def generate(self, seed: int, env: dict, theme_hints: dict) -> str:
        # Default fallback quotes
        quotes = [
            "The impediment to action advances action. What stands in the way becomes the way.",
            "You have power over your mind - not outside events.",
            "If it is not right do not do it; if it is not true do not say it.",
            "Simplicity is the ultimate sophistication.",
            "Focus on the signal, not the noise."
        ]
        
        # Read from CSV if available
        # Check config for path, else fallback to ~/.local/share/genwal/quotes.csv
        file_path = self.config.get('file', os.path.join(XDG_DATA_HOME, 'genwal', 'quotes.csv'))
        
        if os.path.exists(file_path):
            try:
                with open(file_path, mode='r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    file_quotes = [row[0] for row in reader if row]
                    if file_quotes:
                        quotes = file_quotes
            except Exception as e:
                print(f"Failed to read CSV quotes: {e}")
                
        rng = random.Random(seed)
        return rng.choice(quotes)

register_provider('quote', CsvQuoteProvider)
