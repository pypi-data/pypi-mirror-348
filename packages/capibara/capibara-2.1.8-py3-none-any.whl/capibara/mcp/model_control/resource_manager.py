from typing import Dict, Optional, List
from dataclasses import dataclass
import logging
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class ResourceAllocation:
    model_id: str
    version: str
    resources: Dict
    allocated_at: datetime
    last_used: datetime

class ResourceManager:
    def __init__(self):
        self.allocations: Dict[str, ResourceAllocation] = {}  # model_id -> allocation
        self.total_resources = {
            "cpu": 100,  # porcentaje
            "memory": 16384,  # MB
            "gpu": 1  # número de GPUs
        }
        self.used_resources = {
            "cpu": 0,
            "memory": 0,
            "gpu": 0
        }

    async def allocate_resources(self, model_id: str, version: str, resources: Dict) -> ResourceAllocation:
        """Asigna recursos a un modelo específico."""
        if model_id in self.allocations:
            raise ValueError(f"El modelo {model_id} ya tiene recursos asignados")

        # Verificar disponibilidad de recursos
        for resource, amount in resources.items():
            if self.used_resources[resource] + amount > self.total_resources[resource]:
                raise ValueError(f"No hay suficientes recursos de {resource} disponibles")

        # Crear nueva asignación
        allocation = ResourceAllocation(
            model_id=model_id,
            version=version,
            resources=resources,
            allocated_at=datetime.now(),
            last_used=datetime.now()
        )

        # Actualizar recursos usados
        for resource, amount in resources.items():
            self.used_resources[resource] += amount

        self.allocations[model_id] = allocation
        logger.info(f"Recursos asignados para el modelo {model_id}")
        return allocation

    async def release_resources(self, model_id: str) -> None:
        """Libera los recursos asignados a un modelo."""
        if model_id not in self.allocations:
            raise ValueError(f"El modelo {model_id} no tiene recursos asignados")

        # Liberar recursos
        for resource, amount in self.allocations[model_id].resources.items():
            self.used_resources[resource] -= amount

        del self.allocations[model_id]
        logger.info(f"Recursos liberados para el modelo {model_id}")

    async def update_usage(self, model_id: str) -> None:
        """Actualiza el timestamp de último uso de un modelo."""
        if model_id in self.allocations:
            self.allocations[model_id].last_used = datetime.now()

    async def get_resource_usage(self) -> Dict:
        """Obtiene el uso actual de recursos."""
        return {
            "total": self.total_resources,
            "used": self.used_resources,
            "available": {
                resource: self.total_resources[resource] - self.used_resources[resource]
                for resource in self.total_resources
            }
        }

    async def monitor_resources(self, interval: int = 60) -> None:
        """Monitorea el uso de recursos periódicamente."""
        while True:
            usage = await self.get_resource_usage()
            logger.info(f"Estado de recursos: {usage}")
            
            # Verificar uso excesivo
            for resource, used in self.used_resources.items():
                if used > self.total_resources[resource] * 0.9:  # 90% de uso
                    logger.warning(f"Uso alto de {resource}: {used}/{self.total_resources[resource]}")

            await asyncio.sleep(interval)

    async def optimize_allocations(self) -> None:
        """Optimiza las asignaciones de recursos."""
        # Implementar lógica de optimización
        # Por ejemplo, liberar recursos de modelos inactivos
        current_time = datetime.now()
        for model_id, allocation in list(self.allocations.items()):
            if (current_time - allocation.last_used).total_seconds() > 3600:  # 1 hora
                await self.release_resources(model_id)
                logger.info(f"Recursos liberados para el modelo inactivo {model_id}") 