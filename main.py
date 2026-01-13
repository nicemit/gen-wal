import os
import time
import argparse
from src.renderer import WallpaperRenderer
from src.utils import load_config, set_wallpaper
from src.factory import (
    get_profile_provider, 
    get_quote_provider, 
    get_image_provider, 
    get_text_provider
)

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
    
    # Generate dynamic image prompt if configured
    prompt = "motivational abstract nature landscape technology calm powerful" 
    
    img_prompt_provider_name = config.get('image_prompt_provider')
    if img_prompt_provider_name:
        print(f"Generating custom image prompt using '{img_prompt_provider_name}'...")
        try:
            text_provider = get_text_provider(config, img_prompt_provider_name)
            if text_provider:
                prompt_instruction = f"""
                Generate a concise visual description for an image to accompany this motivational quote. 
                Focus on abstract, nature, or technological themes. No text in the image. 
                Max 15 words.
                
                QUOTE: {quote}
                PROFILE: {profile_content}
                """
                dynamic_prompt = text_provider.generate_text(prompt_instruction, system_prompt="You are a creative director.")
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
