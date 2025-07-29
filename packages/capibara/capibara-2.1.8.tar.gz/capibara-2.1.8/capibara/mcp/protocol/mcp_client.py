import asyncio
import json
import logging
from typing import Dict, Optional, Any, Callable
from datetime import datetime
import websockets
from .mcp_messages import (
    MCPMessage, MessageType, ModelRequest, ModelResponse,
    ModelError, ControlMessage, HeartbeatMessage,
    create_request_message, create_control_message,
    create_heartbeat_message
)

logger = logging.getLogger(__name__)

class MCPClient:
    def __init__(self, server_url: str, model_id: str):
        self.server_url = server_url
        self.model_id = model_id
        self.websocket = None
        self.connected = False
        self.message_handlers: Dict[MessageType, Callable] = {}
        self.pending_requests: Dict[str, asyncio.Future] = {}
        self.heartbeat_task = None

    async def connect(self) -> None:
        """Establece conexión con el servidor MCP."""
        try:
            self.websocket = await websockets.connect(self.server_url)
            self.connected = True
            logger.info(f"Conectado al servidor MCP en {self.server_url}")
            
            # Iniciar tareas de mantenimiento
            self.heartbeat_task = asyncio.create_task(self._send_heartbeats())
            asyncio.create_task(self._receive_messages())
            
        except Exception as e:
            logger.error(f"Error al conectar con el servidor MCP: {str(e)}")
            raise

    async def disconnect(self) -> None:
        """Cierra la conexión con el servidor MCP."""
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
        if self.websocket:
            await self.websocket.close()
        self.connected = False
        logger.info("Desconectado del servidor MCP")

    async def send_request(self, request: ModelRequest) -> ModelResponse:
        """Envía una solicitud al servidor MCP."""
        if not self.connected:
            raise ConnectionError("No hay conexión con el servidor MCP")

        message = create_request_message(request)
        future = asyncio.Future()
        self.pending_requests[message.message_id] = future

        try:
            await self.websocket.send(json.dumps({
                "message_id": message.message_id,
                "message_type": message.message_type.value,
                "timestamp": message.timestamp.isoformat(),
                "payload": message.payload,
                "metadata": message.metadata
            }))
            
            response = await asyncio.wait_for(future, timeout=request.timeout)
            return response
            
        except asyncio.TimeoutError:
            del self.pending_requests[message.message_id]
            raise TimeoutError(f"Timeout al esperar respuesta para la solicitud {message.message_id}")
        except Exception as e:
            del self.pending_requests[message.message_id]
            raise

    async def send_control(self, control: ControlMessage) -> None:
        """Envía un mensaje de control al servidor MCP."""
        if not self.connected:
            raise ConnectionError("No hay conexión con el servidor MCP")

        message = create_control_message(control)
        await self.websocket.send(json.dumps({
            "message_id": message.message_id,
            "message_type": message.message_type.value,
            "timestamp": message.timestamp.isoformat(),
            "payload": message.payload,
            "metadata": message.metadata
        }))

    async def _send_heartbeats(self) -> None:
        """Envía mensajes de heartbeat periódicamente."""
        while self.connected:
            try:
                heartbeat = HeartbeatMessage(
                    model_id=self.model_id,
                    status="active",
                    metrics={"timestamp": datetime.now().timestamp()},
                    timestamp=datetime.now()
                )
                message = create_heartbeat_message(heartbeat)
                await self.websocket.send(json.dumps({
                    "message_id": message.message_id,
                    "message_type": message.message_type.value,
                    "timestamp": message.timestamp.isoformat(),
                    "payload": message.payload,
                    "metadata": message.metadata
                }))
                await asyncio.sleep(30)  # Enviar cada 30 segundos
            except Exception as e:
                logger.error(f"Error al enviar heartbeat: {str(e)}")
                await asyncio.sleep(5)  # Esperar antes de reintentar

    async def _receive_messages(self) -> None:
        """Recibe y procesa mensajes del servidor MCP."""
        while self.connected:
            try:
                message_data = await self.websocket.recv()
                message_dict = json.loads(message_data)
                
                message = MCPMessage(
                    message_id=message_dict["message_id"],
                    message_type=MessageType(message_dict["message_type"]),
                    timestamp=datetime.fromisoformat(message_dict["timestamp"]),
                    payload=message_dict["payload"],
                    metadata=message_dict.get("metadata")
                )

                # Procesar mensaje según su tipo
                if message.message_type == MessageType.RESPONSE:
                    if message.message_id in self.pending_requests:
                        future = self.pending_requests.pop(message.message_id)
                        future.set_result(ModelResponse(
                            request_id=message.payload["request_id"],
                            model_id=message.payload["model_id"],
                            version=message.payload["version"],
                            output_data=message.payload["output_data"],
                            processing_time=message.payload["processing_time"],
                            metadata=message.payload.get("metadata")
                        ))
                elif message.message_type == MessageType.ERROR:
                    if message.message_id in self.pending_requests:
                        future = self.pending_requests.pop(message.message_id)
                        future.set_exception(Exception(message.payload["error_message"]))
                elif message.message_type in self.message_handlers:
                    await self.message_handlers[message.message_type](message)

            except websockets.exceptions.ConnectionClosed:
                logger.error("Conexión con el servidor MCP cerrada")
                self.connected = False
                break
            except Exception as e:
                logger.error(f"Error al procesar mensaje: {str(e)}")

    def register_handler(self, message_type: MessageType, handler: Callable) -> None:
        """Registra un manejador para un tipo de mensaje específico."""
        self.message_handlers[message_type] = handler 