from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class ModelVersion:
    version: str
    model_id: str
    created_at: datetime
    status: str
    metadata: Dict
    resources: Dict

class VersionManager:
    def __init__(self):
        self.versions: Dict[str, ModelVersion] = {}
        self.active_versions: Dict[str, str] = {}  # model_id -> version

    async def register_version(self, model_id: str, version: str, metadata: Dict) -> ModelVersion:
        """Registra una nueva versión de un modelo."""
        if model_id in self.versions and version in self.versions[model_id]:
            raise ValueError(f"La versión {version} ya existe para el modelo {model_id}")

        model_version = ModelVersion(
            version=version,
            model_id=model_id,
            created_at=datetime.now(),
            status="registered",
            metadata=metadata,
            resources={}
        )

        if model_id not in self.versions:
            self.versions[model_id] = {}
        self.versions[model_id][version] = model_version

        logger.info(f"Versión {version} registrada para el modelo {model_id}")
        return model_version

    async def activate_version(self, model_id: str, version: str) -> None:
        """Activa una versión específica de un modelo."""
        if model_id not in self.versions or version not in self.versions[model_id]:
            raise ValueError(f"La versión {version} no existe para el modelo {model_id}")

        self.active_versions[model_id] = version
        self.versions[model_id][version].status = "active"
        logger.info(f"Versión {version} activada para el modelo {model_id}")

    async def get_active_version(self, model_id: str) -> Optional[str]:
        """Obtiene la versión activa de un modelo."""
        return self.active_versions.get(model_id)

    async def list_versions(self, model_id: str) -> List[ModelVersion]:
        """Lista todas las versiones de un modelo."""
        if model_id not in self.versions:
            return []
        return list(self.versions[model_id].values())

    async def update_metadata(self, model_id: str, version: str, metadata: Dict) -> None:
        """Actualiza los metadatos de una versión específica."""
        if model_id not in self.versions or version not in self.versions[model_id]:
            raise ValueError(f"La versión {version} no existe para el modelo {model_id}")

        self.versions[model_id][version].metadata.update(metadata)
        logger.info(f"Metadatos actualizados para la versión {version} del modelo {model_id}")

    async def deactivate_version(self, model_id: str, version: str) -> None:
        """Desactiva una versión específica de un modelo."""
        if model_id not in self.versions or version not in self.versions[model_id]:
            raise ValueError(f"La versión {version} no existe para el modelo {model_id}")

        if self.active_versions.get(model_id) == version:
            del self.active_versions[model_id]
        
        self.versions[model_id][version].status = "inactive"
        logger.info(f"Versión {version} desactivada para el modelo {model_id}") 