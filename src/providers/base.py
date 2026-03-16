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

_CURRENT_REGISTER_ORIGIN = "builtin"

def register_provider(provider_type: str, provider_class, origin=None):
    if origin is None:
        origin = _CURRENT_REGISTER_ORIGIN
        
    name = provider_class.name()
    metadata = {
        "class": provider_class,
        "origin": origin
    }
    
    # Precedence Rule: "user" overrides "builtin", but "builtin" does not override "user"
    def _should_register(registry, new_origin):
        if name not in registry:
            return True
        existing_origin = registry[name]["origin"]
        if new_origin == "builtin" and existing_origin == "user":
            return False
        return True
    
    if provider_type == 'image':
        if _should_register(_IMAGE_PROVIDERS, origin):
            _IMAGE_PROVIDERS[name] = metadata
    elif provider_type == 'quote':
        if _should_register(_QUOTE_PROVIDERS, origin):
            _QUOTE_PROVIDERS[name] = metadata
    elif provider_type == 'palette':
        if _should_register(_PALETTE_PROVIDERS, origin):
            _PALETTE_PROVIDERS[name] = metadata
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
        
    provider_class = registry[name]["class"]
    specific_config = config.get(name, {})
    return provider_class(specific_config)

def list_registered_providers():
    return {
        "image": _IMAGE_PROVIDERS,
        "quote": _QUOTE_PROVIDERS,
        "palette": _PALETTE_PROVIDERS
    }
