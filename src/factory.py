from src.providers.quotes import *
from src.providers.images import *
from src.providers.text import *
from src.providers.profiles import LocalFileProfileProvider

def get_config_from_path(config, provider_path):
    """
    Traverses config using a path string like 'pollinations:text'.
    Returns the specific config dict and the base provider name.
    Example: 'pollinations:text' -> returns (config['pollinations']['text'], 'pollinations')
    """
    parts = provider_path.split(':')
    base_name = parts[0]
    
    current_config = config
    try:
        if len(parts) > 1:
            for part in parts:
                current_config = current_config.get(part, {})
        else:
            current_config = config.get(base_name, {})
    except AttributeError:
        current_config = {}
        
    return current_config, base_name

def get_profile_provider(config):
    # Default to local_file, could be 'url' or 'notion' in future
    name = config.get('profile_provider', 'local_file')
    if name == 'local_file':
        return LocalFileProfileProvider(config.get('profile_path', 'profiles/examples/stoic_profile.md'))
    else:
        return LocalFileProfileProvider(config.get('profile_path', 'profiles/examples/stoic_profile.md'))

def get_quote_provider(config):
    name = config.get('quote_provider', 'zenquotes')
    specific_config, base_name = get_config_from_path(config, name)
    
    if base_name == 'csv':
        # Support nested config 'file' key or fallback to root 'quotes_file'
        path = specific_config.get('file', config.get('quotes_file', 'quotes.csv'))
        return CsvQuoteProvider(path)
    elif base_name == 'yaml':
        path = specific_config.get('file', config.get('quotes_file', 'quotes.yaml'))
        return YamlQuoteProvider(path)
    elif base_name == 'pollinations':
        # specific_config should point to ['pollinations']['text'] if name was 'pollinations:text'
        if 'text' in specific_config and 'image' in specific_config:
             # It's the parent, dig into 'text' defaults
             specific_config = specific_config.get('text', {})

        return PollinationsQuoteProvider(
            model=specific_config.get('model', 'openai'),
            api_key=specific_config.get('api_key'),
            prompt_template=specific_config.get('prompt_template') or config.get('prompts', {}).get('quote'),
            request_params=specific_config.get('request_params', {})
        )
    elif base_name == 'llm':
        # specific_config is either config['llm'] or config['llm']['sub'] etc.
        return LLMQuoteProvider(
            specific_config.get('base_url', 'http://localhost:11434/v1'),
            specific_config.get('api_key', 'ollama'),
            specific_config.get('model', 'llama3'),
            specific_config.get('prompt_template') or config.get('prompts', {}).get('quote'),
            specific_config.get('request_params', {})
        )
    elif base_name == 'huggingface':
        # specific_config should point to ['huggingface'] or ['huggingface']['text']
        if 'text' in specific_config and 'image' in specific_config:
             specific_config = specific_config.get('text', {})
        
        return HuggingFaceQuoteProvider(
            model=specific_config.get('model', 'Qwen/Qwen2.5-7B-Instruct'),
            api_key=specific_config.get('api_key') or config.get('huggingface', {}).get('api_key'),
            prompt_template=specific_config.get('prompt_template') or config.get('prompts', {}).get('quote')
        )
    else:
        return ZenQuotesProvider()

def get_image_provider(config):
    name = config.get('image_provider', 'local_dir')
    specific_config, base_name = get_config_from_path(config, name)

    if base_name == 'local_dir':
        # Support nested config 'path' key or fallback to root 'local_image_dir'
        path = specific_config.get('path', config.get('local_image_dir', ''))
        return LocalDirImageProvider(path)
    elif base_name == 'huggingface':
        if 'text' in specific_config and 'image' in specific_config:
             specific_config = specific_config.get('image', {})

        return HuggingFaceImageProvider(
            model=specific_config.get('model', 'stabilityai/stable-diffusion-2-1'),
            api_key=specific_config.get('api_key') or config.get('huggingface', {}).get('api_key'),
            seed=specific_config.get('seed')
        )
    else:
        # Assume Pollinations/generic
        if 'text' in specific_config and 'image' in specific_config:
             specific_config = specific_config.get('image', {})

        return PollinationsImageProvider(
            model=specific_config.get('model', 'flux'),
            nologo=specific_config.get('nologo', True),
            api_key=specific_config.get('api_key'),
            seed=specific_config.get('seed', 42) 
        )

def get_text_provider(config, provider_name):
    specific_config, base_name = get_config_from_path(config, provider_name)

    if base_name == 'llm':
        return LLMTextProvider(
            specific_config.get('base_url', 'http://localhost:11434/v1'),
            specific_config.get('api_key', 'ollama'),
            specific_config.get('model', 'llama3'),
            specific_config.get('request_params', {})
        )
    elif base_name == 'pollinations':
        if 'text' in specific_config and 'image' in specific_config:
             specific_config = specific_config.get('text', {})

        return PollinationsTextProvider(
            model=specific_config.get('model', 'openai'),
            api_key=specific_config.get('api_key')
        )
    elif base_name == 'huggingface':
        if 'text' in specific_config and 'image' in specific_config:
             specific_config = specific_config.get('text', {})

        return HuggingFaceTextProvider(
            model=specific_config.get('model', 'Qwen/Qwen2.5-7B-Instruct'),
            api_key=specific_config.get('api_key') or config.get('huggingface', {}).get('api_key')
        )
    return None
