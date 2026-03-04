from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @classmethod
    @abstractmethod
    def name(cls) -> str:
        pass

    @abstractmethod
    def generate(self, seed: int, env: dict, theme_hints: dict) -> any:
        pass

class ImageProvider(BaseProvider):
    pass

class QuoteProvider(BaseProvider):
    pass

class PaletteProvider(BaseProvider):
    pass

# Registry System
_IMAGE_PROVIDERS = {}
_QUOTE_PROVIDERS = {}
_PALETTE_PROVIDERS = {}

def register_provider(provider_type: str, provider_class):
    name = provider_class.name()
    if provider_type == 'image':
        _IMAGE_PROVIDERS[name] = provider_class
    elif provider_type == 'quote':
        _QUOTE_PROVIDERS[name] = provider_class
    elif provider_type == 'palette':
        _PALETTE_PROVIDERS[name] = provider_class
    else:
        raise ValueError(f"Unknown provider type: {provider_type}")

def get_provider(provider_type: str, name: str, config: dict):
    """Instantiates a provider with its specific config block."""
    registry = {}
    if provider_type == 'image':
        registry = _IMAGE_PROVIDERS
    elif provider_type == 'quote':
        registry = _QUOTE_PROVIDERS
    elif provider_type == 'palette':
        registry = _PALETTE_PROVIDERS
        
    if name not in registry:
        raise ValueError(f"Provider '{name}' not found for type '{provider_type}'")
        
    provider_class = registry[name]
    specific_config = config.get(name, {})
    return provider_class(specific_config)

def list_registered_providers():
    return {
        "image": list(_IMAGE_PROVIDERS.keys()),
        "quote": list(_QUOTE_PROVIDERS.keys()),
        "palette": list(_PALETTE_PROVIDERS.keys())
    }
