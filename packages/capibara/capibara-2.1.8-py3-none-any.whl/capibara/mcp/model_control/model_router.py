from typing import Dict, Optional, List, Any
from dataclasses import dataclass
import logging
import asyncio
from datetime import datetime
from .version_manager import VersionManager
from .resource_manager import ResourceManager

logger = logging.getLogger(__name__)

@dataclass
class ModelRequest:
    model_id: str
    version: Optional[str]
    input_data: Dict[str, Any]
    priority: int = 1
    timeout: int = 30

class ModelRouter:
    def __init__(self, version_manager: VersionManager, resource_manager: ResourceManager):
        self.version_manager = version_manager
        self.resource_manager = resource_manager
        self.request_queue: asyncio.Queue[ModelRequest] = asyncio.Queue()
        self.active_requests: Dict[str, ModelRequest] = {}
        self.request_history: List[Dict] = []

    async def route_request(self, request: ModelRequest) -> Dict[str, Any]:
        """Enruta una solicitud a un modelo específico."""
        try:
            # Verificar versión
            if request.version is None:
                request.version = await self.version_manager.get_active_version(request.model_id)
                if request.version is None:
                    raise ValueError(f"No hay versión activa para el modelo {request.model_id}")

            # Verificar recursos
            await self.resource_manager.update_usage(request.model_id)

            # Procesar solicitud
            result = await self._process_request(request)

            # Registrar en historial
            self.request_history.append({
                "model_id": request.model_id,
                "version": request.version,
                "timestamp": datetime.now(),
                "status": "success"
            })

            return result

        except Exception as e:
            logger.error(f"Error al procesar solicitud: {str(e)}")
            self.request_history.append({
                "model_id": request.model_id,
                "version": request.version,
                "timestamp": datetime.now(),
                "status": "error",
                "error": str(e)
            })
            raise

    async def _process_request(self, request: ModelRequest) -> Dict[str, Any]:
        """Procesa una solicitud de modelo."""
        # Aquí se implementaría la lógica real de procesamiento
        # Por ahora, simulamos una respuesta
        await asyncio.sleep(0.1)  # Simular procesamiento
        return {
            "status": "success",
            "model_id": request.model_id,
            "version": request.version,
            "result": "Respuesta simulada"
        }

    async def get_request_history(self, model_id: Optional[str] = None) -> List[Dict]:
        """Obtiene el historial de solicitudes."""
        if model_id:
            return [req for req in self.request_history if req["model_id"] == model_id]
        return self.request_history

    async def get_active_requests(self) -> Dict[str, ModelRequest]:
        """Obtiene las solicitudes activas."""
        return self.active_requests

    async def cancel_request(self, request_id: str) -> None:
        """Cancela una solicitud activa."""
        if request_id in self.active_requests:
            del self.active_requests[request_id]
            logger.info(f"Solicitud {request_id} cancelada")

    async def monitor_requests(self, interval: int = 60) -> None:
        """Monitorea las solicitudes activas."""
        while True:
            active_count = len(self.active_requests)
            if active_count > 0:
                logger.info(f"Solicitudes activas: {active_count}")
            
            # Verificar timeouts
            current_time = datetime.now()
            for request_id, request in list(self.active_requests.items()):
                if (current_time - request.timestamp).total_seconds() > request.timeout:
                    await self.cancel_request(request_id)
                    logger.warning(f"Solicitud {request_id} cancelada por timeout")

            await asyncio.sleep(interval) 