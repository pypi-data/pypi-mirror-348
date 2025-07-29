"""Módulo de entrenamiento y evaluación para CapibaraModel."""

import jax # type: ignore
import jax.numpy as jnp # type: ignore
import optax # type: ignore
from flax import linen as nn # type: ignore
from typing import Dict, Any, Optional, Tuple # type: ignore
import logging # type: ignore
from ..core.config import CapibaraConfig # type: ignore
from ..core.interfaces.isub_models import ISubModel # type: ignore
from ..utils.monitoring import ResourceMonitor # type: ignore
from ..optimization import TrainingState, TrainingMetrics, setup_logging, teardown_logging, apply_gc
from tensorboardX import SummaryWriter
import wandb
import time
from pathlib import Path

logger = logging.getLogger(__name__)

class CapibaraTrainer(nn.Module):
    """Entrenador para el modelo Capibara con soporte para submodelos y pensamiento dual."""
    
    config: CapibaraConfig
    submodels: Dict[str, ISubModel]
    hidden_size: int
    use_context: bool = False
    writer: Optional[SummaryWriter] = None
    wandb_run: Optional[wandb.run] = None
    
    def setup(self):
        """Inicializa el entrenador."""
        self.dropout = nn.Dropout(rate=self.config.dropout_rate)
        self.fusion = nn.Dense(self.hidden_size)
        self.attention = nn.SelfAttention(num_heads=8)
        
        # Adaptadores de dimensión
        self.adapters = {
            name: nn.Dense(self.hidden_size)
            for name in self.submodels.keys()
        }
        
        # Optimizador adaptativo con Gradient Centralization
        self.optimizer = optax.chain(
            optax.clip_by_global_norm(1.0),
            optax.adamw(
                learning_rate=self.config.learning_rate,
                weight_decay=self.config.weight_decay
            )
        )
        
        # Monitor de recursos
        self.resource_monitor = ResourceMonitor(self.config)
        
        # Setup de logging
        self.writer, self.wandb_run = setup_logging(self.config)
    
    def __del__(self):
        """Limpieza de recursos al destruir el trainer."""
        teardown_logging(self.writer, self.wandb_run)
    
    def _preprocess_input(self, x: jnp.ndarray) -> jnp.ndarray:
        """Preprocesa la entrada para asegurar formato 3D."""
        if x.ndim == 2:
            return x[None, :, :]  # Agrega dimensión de batch
        return x
        
    def _adapt_dimensions(self, x: jnp.ndarray, target_size: int, name: str) -> jnp.ndarray:
        """Adapta las dimensiones del tensor al tamaño objetivo."""
        if x.shape[-1] != target_size:
            return self.adapters[name](x)
        return x
        
    def _process_submodel_output(
        self,
        name: str,
        result: Any,
        context: Optional[jnp.ndarray] = None
    ) -> Tuple[jnp.ndarray, Dict[str, Any]]:
        """Procesa la salida de un submodelo según su tipo."""
        metrics = {}
        
        if isinstance(result, tuple):
            # Submodelos con estado
            output, state = result
            metrics[f"{name}_state"] = state
        elif isinstance(result, dict):
            # Submodelos con métricas
            output = result.get("output", result)
            metrics.update(result.get("metrics", {}))
        else:
            # Salida directa
            output = result
            
        # Adaptar dimensiones si es necesario
        output = self._adapt_dimensions(output, self.hidden_size, name)
        
        return output, metrics
        
    def apply_gradient_clipping(self, grads, config):
        """Aplica diferentes estrategias de gradient clipping según la configuración."""
        method = config.training.gradient_clip_method
        norm = config.training.gradient_clip_norm
        
        if method == 'global_norm':
            return optax.clip_by_global_norm(grads, norm)
        
        elif method == 'value':
            return jax.tree_map(
                lambda g: jnp.clip(g, -norm, norm),
                grads
            )
        
        elif method == 'adaptive':
            # Clipping adaptativo basado en la norma actual
            current_norm = optax.global_norm(grads)
            if current_norm > config.training.gradient_clip_adaptive_threshold:
                scale = config.training.gradient_clip_adaptive_threshold / current_norm
                return jax.tree_map(lambda g: g * scale, grads)
            return grads
        
        elif method == 'layer_norm':
            # Clipping por norma de capa
            def clip_layer(path, g):
                layer_name = '/'.join(str(p) for p in path)
                layer_norm = optax.global_norm([g])
                if layer_norm > norm:
                    scale = norm / layer_norm
                    return g * scale
                return g
            return jax.tree_util.tree_map_with_path(clip_layer, grads)
        
        elif method == 'per_layer':
            # Clipping con normas específicas por capa
            def clip_per_layer(path, g):
                layer_name = '/'.join(str(p) for p in path)
                layer_norm = config.training.gradient_clip_per_layer_norm.get(layer_name, norm)
                current_norm = optax.global_norm([g])
                if current_norm > layer_norm:
                    scale = layer_norm / current_norm
                    return g * scale
                return g
            return jax.tree_util.tree_map_with_path(clip_per_layer, grads)
        
        else:
            return grads

    def train_step(
        self,
        state: TrainingState,
        batch: Dict[str, jnp.ndarray],
        dropout_rng: jax.random.PRNGKey
    ) -> Tuple[TrainingState, Dict[str, jnp.ndarray]]:
        """Paso de entrenamiento con pérdida adaptativa y Gradient Centralization."""
        start_time = time.time()
        
        def loss_fn(params):
            # Forward pass
            outputs = self.apply(
                params,
                batch["input"],
                rngs={'dropout': dropout_rng},
                training=True
            )
            
            # Cálculo de pérdidas
            base_loss = jnp.mean((outputs["output"] - batch["target"]) ** 2)
            dual_loss = jnp.mean((outputs["metrics"]["dual_process_importance"] - 0.5) ** 2)
            
            # Pérdida total
            total_loss = base_loss + 0.1 * dual_loss
            
            return total_loss, outputs["metrics"]
        
        # Cálculo de gradientes y actualización
        grad_fn = jax.value_and_grad(loss_fn, has_aux=True)
        (loss, metrics), grads = grad_fn(state.params)
        
        # Aplicar Gradient Clipping
        grads = self.apply_gradient_clipping(grads, self.config)
        
        # Aplicar Gradient Centralization
        if state.step % self.config.gc.apply_every == 0:
            grads = jax.tree_util.tree_map_with_path(
                lambda path, g: apply_gc(g, '/'.join(str(p) for p in path), self.config.gc),
                grads
            )
        
        # Calcular norma de gradientes usando optax.global_norm
        grad_norm = optax.global_norm(grads)
        
        # Actualizar estado
        state = state.apply_gradients(grads=grads)
        
        # Calcular throughput y tokens/segundo
        step_time = time.time() - start_time
        batch_size = batch["input"].shape[0]
        seq_length = batch["input"].shape[1]
        throughput = (batch_size * seq_length) / step_time
        tokens_per_second = throughput / step_time
        
        # Actualizar métricas
        metrics.update({
            "loss": loss,
            "grad_norm": grad_norm,
            "learning_rate": state.opt_state.hyperparams['learning_rate'],
            "throughput": throughput,
            "tokens_per_second": tokens_per_second,
            "step_time": step_time
        })
        
        # Registrar métricas
        if jax.process_index() == 0:
            if self.wandb_run is not None:
                wandb.log(metrics, step=state.step)
            if self.writer is not None:
                for k, v in metrics.items():
                    self.writer.add_scalar(f'train/{k}', v, state.step)
        
        return state, metrics
    
    def evaluate(
        self,
        state: TrainingState,
        batch: Dict[str, jnp.ndarray]
    ) -> Dict[str, jnp.ndarray]:
        """Evaluación del modelo con métricas extendidas."""
        start_time = time.time()
        
        outputs = self.apply(
            state.params,
            batch["input"],
            training=False
        )
        
        # Métricas de evaluación
        metrics = {
            "accuracy": jnp.mean(jnp.argmax(outputs["output"], axis=-1) == batch["target"]),
            "compute_savings": outputs["metrics"]["compute_savings"],
            "avg_importance": jnp.mean(outputs["metrics"]["dual_process_importance"]),
            "avg_steps": jnp.mean(outputs["metrics"]["dual_process_steps"]),
            "val_loss": jnp.mean((outputs["output"] - batch["target"]) ** 2),
            "val_perplexity": jnp.exp(jnp.mean((outputs["output"] - batch["target"]) ** 2))
        }
        
        # Calcular throughput de validación
        step_time = time.time() - start_time
        batch_size = batch["input"].shape[0]
        seq_length = batch["input"].shape[1]
        metrics.update({
            "val_throughput": (batch_size * seq_length) / step_time,
            "val_tokens_per_second": (batch_size * seq_length) / (step_time ** 2)
        })
        
        # Registrar métricas de validación
        if jax.process_index() == 0:
            if self.wandb_run is not None:
                wandb.log(metrics, step=state.step)
            if self.writer is not None:
                for k, v in metrics.items():
                    self.writer.add_scalar(f'val/{k}', v, state.step)
        
        return metrics
        
    def get_submodel_metrics(self, submodel_name: str) -> Dict[str, Any]:
        """Obtiene métricas de un submodelo específico."""
        if submodel_name in self.submodels:
            submodel = self.submodels[submodel_name]
            if hasattr(submodel, "get_metrics"):
                return submodel.get_metrics()
        return {}
        
    def get_all_metrics(self) -> Dict[str, Any]:
        """Obtiene métricas de todos los submodelos."""
        return {
            name: submodel.get_metrics() if hasattr(submodel, "get_metrics") else {}
            for name, submodel in self.submodels.items()
        }

    def benchmark_step(self, state: TrainingState, batch_size: int = 1024, num_steps: int = 100) -> Dict[str, float]:
        """
        Realiza un benchmark del paso de entrenamiento.
        
        Args:
            state: Estado actual del entrenamiento
            batch_size: Tamaño del batch para el benchmark
            num_steps: Número de pasos a ejecutar para el benchmark
            
        Returns:
            Dict con métricas de rendimiento:
            - avg_time: Tiempo promedio por paso (ms)
            - throughput: Ejemplos procesados por segundo
            - tokens_per_second: Tokens procesados por segundo
        """
        import timeit
        from time import time
        
        # Crear batch dummy
        dummy_batch = {
            "input": jnp.ones((batch_size, self.config.training.seq_length), dtype=self.config.get_precision_dtype()),
            "target": jnp.ones((batch_size, self.config.training.seq_length), dtype=self.config.get_precision_dtype())
        }
        
        # Función a medir
        def step_fn():
            dropout_rng = jax.random.PRNGKey(int(time()))
            state, _ = self.train_step(state, dummy_batch, dropout_rng)
            return state
        
        # Ejecutar benchmark
        total_time = timeit.timeit(step_fn, number=num_steps)
        avg_time = (total_time / num_steps) * 1000  # Convertir a milisegundos
        
        # Calcular métricas
        throughput = (batch_size * num_steps) / total_time
        tokens_per_second = (batch_size * self.config.training.seq_length * num_steps) / total_time
        
        return {
            "avg_time": avg_time,
            "throughput": throughput,
            "tokens_per_second": tokens_per_second
        } 