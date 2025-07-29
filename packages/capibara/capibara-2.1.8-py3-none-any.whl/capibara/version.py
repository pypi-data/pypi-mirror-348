"""
Módulo de versión para CapibaraGPT.
"""

__version__ = "2.1.8"
__version_info__ = tuple(int(x) for x in __version__.split("."))

def get_version():
    """Retorna la versión actual del paquete."""
    return __version__

def get_version_info():
    """Retorna la información de versión como una tupla."""
    return __version_info__ 