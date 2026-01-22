import os
import time
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from src.renderer import WallpaperRenderer
from src.utils import load_config, set_wallpaper
from src.factory import (
    get_profile_provider, 
    get_quote_provider, 
    get_image_provider, 
    get_text_provider
)

console = Console()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    parser.add_argument("--profile", help="Override profile path")
    parser.add_argument("--text-pos", help="Override text position (e.g. center, bottom_right)")
    parser.add_argument("--font-size", type=int, help="Override font size")
    args = parser.parse_args()

    # Load Config
    config_path = os.path.join(os.path.dirname(__file__), args.config)
    config = load_config(config_path)
    
    # Override Profile if argument provided
    if args.profile:
        config['profile_path'] = args.profile

    # Override Text Position if argument provided
    if args.text_pos:
        config['text_position'] = args.text_pos
    
    if args.font_size:
        config['font_size'] = args.font_size

    # 1. Load Profile (First, to get metadata for the summary)
    profile_content = ""
    smart_prompts_active = False
    
    with console.status("[bold green]Loading profile...[/bold green]"):
        profile_provider = get_profile_provider(config)
        profile_data = profile_provider.get_profile()
        
        # Handle ProfileData
        if hasattr(profile_data, 'metadata'):
            profile_content = profile_data.content
            metadata = profile_data.metadata

            # Apply Frontmatter Overrides
            if 'quote_prompt_template' in metadata:
                 if 'prompts' not in config: config['prompts'] = {}
                 config['prompts']['quote'] = metadata['quote_prompt_template']
                 smart_prompts_active = True

            if 'image_prompt_template' in metadata:
                 if 'prompts' not in config: config['prompts'] = {}
                 config['prompts']['image_description'] = metadata['image_prompt_template']
                 smart_prompts_active = True
        else:
            profile_content = str(profile_data)

    # 2. Display Info Table
    quote_provider_name = config.get('quote_provider', 'zenquotes')
    image_provider_name = config.get('image_provider', 'pollinations')
    
    # Extract Model Names
    quote_model = "Unknown"
    if "pollinations" in quote_provider_name:
         quote_model = config.get('pollinations', {}).get('text', {}).get('model', 'openai')
    elif "llm" in quote_provider_name:
         parts = quote_provider_name.split(':')
         sub = parts[1] if len(parts) > 1 else 'ollama'
         quote_model = config.get('llm', {}).get(sub, {}).get('model', 'unknown')

    image_model = "Unknown"
    if "pollinations" in image_provider_name:
         image_model = config.get('pollinations', {}).get('image', {}).get('model', 'flux')
    
    # Build Table
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column(justify="right")
    
    profile_name = os.path.basename(config.get('profile_path', 'default'))
    res = config.get('resolution', {})
    res_str = f"{res.get('width')}x{res.get('height')}"

    grid.add_row(f"[bold blue]Gen-Wal[/bold blue] v1.0", f"[dim]Profile:[/dim] [cyan]{profile_name}[/cyan]")
    grid.add_row(f"[dim]Resolution:[/dim] {res_str}", f"[dim]Smart Prompts:[/dim] " + ("[bold green]Active 🧠[/bold green]" if smart_prompts_active else "[dim]None[/dim]"))
    grid.add_row(f"[dim]Quote Provider:[/dim] {quote_provider_name}", f"[dim]Model:[/dim] {quote_model}")
    grid.add_row(f"[dim]Image Provider:[/dim] {image_provider_name}", f"[dim]Model:[/dim] {image_model}")
    
    console.print(Panel(grid, title="[bold]Environment designs the mind[/bold]", border_style="blue", padding=(1, 2)))

    # 3. Execution
    start_total = time.time()
    
    # Get Quote
    quote = ""
    with console.status(f"[bold green]Fetching quote...[/bold green]"):
        start_t = time.time()
        quote_provider = get_quote_provider(config)
        quote = quote_provider.get_quote(profile_content)
        dur_q = time.time() - start_t
    
    console.print(f"📄 [bold]Quote[/bold]           [dim]({dur_q:.1f}s)[/dim]: [italic]\"{quote}\"[/italic]")

    # Get Image Prompt
    img_prompt_provider_name = config.get('image_prompt_provider')
    prompt = "motivational abstract nature landscape technology calm powerful"
    
    if img_prompt_provider_name:
        with console.status(f"[bold purple]Generating visual description...[/bold purple]"):
            try:
                text_provider = get_text_provider(config, img_prompt_provider_name)
                if text_provider:
                    prompt_instruction = config.get('prompts', {}).get('image_description')
                    
                    if not prompt_instruction:
                        prompt_instruction = f"Generate a concise visual description... QUOTE: {quote}"
                    else:
                        prompt_instruction = prompt_instruction.format(quote=quote, profile_content=profile_content)
                        
                    dynamic_prompt = text_provider.generate_text(prompt_instruction, system_prompt="You are a creative director.")
                    prompt = dynamic_prompt
                    console.print(f"🎨 [bold]Visual Prompt[/bold]: [dim]{prompt}[/dim]")
            except Exception as e:
                 console.print(f"[red]Failed to generate dynamic prompt, using default.[/red] [dim]{e}[/dim]")

    # Get Image
    bg_path = ""
    with console.status(f"[bold green]Generating wallpaper...[/bold green]"):
        start_t = time.time()
        image_provider = get_image_provider(config)
        width = config.get('resolution', {}).get('width', 1920)
        height = config.get('resolution', {}).get('height', 1080)
        bg_path = image_provider.get_image(prompt, width, height)
        dur_i = time.time() - start_t

    if not bg_path:
        console.print("[bold red]Failed to get image.[/bold red]")
        return
        
    console.print(f"🖼️  [bold]Image[/bold]           [dim]({dur_i:.1f}s)[/dim]: [link={bg_path}]{os.path.basename(bg_path)}[/link]")

    # Render & Save
    with console.status("[bold green]Composing final image...[/bold green]"):
        font_size = config.get('font_size', 60)
        renderer = WallpaperRenderer(font_size=font_size)
        
        # Output Path Logic
        wallpaper_settings = config.get('wallpaper_settings', {})
        custom_path = wallpaper_settings.get('save_path')
        
        if custom_path:
             output_path = os.path.expanduser(custom_path)
             if not os.path.splitext(output_path)[1]: # Is Dir
                 from datetime import datetime
                 import re
                 
                 timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                 
                 # Clean Profile Name
                 profile_clean = os.path.splitext(os.path.basename(config.get('profile_path', 'default')))[0]
                 
                 # Clean Model Name
                 model_clean = re.sub(r'[^a-zA-Z0-9]', '', image_model)
                 
                 filename = f"{timestamp}_{profile_clean}_{model_clean}.jpg"
                 os.makedirs(output_path, exist_ok=True)
                 output_path = os.path.join(output_path, filename)
             else:
                 os.makedirs(os.path.dirname(output_path), exist_ok=True)
        else:
             output_path = os.path.join(os.path.expanduser("~/.cache/gen-wal"), "current_wallpaper.jpg")
        
        position = config.get('text_position', 'center')
        padding = config.get('text_padding', 100)
        
        # Watermark Setup
        watermark_config = config.get('watermark', {})
        if watermark_config.get('enabled', True): # Default to true if not specified but logic passed
            # Clean Profile Name for display
            display_name = os.path.splitext(os.path.basename(config.get('profile_path', 'Gen-Wal')))[0]
            display_name = display_name.replace('_profile', '').replace('_', ' ').title()
            
            # Allow config to override text, otherwise use profile name
            if 'text' not in watermark_config:
                watermark_config['text'] = display_name
                
        final_path = renderer.compose(bg_path, quote, output_path, position=position, padding=padding, target_size=(width, height), watermark_config=watermark_config)
    
    if final_path:
        console.print(f"💾 [bold]Saved to[/bold]        : [link={final_path}]{final_path}[/link]")
        
        should_apply = wallpaper_settings.get('apply_wallpaper', True)
        
        if should_apply:
            try:
                set_wallpaper(final_path)
                console.print(f"[bold green]✨ Desktop Updated Successfully![/bold green]")
            except:
                pass # Error printed by util
        else:
            console.print(f"[yellow]Skipping application (config).[/yellow]")
    else:
        console.print("[bold red]Rendering failed.[/bold red]")

if __name__ == "__main__":
    main()
