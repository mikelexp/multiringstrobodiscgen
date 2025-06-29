import sys
import json
import locale
from pathlib import Path


class ConfigManager:
    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()
    
    def _get_config_dir(self):
        if sys.platform == "win32":
            config_dir = Path.home() / "AppData" / "Roaming" / "MultiRingStroboDiscGen"
        else:
            config_dir = Path.home() / ".config" / "multiringstrobodiscgen"
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
    
    def _load_config(self):
        default_config = {
            "language": self._detect_language()
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Ensure all default keys exist
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except (json.JSONDecodeError, OSError):
                pass
        
        return default_config
    
    def _detect_language(self):
        try:
            system_locale = locale.getdefaultlocale()[0]
            if system_locale and system_locale.startswith('es'):
                return 'es'
        except:
            pass
        return 'en'
    
    def save_config(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except OSError:
            pass
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self.save_config()