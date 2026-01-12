import os
import sys
import time
import yaml
import argparse
import subprocess
from src.providers.quotes import *
from src.providers.images import *
from src.providers.profiles import LocalFileProfileProvider
from src.renderer import WallpaperRenderer

def load_config(path="config.yaml"):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def get_profile_provider(config):
    # Default to local_file, could be 'url' or 'notion' in future
    name = config.get('profile_provider', 'local_file')
    if name == 'local_file':
        return LocalFileProfileProvider(config.get('profile_path', 'profiles/amit_motivation_profile.md'))
    else:
        return LocalFileProfileProvider(config.get('profile_path', 'profiles/amit_motivation_profile.md'))

def get_quote_provider(config):
    name = config.get('quote_provider', 'zenquotes')
    if name == 'llm':
        llm_config = config.get('llm', {})
        return LLMQuoteProvider(
            llm_config.get('base_url', 'http://localhost:11434/v1'),
            llm_config.get('api_key', 'ollama'),
            llm_config.get('model', 'llama3'),
            llm_config.get('prompt_template'),
            llm_config.get('request_params', {})
        )
    elif name == 'csv':
        return CsvQuoteProvider(config.get('quotes_file', 'quotes.csv'))
    elif name == 'yaml':
        return YamlQuoteProvider(config.get('quotes_file', 'quotes.yaml'))
    else:
        return ZenQuotesProvider()

def get_image_provider(config):
    name = config.get('image_provider', 'pollinations')
    if name == 'local_dir':
        return LocalDirImageProvider(config.get('local_image_dir', ''))
    else:
        # Pollinations config
        poll_config = config.get('pollinations', {})
        return PollinationsImageProvider(
            model=poll_config.get('model'),
            nologo=poll_config.get('nologo', True),
            api_key=poll_config.get('api_key')
        )

def set_wallpaper(image_path):
    # GNOME / Ubuntu
    uri = f"file://{os.path.abspath(image_path)}"
    try:
        # Set for both light and dark themes
        subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri], check=True)
        subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", uri], check=True)
        print(f"Wallpaper set to: {uri}")
    except Exception as e:
        print(f"Error setting wallpaper: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    args = parser.parse_args()

    # Load Config
    config_path = os.path.join(os.path.dirname(__file__), args.config)
    config = load_config(config_path)

    # Load Profile
    print("Fetching profile...")
    profile_provider = get_profile_provider(config)
    profile_content = profile_provider.get_profile()

    # 1. Get Quote
    quote_provider_name = config.get('quote_provider', 'zenquotes')
    print(f"Fetching quote using provider: '{quote_provider_name}'...")
    
    start_t = time.time()
    quote_provider = get_quote_provider(config)
    quote = quote_provider.get_quote(profile_content)
    duration = time.time() - start_t
    
    print(f"Quote fetched in {duration:.2f}s")
    print(f"Quote: {quote}")

    # 2. Get Image
    image_provider_name = config.get('image_provider', 'pollinations')
    print(f"Fetching background using provider: '{image_provider_name}'...")
    
    start_t = time.time()
    image_provider = get_image_provider(config)
    # Try to generate a dynamic image prompt if possible
    prompt = "motivational abstract nature landscape technology calm powerful" # Default
    
    if hasattr(quote_provider, 'get_image_prompt'):
        print("Generating custom image prompt via LLM...")
        try:
            dynamic_prompt = quote_provider.get_image_prompt(quote, profile_content)
            print(f"Generated Image Prompt: {dynamic_prompt}")
            prompt = dynamic_prompt
        except Exception as e:
            print(f"Failed to generate dynamic prompt, using default. Error: {e}") 
    
    width = config.get('resolution', {}).get('width', 1920)
    height = config.get('resolution', {}).get('height', 1080)
    
    bg_path = image_provider.get_image(prompt, width, height)
    duration = time.time() - start_t
    print(f"Image fetched in {duration:.2f}s")

    if not bg_path:
        print("Failed to get image.")
        return

    # 3. Render
    print("Rendering...")
    
    font_size = config.get('font_size', 60)
    renderer = WallpaperRenderer(font_size=font_size)
    
    output_path = os.path.join(os.path.expanduser("~/.cache/gen-wal"), "current_wallpaper.jpg")
    
    position = config.get('text_position', 'center')
    padding = config.get('text_padding', 100)
    
    final_path = renderer.compose(bg_path, quote, output_path, position=position, padding=padding, target_size=(width, height))
    
    if final_path:
        # 4. Set Wallpaper
        set_wallpaper(final_path)
    else:
        print("Rendering failed.")

if __name__ == "__main__":
    main()
