import os
import yaml
import subprocess
from src.config import THEMES_DIR, update_config

# Default themes shipped with the repo
DEFAULT_THEMES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'themes')

def ensure_theme_dir():
    os.makedirs(THEMES_DIR, exist_ok=True)

def _get_all_theme_files():
    """Returns a dict mapping theme_name -> absolute_path. 
    User themes in ~/.local/share/genwal/themes/ override default themes."""
    themes = {}
    
    # Load defaults first
    if os.path.exists(DEFAULT_THEMES_DIR):
        for f in os.listdir(DEFAULT_THEMES_DIR):
            if f.endswith('.md'):
                name = os.path.splitext(f)[0]
                themes[name] = os.path.join(DEFAULT_THEMES_DIR, f)
                
    # User themes override
    if os.path.exists(THEMES_DIR):
        for f in os.listdir(THEMES_DIR):
            if f.endswith('.md'):
                name = os.path.splitext(f)[0]
                themes[name] = os.path.join(THEMES_DIR, f)
                
    return themes

def list_themes():
    themes = _get_all_theme_files()
    if not themes:
        print("No themes found.")
        return []
    
    print("Available Themes:")
    for name in sorted(themes.keys()):
        print(f"  - {name}")
    return list(themes.keys())

def use_theme(name):
    themes = _get_all_theme_files()
    if name not in themes:
        print(f"❌ Theme '{name}' not found.")
        return False
        
    update_config('theme', name)
    print(f"✅ Switched to theme: {name}")
    return True

def edit_theme(name):
    themes = _get_all_theme_files()
    
    # If the theme exists but is a default theme, copy it to the user dir first
    if name in themes:
        path = themes[name]
        if path.startswith(DEFAULT_THEMES_DIR):
            print(f"Copying default theme '{name}' to user directory for editing...")
            user_path = os.path.join(THEMES_DIR, f"{name}.md")
            ensure_theme_dir()
            with open(path, 'r') as src, open(user_path, 'w') as dst:
                dst.write(src.read())
            path = user_path
    else:
        # Create a new theme
        print(f"🆕 Creating new theme: {name}")
        ensure_theme_dir()
        path = os.path.join(THEMES_DIR, f"{name}.md")
        with open(path, 'w') as f:
            f.write("---\nlayout_hint: minimal\npalette_hint: dark\nquote_style: concise\n---\n\nWrite your theme philosophy here.\n")
            
    print(f"📝 Opening theme: {name}")
    editor = os.environ.get('EDITOR', 'nano')
    subprocess.run([editor, path])

def load_theme(name):
    """Loads a theme by name, parses YAML frontmatter and content."""
    themes = _get_all_theme_files()
    if name not in themes:
        raise ValueError(f"Theme '{name}' not found.")
        
    path = themes[name]
    with open(path, 'r') as f:
        content = f.read()
        
    # Naive frontmatter parser
    hints = {}
    body = content
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                hints = yaml.safe_load(parts[1]) or {}
                body = parts[2].strip()
            except yaml.YAMLError as e:
                print(f"Warning: Failed to parse theme frontmatter - {e}")
                
    return hints, body
