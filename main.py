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
    args = parser.parse_args()

    # Load Config
    config_path = os.path.join(os.path.dirname(__file__), args.config)
    config = load_config(config_path)

    # 1. Info Table
    quote_provider_name = config.get('quote_provider', 'zenquotes')
    image_provider_name = config.get('image_provider', 'pollinations')
    
    # Extract Model Names (Heuristic based on config structure)
    quote_model = "Unknown"
    if "pollinations" in quote_provider_name:
         quote_model = config.get('pollinations', {}).get('text', {}).get('model', 'openai')
    elif "llm" in quote_provider_name:
         # Simplified lookup logic
         parts = quote_provider_name.split(':')
         sub = parts[1] if len(parts) > 1 else 'ollama'
         quote_model = config.get('llm', {}).get(sub, {}).get('model', 'unknown')

    image_model = "Unknown"
    if "pollinations" in image_provider_name:
         image_model = config.get('pollinations', {}).get('image', {}).get('model', 'flux')
    
    
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column(justify="right")
    grid.add_row(f"[bold blue]Gen-Wal[/bold blue] v1.0", f"[dim]Profile:[/dim] [cyan]{os.path.basename(config.get('profile_path', 'default'))}[/cyan]")
    grid.add_row(f"[dim]Quote Provider:[/dim] {quote_provider_name}", f"[dim]Model:[/dim] {quote_model}")
    grid.add_row(f"[dim]Image Provider:[/dim] {image_provider_name}", f"[dim]Model:[/dim] {image_model}")
    
    console.print(Panel(grid, border_style="blue"))

    # Load Profile
    with console.status("[bold green]Fetching profile...[/bold green]"):
        profile_provider = get_profile_provider(config)
        profile_content = profile_provider.get_profile()

    # 2. Get Quote
    start_t = time.time()
    quote = ""
    with console.status(f"[bold green]Fetching quote...[/bold green]"):
        quote_provider = get_quote_provider(config)
        quote = quote_provider.get_quote(profile_content)
    duration = time.time() - start_t
    
    console.print(f"📄 [bold]Quote[/bold] ([green]{duration:.2f}s[/green]): [italic]\"{quote}\"[/italic]")

    # 3. Get Image
    img_prompt_provider_name = config.get('image_prompt_provider')
    prompt = "motivational abstract nature landscape technology calm powerful"
    
    # Generate dynamic image prompt if configured
    if img_prompt_provider_name:
        with console.status(f"[bold purple]Generating image prompt...[/bold purple]"):
            try:
                text_provider = get_text_provider(config, img_prompt_provider_name)
                if text_provider:
                    prompt_instruction = config.get('prompts', {}).get('image_description')
                    
                    if not prompt_instruction:
                        # Fallback default
                        prompt_instruction = f"Generate a concise visual description... QUOTE: {quote}"
                    else:
                        prompt_instruction = prompt_instruction.format(quote=quote, profile_content=profile_content)
                        
                    dynamic_prompt = text_provider.generate_text(prompt_instruction, system_prompt="You are a creative director.")
                    prompt = dynamic_prompt
                    console.print(f"🎨 [bold]Visual Prompt[/bold]: [dim]{prompt}[/dim]")
            except Exception as e:
                 console.print(f"[red]Failed to generate dynamic prompt, using default.[/red] [dim]{e}[/dim]")

    start_t = time.time()
    bg_path = ""
    with console.status(f"[bold green]Generating wallpaper...[/bold green]"):
        image_provider = get_image_provider(config)
        width = config.get('resolution', {}).get('width', 1920)
        height = config.get('resolution', {}).get('height', 1080)
        bg_path = image_provider.get_image(prompt, width, height)
    duration = time.time() - start_t

    if not bg_path:
        console.print("[bold red]Failed to get image.[/bold red]")
        return
        
    console.print(f"🖼️ [bold]Image[/bold] ([green]{duration:.2f}s[/green]): [link={bg_path}]{bg_path}[/link]")

    # 4. Render
    with console.status("[bold green]Composing wallpaper...[/bold green]"):
        font_size = config.get('font_size', 60)
        renderer = WallpaperRenderer(font_size=font_size)
        
        output_path = os.path.join(os.path.expanduser("~/.cache/gen-wal"), "current_wallpaper.jpg")
        
        position = config.get('text_position', 'center')
        padding = config.get('text_padding', 100)
        
        final_path = renderer.compose(bg_path, quote, output_path, position=position, padding=padding, target_size=(width, height))
    
    if final_path:
        set_wallpaper(final_path)
        console.print(f"[bold green]✨ Wallpaper updated successfully![/bold green]")
    else:
        console.print("[bold red]Rendering failed.[/bold red]")

if __name__ == "__main__":
    main()
