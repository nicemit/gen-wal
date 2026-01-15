import requests
from src.interfaces import QuoteProvider

class ZenQuotesProvider(QuoteProvider):
    def get_quote(self, profile_content: str) -> str:
        try:
            response = requests.get("https://zenquotes.io/api/random")
            data = response.json()
            return f"{data[0]['q']} - {data[0]['a']}"
        except Exception as e:
            return "Discipline is doing what needs to be done, even if you don't want to do it."
