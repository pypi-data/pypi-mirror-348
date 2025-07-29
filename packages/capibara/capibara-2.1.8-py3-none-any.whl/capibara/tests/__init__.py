"""
tests/__init__.py

Este módulo inicializa el paquete de pruebas y proporciona utilidades comunes,
configuraciones y fixtures para probar el modelo CapibaraGPT.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Union, TYPE_CHECKING
import dataclasses

if TYPE_CHECKING:
    import pytest #type: ignore
else:
    try:
        import pytest
    except ImportError:
        raise ImportError(
            "pytest is required for testing. Install it with: pip install pytest"
        )

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from capibara.core.config import Config as CapibaraConfig, get_default_config
    from capibara.core.inference import InferenceConfig
    from capibara.utils.logging import setup_logging
    from pydantic import BaseModel, Field
    
    class LogConfig(BaseModel):
        log_level: str = Field(default='INFO')
    
    # Configure logging
    setup_logging(LogConfig())
except ImportError as e:
    logger.error(f"Failed to import capibara_model: {str(e)}")

# Common test configurations
BASE_TEST_CONFIG = get_default_config()

# Configuración pequeña para pruebas rápidas
SMALL_TEST_CONFIG = get_default_config()
SMALL_TEST_CONFIG.training = dataclasses.replace(
    SMALL_TEST_CONFIG.training,
    batch_size=16,
    learning_rate=0.001
)
SMALL_TEST_CONFIG.validation = dataclasses.replace(
    SMALL_TEST_CONFIG.validation,
    val_batch_size=16
)

# Configuración grande para pruebas de escalabilidad
LARGE_TEST_CONFIG = get_default_config()
LARGE_TEST_CONFIG.training = dataclasses.replace(
    LARGE_TEST_CONFIG.training,
    batch_size=64,
    learning_rate=0.0001
)
LARGE_TEST_CONFIG.validation = dataclasses.replace(
    LARGE_TEST_CONFIG.validation,
    val_batch_size=64
)

def create_random_input(
    rng: Any,
    batch_size: int = 1,
    config: Optional[CapibaraConfig] = None,
    backend: str = 'jax'
) -> Any:
    """
    Creates a random input array for testing.

    Args:
        rng: Random number generator
        batch_size: Batch size for input
        config: Optional config, uses BASE_TEST_CONFIG if None
        backend: Backend to use ('jax' or 'torch')

    Returns:
        Random tensor of appropriate type
    """
    cfg = config if config is not None else BASE_TEST_CONFIG
    
    if backend == 'jax':
        import jax.random as jrandom
        return jrandom.randint(
            rng,
            (batch_size, cfg.training.seq_length),
            0,
            cfg.training.vocab_size
        )
    elif backend == 'torch':
        import torch
        generator = torch.Generator()
        if isinstance(rng, int):
            generator.manual_seed(rng)
        return torch.randint(
            0,
            cfg.training.vocab_size,
            (batch_size, cfg.training.seq_length),
            generator=generator
        )
    else:
        raise ValueError(f"Backend {backend} not supported. Use 'jax' or 'torch'.")

# Pytest fixtures
@pytest.fixture(scope="function")
def random_seed() -> int:
    """Provides a fixed random seed for reproducibility."""
    return 42

@pytest.fixture(scope="function")
def jax_rng(random_seed: int) -> Any:
    """Provides a fresh JAX random key for each test."""
    try:
        import jax
        return jax.random.PRNGKey(random_seed)
    except ImportError:
        pytest.skip("JAX not installed")

@pytest.fixture(scope="function")
def torch_generator(random_seed: int) -> Any:
    """Provides a fresh PyTorch generator for each test."""
    try:
        import torch
        return torch.Generator().manual_seed(random_seed)
    except ImportError:
        pytest.skip("PyTorch not installed")

@pytest.fixture(scope="session")
def test_configs() -> Dict[str, CapibaraConfig]:
    """Provides access to all test configurations."""
    return {
        'base': BASE_TEST_CONFIG,
        'small': SMALL_TEST_CONFIG,
        'large': LARGE_TEST_CONFIG
    }

def setup_test_environment() -> None:
    """Sets up the test environment with necessary configurations."""
    try:
        # Set up environment variables
        os.environ['CAPIBARA_LOG_LEVEL'] = 'ERROR'
        os.environ['CAPIBARA_TEST_MODE'] = 'TRUE'

        # Create test directories if needed
        test_data_dir = Path(__file__).parent / 'test_data'
        test_data_dir.mkdir(exist_ok=True)

        logger.info("Test environment setup completed successfully")
    except Exception as e:
        logger.error(f"Test environment setup failed: {str(e)}")
        raise RuntimeError(f"Environment setup failed: {str(e)}")

# Initialize test environment when module is imported
setup_test_environment()
