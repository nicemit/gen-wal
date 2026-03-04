from .minimal import MinimalLayout
from .centered import CenteredLayout

_LAYOUTS = {
    MinimalLayout.name(): MinimalLayout,
    CenteredLayout.name(): CenteredLayout
}

def get_layout(name: str, config: dict):
    if name not in _LAYOUTS:
        print(f"Warning: Layout '{name}' not found. Falling back to 'minimal'.")
        name = 'minimal'
        
    layout_class = _LAYOUTS[name]
    return layout_class(config.get(name, {}))
