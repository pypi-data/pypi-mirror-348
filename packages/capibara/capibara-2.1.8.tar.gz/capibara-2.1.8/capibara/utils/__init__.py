"""
Módulo de utilidades para CapibaraGPT.
"""

from .error_handling import handle_error, DataProcessingError, ConfigError
from .data_processing import (
    process_batch,
    load_processed_data,
    save_processed_data,
    text_to_bytes,
    bytes_to_text,
    prepare_training_data
)
from capibara.core.config import Config

__all__ = [
    'handle_error',
    'DataProcessingError',
    'ConfigError',
    'process_batch',
    'load_processed_data',
    'save_processed_data',
    'text_to_bytes',
    'bytes_to_text',
    'prepare_training_data',
    'BaseConfig',
    'load_config'
]
