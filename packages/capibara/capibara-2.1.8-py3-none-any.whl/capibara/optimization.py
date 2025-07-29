"""
Módulo de optimización para CapibaraGPT.
Incluye Gradient Centralization, optimizaciones de memoria y profiling.
"""

from typing import Any, Dict, Optional, Tuple, Union, Callable
import jax
import jax.numpy as jnp
from flax import struct
from flax.training import train_state
import optax
import wandb
from tensorboardX import SummaryWriter
import time
from jax.experimental import mesh_utils
from jax.sharding import Mesh, PartitionSpec
import jax.profiler
import logging
from pathlib import Path
import argparse
from .core.config import Config, GCConfig

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@struct.dataclass
class TrainingMetrics:
    """Métricas de entrenamiento extendidas."""
    grad_norm: float = 0.0
    learning_rate: float = 0.0
    val_loss: float = 0.0
    val_perplexity: float = 0.0
    throughput: float = 0.0
    step_time: float = 0.0
    tokens_per_second: float = 0.0

def apply_gc(g: jnp.ndarray, layer_name: Optional[str] = None, gc_config: GCConfig = GCConfig()) -> jnp.ndarray:
    """
    Aplica Gradient Centralization a un tensor.
    
    Args:
        g: Tensor de gradientes
        layer_name: Nombre de la capa (opcional)
        gc_config: Configuración de GC
        
    Returns:
        Tensor centralizado
    """
    if not gc_config.enabled:
        return g
    
    # Validación segura de layer_specific
    if layer_name is not None and layer_name in gc_config.layer_specific:
        if not gc_config.layer_specific[layer_name]:
            return g
    
    return g - jnp.mean(g, axis=tuple(range(1, g.ndim)), keepdims=True) if g.ndim > 1 else g

def create_dummy_batch(config: Config) -> Dict[str, jnp.ndarray]:
    """
    Crea un lote dummy con la precisión correcta.
    
    Args:
        config: Configuración del modelo
        
    Returns:
        Lote dummy con input_ids y attention_mask
    """
    dtype = config.get_precision_dtype()
    return {
        'input_ids': jnp.ones((config.training.batch_size, config.training.seq_length), dtype=dtype),
        'attention_mask': jnp.ones((config.training.batch_size, config.training.seq_length), dtype=dtype),
        'labels': jnp.ones((config.training.batch_size, config.training.seq_length), dtype=dtype)
    }

class EarlyStopping:
    """Early stopping con guardado del mejor modelo."""
    
    def __init__(self, config: Config):
        self.patience = config.training.early_stopping_patience
        self.min_delta = config.training.early_stopping_min_delta
        self.best_model_path = Path(config.training.best_model_dir)
        self.best_loss = float('inf')
        self.counter = 0
        self.best_state: Optional[TrainingState] = None
        
    def __call__(
        self,
        current_loss: float,
        state: TrainingState
    ) -> Tuple[bool, Optional[TrainingState]]:
        """
        Verifica si se debe detener el entrenamiento.
        
        Args:
            current_loss: Pérdida actual
            state: Estado del modelo
            
        Returns:
            Tuple[bool, Optional[TrainingState]]: (debe detenerse, mejor estado)
        """
        if current_loss < self.best_loss - self.min_delta:
            self.best_loss = current_loss
            self.counter = 0
            self.best_state = state
            # Guardar el mejor modelo
            self.best_model_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.best_model_path, 'wb') as f:
                f.write(jax.serialization.to_bytes(state))
            return False, None
        
        self.counter += 1
        if self.counter >= self.patience:
            return True, self.best_state
        
        return False, None

class TrainingState(train_state.TrainState):
    """
    Estado de entrenamiento extendido con métricas y profiling.
    """
    metrics: TrainingMetrics
    val_step_fn: Callable[[TrainingState, Dict[str, jnp.ndarray]], Dict[str, float]] = struct.field(pytree_node=False)
    last_val_step: int = 0
    config: Config = struct.field(pytree_node=False)
    writer: Optional[SummaryWriter] = struct.field(pytree_node=False, default=None)
    
    @classmethod
    def create(
        cls,
        *,
        apply_fn,
        params,
        tx,
        config: Config,
        metrics: Optional[TrainingMetrics] = None,
        writer: Optional[SummaryWriter] = None,
        **kwargs
    ):
        if metrics is None:
            metrics = TrainingMetrics()
        return super().create(
            apply_fn=apply_fn,
            params=params,
            tx=tx,
            config=config,
            metrics=metrics,
            writer=writer,
            **kwargs
        )

