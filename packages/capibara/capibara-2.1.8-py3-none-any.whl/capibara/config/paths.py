"""
Configuración de rutas para el proyecto Capibara.
"""

import os
from pathlib import Path

# Obtener la ruta raíz del proyecto
def get_project_root() -> Path:
    """Obtiene la ruta raíz del proyecto."""
    # Primero intenta obtener la ruta desde la variable de entorno
    if 'CAPIBARA_ROOT' in os.environ:
        return Path(os.environ['CAPIBARA_ROOT'])
    
    # Si no está definida, usa la ruta relativa al módulo actual
    return Path(__file__).parent.parent

# Definir rutas importantes del proyecto
PROJECT_ROOT = get_project_root()
CONFIG_DIR = PROJECT_ROOT / 'config'
DATA_DIR = PROJECT_ROOT / 'data'
MODELS_DIR = PROJECT_ROOT / 'models'
LOGS_DIR = PROJECT_ROOT / 'logs'
CACHE_DIR = PROJECT_ROOT / 'cache'

# Crear directorios si no existen
for directory in [CONFIG_DIR, DATA_DIR, MODELS_DIR, LOGS_DIR, CACHE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Configurar rutas para diferentes entornos
def get_model_path(model_name: str) -> Path:
    """Obtiene la ruta para un modelo específico."""
    return MODELS_DIR / model_name

def get_data_path(data_name: str) -> Path:
    """Obtiene la ruta para un conjunto de datos específico."""
    return DATA_DIR / data_name

def get_config_path(config_name: str) -> Path:
    """Obtiene la ruta para un archivo de configuración específico."""
    return CONFIG_DIR / config_name 