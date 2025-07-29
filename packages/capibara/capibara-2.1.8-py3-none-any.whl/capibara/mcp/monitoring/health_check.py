from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging
import asyncio
import psutil
import GPUtil
from .metrics import ModelMetrics

logger = logging.getLogger(__name__)

@dataclass
class HealthStatus:
    status: str
    timestamp: datetime
    details: Dict
    metrics: Dict

class HealthChecker:
    def __init__(self, model_metrics: ModelMetrics):
        self.model_metrics = model_metrics
        self.health_status: Dict[str, HealthStatus] = {}
        self.check_interval = 60  # segundos
        self.warning_thresholds = {
            "cpu_usage": 80,  # porcentaje
            "memory_usage": 80,  # porcentaje
            "gpu_usage": 80,  # porcentaje
            "error_rate": 0.1,  # 10% de errores
            "latency": 1000  # ms
        }

    async def check_model_health(self, model_id: str) -> HealthStatus:
        """Verifica la salud de un modelo específico."""
        try:
            # Obtener métricas recientes
            metrics = await self.model_metrics.get_model_metrics(model_id, window_seconds=300)  # últimos 5 minutos
            
            # Verificar uso de recursos
            cpu_usage = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            gpu_usage = 0
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu_usage = gpus[0].load * 100
            except:
                pass

            # Calcular tasa de errores
            error_rate = 0
            if metrics["request_count"]["count"] > 0:
                error_rate = metrics["error_count"]["count"] / metrics["request_count"]["count"]

            # Determinar estado
            status = "healthy"
            details = {
                "cpu_usage": cpu_usage,
                "memory_usage": memory.percent,
                "gpu_usage": gpu_usage,
                "error_rate": error_rate,
                "avg_latency": metrics["request_latency"]["avg"]
            }

            # Verificar umbrales
            if (cpu_usage > self.warning_thresholds["cpu_usage"] or
                memory.percent > self.warning_thresholds["memory_usage"] or
                gpu_usage > self.warning_thresholds["gpu_usage"] or
                error_rate > self.warning_thresholds["error_rate"] or
                metrics["request_latency"]["avg"] > self.warning_thresholds["latency"]):
                status = "warning"
                logger.warning(f"Modelo {model_id} en estado de advertencia: {details}")

            health_status = HealthStatus(
                status=status,
                timestamp=datetime.now(),
                details=details,
                metrics=metrics
            )

            self.health_status[model_id] = health_status
            return health_status

        except Exception as e:
            logger.error(f"Error al verificar salud del modelo {model_id}: {str(e)}")
            return HealthStatus(
                status="error",
                timestamp=datetime.now(),
                details={"error": str(e)},
                metrics={}
            )

    async def get_model_health(self, model_id: str) -> Optional[HealthStatus]:
        """Obtiene el estado de salud de un modelo."""
        return self.health_status.get(model_id)

    async def get_all_health_status(self) -> Dict[str, HealthStatus]:
        """Obtiene el estado de salud de todos los modelos."""
        return self.health_status

    async def monitor_health(self) -> None:
        """Monitorea la salud de los modelos periódicamente."""
        while True:
            try:
                # Obtener lista de modelos activos
                all_metrics = await self.model_metrics.get_all_metrics()
                model_ids = set()
                for metric_name, points in all_metrics.items():
                    for point in points:
                        if "model_id" in point.labels:
                            model_ids.add(point.labels["model_id"])

                # Verificar salud de cada modelo
                for model_id in model_ids:
                    await self.check_model_health(model_id)

                await asyncio.sleep(self.check_interval)

            except Exception as e:
                logger.error(f"Error en monitoreo de salud: {str(e)}")
                await asyncio.sleep(5)  # Esperar antes de reintentar

    def set_warning_thresholds(self, thresholds: Dict[str, float]) -> None:
        """Actualiza los umbrales de advertencia."""
        self.warning_thresholds.update(thresholds)
        logger.info(f"Umbrales de advertencia actualizados: {self.warning_thresholds}")

    async def get_system_health(self) -> Dict:
        """Obtiene el estado de salud del sistema."""
        try:
            cpu_usage = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            gpu_info = {}
            try:
                gpus = GPUtil.getGPUs()
                for gpu in gpus:
                    gpu_info[f"gpu_{gpu.id}"] = {
                        "usage": gpu.load * 100,
                        "memory_used": gpu.memoryUsed,
                        "memory_total": gpu.memoryTotal,
                        "temperature": gpu.temperature
                    }
            except:
                pass

            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "system": {
                    "cpu_usage": cpu_usage,
                    "memory_usage": memory.percent,
                    "disk_usage": disk.percent,
                    "gpu_info": gpu_info
                }
            }

        except Exception as e:
            logger.error(f"Error al obtener estado de salud del sistema: {str(e)}")
            return {
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            } 