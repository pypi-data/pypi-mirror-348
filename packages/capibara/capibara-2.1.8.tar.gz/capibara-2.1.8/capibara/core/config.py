"""
Módulo de configuración para CapibaraGPT.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Any
import yaml 
from pathlib import Path
import jax.numpy as jnp
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Tipos específicos para YAML
YAMLDict = Dict[str, Any]
YAMLList = List[Any]

def get_env_or_default(key: str, default: Any) -> Any:
    """Obtiene valor de variable de entorno o valor por defecto."""
    return os.getenv(f'CAPIBARA_{key}', default)

@dataclass
class GCConfig:
    """Configuración de Gradient Centralization."""
    enabled: bool = field(default_factory=lambda: get_env_or_default('GC_ENABLED', True))
    apply_every: int = field(default_factory=lambda: int(get_env_or_default('GC_APPLY_EVERY', 4)))
    layer_specific: Dict[str, bool] = field(default_factory=dict)

@dataclass
class TrainingConfig:
    """Configuración de entrenamiento."""
    batch_size: int = field(default_factory=lambda: int(get_env_or_default('BATCH_SIZE', 32)))
    seq_length: int = field(default_factory=lambda: int(get_env_or_default('SEQ_LENGTH', 512)))
    learning_rate: float = field(default_factory=lambda: float(get_env_or_default('LEARNING_RATE', 1e-4)))
    num_epochs: int = field(default_factory=lambda: int(get_env_or_default('NUM_EPOCHS', 3)))
    warmup_steps: int = field(default_factory=lambda: int(get_env_or_default('WARMUP_STEPS', 1000)))
    weight_decay: float = field(default_factory=lambda: float(get_env_or_default('WEIGHT_DECAY', 0.01)))
    gradient_clip_norm: float = field(default_factory=lambda: float(get_env_or_default('GRADIENT_CLIP_NORM', 1.0)))
    vocab_size: int = field(default_factory=lambda: int(get_env_or_default('VOCAB_SIZE', 32000)))
    hidden_size: int = field(default_factory=lambda: int(get_env_or_default('HIDDEN_SIZE', 768)))
    num_heads: int = field(default_factory=lambda: int(get_env_or_default('NUM_HEADS', 12)))
    num_layers: int = field(default_factory=lambda: int(get_env_or_default('NUM_LAYERS', 12)))
    gradient_clip_method: str = field(default_factory=lambda: get_env_or_default('GRADIENT_CLIP_METHOD', 'global_norm'))
    gradient_clip_adaptive_threshold: float = field(default_factory=lambda: float(get_env_or_default('GRADIENT_CLIP_ADAPTIVE_THRESHOLD', 0.1)))
    gradient_clip_per_layer_norm: Dict[str, float] = field(default_factory=dict)
    precision: str = field(default_factory=lambda: get_env_or_default('PRECISION', 'bfloat16'))
    mixed_precision: bool = field(default_factory=lambda: get_env_or_default('MIXED_PRECISION', 'True').lower() == 'true')
    profiling: bool = field(default_factory=lambda: get_env_or_default('PROFILING', 'False').lower() == 'true')
    profile_dir: str = field(default_factory=lambda: get_env_or_default('PROFILE_DIR', './profile'))
    checkpoint_dir: str = field(default_factory=lambda: get_env_or_default('CHECKPOINT_DIR', './checkpoints'))
    checkpoint_every: int = field(default_factory=lambda: int(get_env_or_default('CHECKPOINT_EVERY', 1000)))
    best_model_dir: str = field(default_factory=lambda: get_env_or_default('BEST_MODEL_DIR', './best_model'))
    early_stopping_patience: int = field(default_factory=lambda: int(get_env_or_default('EARLY_STOPPING_PATIENCE', 5)))
    early_stopping_min_delta: float = field(default_factory=lambda: float(get_env_or_default('EARLY_STOPPING_MIN_DELTA', 0.0)))

@dataclass
class DistributedConfig:
    """Configuración distribuida."""
    num_devices: int = field(default_factory=lambda: int(get_env_or_default('NUM_DEVICES', 1)))
    model_parallel_size: int = field(default_factory=lambda: int(get_env_or_default('MODEL_PARALLEL_SIZE', 1)))
    data_parallel_size: Optional[int] = field(default_factory=lambda: int(get_env_or_default('DATA_PARALLEL_SIZE', 1)) if get_env_or_default('DATA_PARALLEL_SIZE', None) else None)
    sharding_strategy: str = field(default_factory=lambda: get_env_or_default('SHARDING_STRATEGY', 'auto'))
    sync_every: int = field(default_factory=lambda: int(get_env_or_default('SYNC_EVERY', 1)))

@dataclass
class ValidationConfig:
    """Configuración de validación."""
    val_batch_size: int = field(default_factory=lambda: int(get_env_or_default('VAL_BATCH_SIZE', 32)))
    val_seq_length: int = field(default_factory=lambda: int(get_env_or_default('VAL_SEQ_LENGTH', 512)))
    eval_every: int = field(default_factory=lambda: int(get_env_or_default('EVAL_EVERY', 1000)))
    eval_steps: int = field(default_factory=lambda: int(get_env_or_default('EVAL_STEPS', 100)))
    metrics: List[str] = field(default_factory=lambda: get_env_or_default('METRICS', 'loss,perplexity').split(','))

@dataclass
class LoggingConfig:
    """Configuración de logging."""
    use_wandb: bool = field(default_factory=lambda: get_env_or_default('USE_WANDB', 'True').lower() == 'true')
    wandb_project: str = field(default_factory=lambda: get_env_or_default('WANDB_PROJECT', 'capibara-gpt'))
    wandb_entity: Optional[str] = field(default_factory=lambda: get_env_or_default('WANDB_ENTITY', None))
    log_dir: str = field(default_factory=lambda: get_env_or_default('LOG_DIR', './logs'))
    log_every: int = field(default_factory=lambda: int(get_env_or_default('LOG_EVERY', 100)))

@dataclass
class Config:
    """Configuración principal."""
    training: TrainingConfig = field(default_factory=TrainingConfig)
    distributed: DistributedConfig = field(default_factory=DistributedConfig)
    validation: ValidationConfig = field(default_factory=ValidationConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    gc: GCConfig = field(default_factory=GCConfig)
    
    @property
    def experiment_name(self) -> str:
        """Genera un nombre único para el experimento basado en la configuración."""
        return f"{self.logging.wandb_project}-bs{self.training.batch_size}-lr{self.training.learning_rate}"
    
    @classmethod
    def from_yaml(cls, path: Union[str, Path]) -> 'Config':
        """Carga configuración desde archivo YAML."""
        with open(path, 'r', encoding='utf-8') as f:
            config_dict: YAMLDict = yaml.safe_load(f)
        
        return cls(
            training=TrainingConfig(**config_dict['training']),
            distributed=DistributedConfig(**config_dict['distributed']),
            validation=ValidationConfig(**config_dict['validation']),
            logging=LoggingConfig(**config_dict['logging']),
            gc=GCConfig(**config_dict.get('gc', {}))
        )
    
    def to_yaml(self, path: Union[str, Path]) -> None:
        """Guarda configuración en archivo YAML."""
        config_dict: YAMLDict = {
            'training': self.training.__dict__,
            'distributed': self.distributed.__dict__,
            'validation': self.validation.__dict__,
            'logging': self.logging.__dict__,
            'gc': self.gc.__dict__
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(config_dict, f, default_flow_style=False)
    
    def get_precision_dtype(self) -> jnp.dtype:
        """Obtiene el tipo de datos de precisión."""
        precision_map = {
            'float32': jnp.float32,
            'bfloat16': jnp.bfloat16,
            'float16': jnp.float16
        }
        return precision_map[self.training.precision]

def get_default_config() -> Config:
    """Retorna una configuración por defecto para pruebas."""
    return Config()
