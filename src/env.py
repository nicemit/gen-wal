import datetime
import subprocess

def get_system_theme() -> str:
    """Attempts to determine if the OS is in dark or light mode."""
    try:
        # Check GNOME / GTK settings
        result = subprocess.run(
            ['gsettings', 'get', 'org.gnome.desktop.interface', 'color-scheme'],
            capture_output=True,
            text=True,
            timeout=1
        )
        if 'prefer-dark' in result.stdout:
            return 'dark'
        elif 'default' in result.stdout:
            return 'light'
    except Exception:
        pass
    
    # Check KDE/Plasma placeholder
    # Fallback default
    return 'dark'

def collect_env_signals() -> dict:
    """Returns a dictionary of current environment context."""
    now = datetime.datetime.now()
    
    return {
        "time_of_day": "morning" if 5 <= now.hour < 12 else "afternoon" if 12 <= now.hour < 18 else "evening" if 18 <= now.hour < 22 else "night",
        "weekday": now.strftime("%A").lower(),
        "day_of_year": now.timetuple().tm_yday,
        "system_theme": get_system_theme()
    }
