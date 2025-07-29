from typing import Any, Dict, Optional
import tomli
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.configs: Dict[str, Dict[str, Any]] = {}
        
    def load_config(self, name: str) -> Dict[str, Any]:
        """Carga una configuración desde un archivo TOML."""
        try:
            config_path = self.config_dir / f"{name}.toml"
            with open(config_path, "rb") as f:
                config = tomli.load(f)
            self.configs[name] = config
            logger.info(f"Configuración {name} cargada exitosamente")
            return config
        except Exception as e:
            logger.error(f"Error al cargar configuración {name}: {str(e)}")
            raise
            
    def get_config(self, name: str) -> Optional[Dict[str, Any]]:
        """Obtiene una configuración cargada."""
        return self.configs.get(name)
        
    def get_value(self, config_name: str, key_path: str, default: Any = None) -> Any:
        """Obtiene un valor específico de una configuración."""
        config = self.get_config(config_name)
        if not config:
            return default
            
        try:
            value = config
            for key in key_path.split("."):
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
            
    def reload_all(self) -> None:
        """Recarga todas las configuraciones."""
        for name in self.configs:
            self.load_config(name)
            
    def validate_config(self, name: str, schema: Dict[str, Any]) -> bool:
        """Valida una configuración contra un esquema."""
        config = self.get_config(name)
        if not config:
            return False
            
        try:
            self._validate_schema(config, schema)
            return True
        except ValueError as e:
            logger.error(f"Error de validación en {name}: {str(e)}")
            return False
            
    def _validate_schema(self, config: Dict[str, Any], schema: Dict[str, Any]) -> None:
        """Valida recursivamente un esquema de configuración."""
        for key, expected_type in schema.items():
            if key not in config:
                raise ValueError(f"Falta clave requerida: {key}")
                
            if isinstance(expected_type, dict):
                if not isinstance(config[key], dict):
                    raise ValueError(f"Tipo incorrecto para {key}")
                self._validate_schema(config[key], expected_type)
            elif not isinstance(config[key], expected_type):
                raise ValueError(f"Tipo incorrecto para {key}") 