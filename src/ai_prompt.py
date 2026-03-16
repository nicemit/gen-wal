def build_prompt(quote: str, palette: dict, theme_hints: dict) -> str:
    """
    Constructs a unified prompt string for AI image generation,
    combining the theme philosophy, color palette, and daily quote.
    """
    style_desc = theme_hints.get("quote_style", "abstract")
    palette_hint = theme_hints.get("palette_hint", "dark")
    layout_hint = theme_hints.get("layout_hint", "minimal")
    
    # Extract hex colors from the palette dictionary safely
    colors = []
    for k in ["background", "primary", "secondary", "accent"]:
        if k in palette and isinstance(palette[k], str) and palette[k].startswith("#"):
            colors.append(palette[k])
            
    color_str = ", ".join(colors) if colors else "system theme colors"

    prompt = (
        f"A {layout_hint} abstract wallpaper background. "
        f"Style: {style_desc}. "
        f"Color palette: {palette_hint} with hex codes ({color_str}). "
        f"The visual tone should reflect the following quote (DO NOT INCLUDE TEXT IN THE IMAGE): '{quote}'. "
        f"Focus on shapes, gradients, and textures without text or words."
    )
    return prompt
