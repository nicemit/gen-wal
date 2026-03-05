import hashlib
from datetime import date

def generate_daily_seed(theme_name: str, config_seed) -> int:
    """
    Returns a deterministic integer seed.
    If config_seed is 'auto', derives the seed from the current date and theme.
    Otherwise, parses config_seed as an int.
    """
    if str(config_seed).lower() == 'auto':
        seed_str = f"{date.today().isoformat()}-{theme_name}"
        return int(hashlib.sha1(seed_str.encode()).hexdigest(), 16)
        
    if str(config_seed).lower() == 'random':
        import random
        return random.randint(1, 10**16)
        
    try:
        return int(config_seed)
    except ValueError:
        # Fallback to auto if weird invalid seed
        seed_str = f"{date.today().isoformat()}-{theme_name}"
        return int(hashlib.sha1(seed_str.encode()).hexdigest(), 16)

def get_seed_info(theme_name: str, config_seed):
    """Used for CLI display purposes."""
    seed = generate_daily_seed(theme_name, config_seed)
    
    if str(config_seed).lower() == 'auto':
        derived_from = f"{date.today().isoformat()} + {theme_name}"
        return {"seed": seed, "derived": derived_from}
    elif str(config_seed).lower() == 'random':
        return {"seed": seed, "derived": "Pseudo-Random Number Generator (PRNG)"}
    else:
        return {"seed": seed, "derived": "config.json (explicit)"}

def derive_seed(base_seed: int, label: str) -> int:
    """Split a base seed deterministically into child seeds by combining with a label."""
    s = f"{base_seed}-{label}"
    return int(hashlib.sha1(s.encode()).hexdigest(), 16)
