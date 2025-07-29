"""
Capibara - Un modelo de lenguaje basado en SSM (State Space Models)

Este paquete proporciona una implementación de un modelo de lenguaje basado en SSM,
optimizado para TPU y GPU, con soporte para entrenamiento distribuido y fine-tuning.
"""

from capibara.core.model import DynamicCapibaraModel
from capibara.core.config import Config
from capibara.core.optimizer import OptimizerType
from capibara.core.tokenizer import AutoTokenizer
from capibara.interfaces import isub_modelsModel, ILayerLayer, ContentFilter
from capibara.utils.logging import setup_logging
from capibara.utils.system_info import SystemMonitor
from capibara.utils.monitoring import RealTimeMonitor, ResourceMonitor
from capibara.utils.checkpointing import CheckpointManager
from typing import List

__version__ = "2.1.7"
__all__: List[str] = [
    'DynamicCapibaraModel',
    'ModelConfig',
    'OptimizerType',
    'AutoTokenizer',
    'BaseModel',
    'BaseLayer',
    'ContentFilter',
    'setup_logging',
    'SystemMonitor',
    'RealTimeMonitor',
    'ResourceMonitor',
    'CheckpointManager'
]

# Indicar que el paquete tiene tipos
__py_typed__ = True
