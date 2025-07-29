from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging
import asyncio
from collections import deque

logger = logging.getLogger(__name__)

@dataclass
class MetricPoint:
    timestamp: datetime
    value: float
    labels: Dict[str, str]

class MetricsCollector:
    def __init__(self, max_points: int = 1000):
        self.metrics: Dict[str, deque] = {}
        self.max_points = max_points
        self.lock = asyncio.Lock()

    async def record_metric(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Registra un nuevo punto de métrica."""
        async with self.lock:
            if name not in self.metrics:
                self.metrics[name] = deque(maxlen=self.max_points)

            point = MetricPoint(
                timestamp=datetime.now(),
                value=value,
                labels=labels or {}
            )
            self.metrics[name].append(point)
            logger.debug(f"Métrica {name} registrada: {value}")

    async def get_metric(self, name: str, window_seconds: Optional[int] = None) -> List[MetricPoint]:
        """Obtiene los puntos de una métrica específica."""
        async with self.lock:
            if name not in self.metrics:
                return []

            points = list(self.metrics[name])
            if window_seconds:
                cutoff = datetime.now().timestamp() - window_seconds
                points = [p for p in points if p.timestamp.timestamp() > cutoff]

            return points

    async def get_metric_summary(self, name: str, window_seconds: Optional[int] = None) -> Dict:
        """Obtiene un resumen de una métrica específica."""
        points = await self.get_metric(name, window_seconds)
        if not points:
            return {
                "count": 0,
                "min": 0,
                "max": 0,
                "avg": 0
            }

        values = [p.value for p in points]
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values)
        }

    async def get_all_metrics(self) -> Dict[str, List[MetricPoint]]:
        """Obtiene todas las métricas registradas."""
        async with self.lock:
            return {name: list(points) for name, points in self.metrics.items()}

class ModelMetrics:
    def __init__(self):
        self.collector = MetricsCollector()
        self.metrics = {
            "request_latency": "Tiempo de respuesta (ms)",
            "request_count": "Número de solicitudes",
            "error_count": "Número de errores",
            "memory_usage": "Uso de memoria (MB)",
            "cpu_usage": "Uso de CPU (%)",
            "gpu_usage": "Uso de GPU (%)"
        }

    async def record_request(self, model_id: str, latency_ms: float, success: bool) -> None:
        """Registra métricas de una solicitud."""
        labels = {"model_id": model_id}
        
        await self.collector.record_metric(
            "request_latency",
            latency_ms,
            labels
        )
        
        await self.collector.record_metric(
            "request_count",
            1,
            labels
        )
        
        if not success:
            await self.collector.record_metric(
                "error_count",
                1,
                labels
            )

    async def record_resource_usage(self, model_id: str, memory_mb: float, cpu_percent: float, gpu_percent: float) -> None:
        """Registra métricas de uso de recursos."""
        labels = {"model_id": model_id}
        
        await self.collector.record_metric(
            "memory_usage",
            memory_mb,
            labels
        )
        
        await self.collector.record_metric(
            "cpu_usage",
            cpu_percent,
            labels
        )
        
        await self.collector.record_metric(
            "gpu_usage",
            gpu_percent,
            labels
        )

    async def get_model_metrics(self, model_id: str, window_seconds: Optional[int] = None) -> Dict:
        """Obtiene todas las métricas de un modelo específico."""
        metrics = {}
        for metric_name in self.metrics:
            summary = await self.collector.get_metric_summary(
                metric_name,
                window_seconds
            )
            metrics[metric_name] = summary
        return metrics

    async def get_all_metrics(self) -> Dict:
        """Obtiene todas las métricas registradas."""
        return await self.collector.get_all_metrics()

    async def clear_metrics(self) -> None:
        """Limpia todas las métricas registradas."""
        async with self.collector.lock:
            self.collector.metrics.clear() 