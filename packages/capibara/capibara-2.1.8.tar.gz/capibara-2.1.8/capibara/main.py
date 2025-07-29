"""
Entry point for CapibaraModel training and inference.

This module handles command-line arguments, loads configuration, and delegates
the training or inference process to specialized modules.
"""

import logging
import argparse
from pathlib import Path
from typing import Optional

# Importamos la clase de configuración y la función de carga
from capibara.core.config import CapibaraConfig, load_config

# Configurar el logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('capibara.log')
    ]
)
logger = logging.getLogger(__name__)

def main() -> None:
    """
    Función principal que maneja los argumentos de línea de comandos,
    carga la configuración y delega el proceso apropiado.
    """
    parser = argparse.ArgumentParser(description='Entrenamiento e inferencia de CapibaraModel')
    parser.add_argument(
        '--config',
        type=Path,
        required=True,
        help='Ruta al archivo de configuración YAML'
    )
    parser.add_argument(
        '--mode',
        type=str,
        choices=['train', 'inference'],
        default='train',
        help='Modo de operación (train/inference)'
    )
    parser.add_argument(
        '--checkpoint',
        type=Path,
        help='Ruta al checkpoint para cargar (opcional)'
    )
    
    args = parser.parse_args()

    try:
        # Cargar configuración
        config = load_config(args.config)
        logger.info("Configuración cargada exitosamente")
        
        # Crear directorios necesarios
        for path in [
            config.paths.data_dir,
            config.paths.checkpoint_dir,
            config.paths.output_dir,
            config.paths.log_dir
        ]:
            path.mkdir(parents=True, exist_ok=True)
        
        if args.mode == 'train':
            from capibara.training.train_unified import train_model as run_training
            run_training(config, output_dir=config.paths.output_dir, use_tpu=config.tpu.use_tpu)
        else:  # inference
            from capibara.core.inference import run_inference
            run_inference(config, checkpoint_path=args.checkpoint)
            
    except FileNotFoundError:
        logger.error(f"No se encontró el archivo de configuración: {args.config}")
    except Exception as e:
        logger.error(f"Error durante la ejecución: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