def train_step(
    state: TrainingState,
    batch: Dict[str, jnp.ndarray],
    dropout_rng: jax.random.PRNGKey
) -> Tuple[TrainingState, Dict[str, float]]:
    """
    Paso de entrenamiento con Gradient Centralization y profiling.
    
    Args:
        state: Estado de entrenamiento
        batch: Lote de datos
        dropout_rng: Clave aleatoria para dropout
        
    Returns:
        Estado actualizado y métricas
    """
    start_time = time.time()
    
    def loss_fn(params):
        logits = state.apply_fn(
            params,
            batch['input_ids'],
            batch['attention_mask'],
            rngs={'dropout': dropout_rng},
            training=True
        )
        loss = optax.softmax_cross_entropy_with_integer_labels(
            logits, batch['labels']
        ).mean()
        return loss, logits
    
    grad_fn = jax.value_and_grad(loss_fn, has_aux=True)
    (loss, logits), grads = grad_fn(state.params)
    
    # Aplicar Gradient Centralization según configuración
    if state.step % state.config.gc.apply_every == 0:
        grads = jax.tree_util.tree_map_with_path(
            lambda path, g: apply_gc(g, '/'.join(str(p) for p in path), state.config.gc),
            grads
        )
    
    # Aplicar gradient clipping usando optax.global_norm
    grad_norm = optax.global_norm(grads)
    grads = jax.tree_util.tree_map(
        lambda g: jnp.clip(g, -state.config.training.gradient_clip_norm, state.config.training.gradient_clip_norm),
        grads
    )
    
    # Actualizar estado
    state = state.apply_gradients(grads=grads)
    
    # Calcular throughput y tokens/segundo
    step_time = time.time() - start_time
    batch_size = batch['input_ids'].shape[0]
    seq_length = batch['input_ids'].shape[1]
    throughput = (batch_size * seq_length) / step_time
    tokens_per_second = throughput / step_time
    
    # Actualizar métricas
    metrics = {
        'loss': loss,
        'grad_norm': grad_norm,
        'learning_rate': state.opt_state.hyperparams['learning_rate'],
        'throughput': throughput,
        'tokens_per_second': tokens_per_second,
        'step_time': step_time
    }
    
    # Registrar en wandb y tensorboard solo en el proceso principal
    if jax.process_index() == 0:
        if state.config.logging.use_wandb:
            wandb.log(metrics, step=state.step)
        if state.writer is not None:
            for k, v in metrics.items():
                state.writer.add_scalar(f'train/{k}', v, state.step)
    
    return state, metrics

@jax.jit
def val_step(
    state: TrainingState,
    batch: Dict[str, jnp.ndarray]
) -> Dict[str, float]:
    """
    Paso de validación con caching de JIT y float32.
    
    Args:
        state: Estado de entrenamiento
        batch: Lote de datos de validación
        
    Returns:
        Métricas de validación
    """
    # Usar float32 para validación
    with jax.default_matmul_precision('float32'):
        logits = state.apply_fn(
            state.params,
            batch['input_ids'],
            batch['attention_mask'],
            training=False
        )
        loss = optax.softmax_cross_entropy_with_integer_labels(
            logits, batch['labels']
        ).mean()
        
        # Calcular perplexity
        perplexity = jnp.exp(loss)
    
    return {
        'val_loss': loss,
        'val_perplexity': perplexity
    }

def setup_profiling(config: Config) -> None:
    """
    Configura el profiling de JAX.
    
    Args:
        config: Configuración del modelo
    """
    if config.training.profiling:
        jax.profiler.start_trace(config.training.profile_dir)
    
def stop_profiling(config: Config) -> None:
    """
    Detiene el profiling de JAX.
    
    Args:
        config: Configuración del modelo
    """
    if config.training.profiling:
        jax.profiler.stop_trace()

def save_checkpoint(state: TrainingState, step: int) -> None:
    """
    Guarda un checkpoint del modelo.
    
    Args:
        state: Estado del modelo
        step: Paso actual
    """
    if jax.process_index() == 0:
        checkpoint_path = Path(state.config.training.checkpoint_dir) / f'checkpoint_{step}'
        checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        with open(checkpoint_path, 'wb') as f:
            f.write(jax.serialization.to_bytes(state))

def load_checkpoint(config: Config, step: Optional[int] = None) -> Optional[TrainingState]:
    """
    Carga un checkpoint del modelo.
    
    Args:
        config: Configuración del modelo
        step: Paso del checkpoint a cargar (opcional)
        
    Returns:
        Estado del modelo o None si no se encuentra
    """
    checkpoint_dir = Path(config.training.checkpoint_dir)
    if not checkpoint_dir.exists():
        return None
    
    if step is None:
        # Cargar el último checkpoint
        checkpoints = list(checkpoint_dir.glob('checkpoint_*'))
        if not checkpoints:
            return None
        checkpoint_path = max(checkpoints, key=lambda p: int(p.stem.split('_')[1]))
    else:
        checkpoint_path = checkpoint_dir / f'checkpoint_{step}'
    
    if not checkpoint_path.exists():
        return None
    
    with open(checkpoint_path, 'rb') as f:
        return jax.serialization.from_bytes(TrainingState, f.read())

def setup_logging(config: Config) -> Tuple[Optional[SummaryWriter], Optional[wandb.run]]:
    """
    Configura el logging para el entrenamiento.
    
    Args:
        config: Configuración del modelo
        
    Returns:
        Tuple[Optional[SummaryWriter], Optional[wandb.run]]: Writer de TensorBoard y run de WandB
    """
    writer = None
    wandb_run = None
    
    if jax.process_index() == 0:
        if config.logging.use_wandb:
            wandb_run = wandb.init(
                project=config.logging.wandb_project,
                entity=config.logging.wandb_entity,
                config=config.__dict__
            )
        
        writer = SummaryWriter(logdir=config.logging.log_dir)
    
    return writer, wandb_run

def teardown_logging(writer: Optional[SummaryWriter], wandb_run: Optional[wandb.run]) -> None:
    """
    Cierra los recursos de logging.
    
    Args:
        writer: Writer de TensorBoard
        wandb_run: Run de WandB
    """
    if jax.process_index() == 0:
        if writer is not None:
            writer.close()
        if wandb_run is not None:
            wandb_run.finish() 