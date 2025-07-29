import asyncio
import json
import logging
from typing import Dict, Set, Optional, Any, Callable
from datetime import datetime
import websockets
from .mcp_messages import (
    MCPMessage, MessageType, ModelRequest, ModelResponse,
    ModelError, ControlMessage, HeartbeatMessage,
    create_response_message, create_error_message
)

logger = logging.getLogger(__name__)

class MCPServer:
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.model_clients: Dict[str, Set[str]] = {}  # model_id -> set of client_ids
        self.message_handlers: Dict[MessageType, Callable] = {}
        self.active_requests: Dict[str, Dict[str, Any]] = {}

    async def start(self) -> None:
        """Inicia el servidor MCP."""
        server = await websockets.serve(
            self._handle_client,
            self.host,
            self.port
        )
        logger.info(f"Servidor MCP iniciado en ws://{self.host}:{self.port}")
        await server.wait_closed()

    async def _handle_client(self, websocket: websockets.WebSocketServerProtocol, path: str) -> None:
        """Maneja la conexión de un nuevo cliente."""
        client_id = f"client_{len(self.clients)}"
        self.clients[client_id] = websocket
        logger.info(f"Nuevo cliente conectado: {client_id}")

        try:
            async for message in websocket:
                await self._process_message(client_id, message)
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Cliente desconectado: {client_id}")
        finally:
            await self._cleanup_client(client_id)

    async def _process_message(self, client_id: str, message_data: str) -> None:
        """Procesa un mensaje recibido de un cliente."""
        try:
            message_dict = json.loads(message_data)
            message = MCPMessage(
                message_id=message_dict["message_id"],
                message_type=MessageType(message_dict["message_type"]),
                timestamp=datetime.fromisoformat(message_dict["timestamp"]),
                payload=message_dict["payload"],
                metadata=message_dict.get("metadata")
            )

            # Procesar mensaje según su tipo
            if message.message_type == MessageType.REQUEST:
                await self._handle_request(client_id, message)
            elif message.message_type == MessageType.CONTROL:
                await self._handle_control(client_id, message)
            elif message.message_type == MessageType.HEARTBEAT:
                await self._handle_heartbeat(client_id, message)
            elif message.message_type in self.message_handlers:
                await self.message_handlers[message.message_type](client_id, message)

        except json.JSONDecodeError:
            logger.error(f"Error al decodificar mensaje de {client_id}")
        except Exception as e:
            logger.error(f"Error al procesar mensaje de {client_id}: {str(e)}")

    async def _handle_request(self, client_id: str, message: MCPMessage) -> None:
        """Maneja una solicitud de modelo."""
        try:
            model_id = message.payload["model_id"]
            if model_id not in self.model_clients:
                raise ValueError(f"Modelo {model_id} no disponible")

            # Registrar solicitud activa
            self.active_requests[message.message_id] = {
                "client_id": client_id,
                "model_id": model_id,
                "timestamp": datetime.now(),
                "status": "processing"
            }

            # Procesar solicitud (simulado)
            await asyncio.sleep(0.1)  # Simular procesamiento

            # Enviar respuesta
            response = ModelResponse(
                request_id=message.message_id,
                model_id=model_id,
                version=message.payload.get("version", "latest"),
                output_data={"result": "Respuesta simulada"},
                processing_time=0.1
            )
            response_message = create_response_message(response)
            await self.clients[client_id].send(json.dumps({
                "message_id": response_message.message_id,
                "message_type": response_message.message_type.value,
                "timestamp": response_message.timestamp.isoformat(),
                "payload": response_message.payload,
                "metadata": response_message.metadata
            }))

        except Exception as e:
            error = ModelError(
                request_id=message.message_id,
                error_code="PROCESSING_ERROR",
                error_message=str(e)
            )
            error_message = create_error_message(error)
            await self.clients[client_id].send(json.dumps({
                "message_id": error_message.message_id,
                "message_type": error_message.message_type.value,
                "timestamp": error_message.timestamp.isoformat(),
                "payload": error_message.payload,
                "metadata": error_message.metadata
            }))

    async def _handle_control(self, client_id: str, message: MCPMessage) -> None:
        """Maneja un mensaje de control."""
        try:
            control_type = message.payload["control_type"]
            target_model = message.payload.get("target_model")
            parameters = message.payload.get("parameters", {})

            if control_type == "register_model":
                if target_model not in self.model_clients:
                    self.model_clients[target_model] = set()
                self.model_clients[target_model].add(client_id)
                logger.info(f"Modelo {target_model} registrado por {client_id}")

            elif control_type == "unregister_model":
                if target_model in self.model_clients:
                    self.model_clients[target_model].discard(client_id)
                    if not self.model_clients[target_model]:
                        del self.model_clients[target_model]
                    logger.info(f"Modelo {target_model} desregistrado por {client_id}")

        except Exception as e:
            logger.error(f"Error al procesar mensaje de control de {client_id}: {str(e)}")

    async def _handle_heartbeat(self, client_id: str, message: MCPMessage) -> None:
        """Maneja un mensaje de heartbeat."""
        try:
            model_id = message.payload["model_id"]
            status = message.payload["status"]
            metrics = message.payload["metrics"]
            logger.debug(f"Heartbeat de {model_id} ({client_id}): {status} - {metrics}")
        except Exception as e:
            logger.error(f"Error al procesar heartbeat de {client_id}: {str(e)}")

    async def _cleanup_client(self, client_id: str) -> None:
        """Limpia los recursos asociados a un cliente desconectado."""
        if client_id in self.clients:
            del self.clients[client_id]

        # Limpiar registros de modelos
        for model_id, clients in list(self.model_clients.items()):
            clients.discard(client_id)
            if not clients:
                del self.model_clients[model_id]

        # Limpiar solicitudes activas
        for request_id, request in list(self.active_requests.items()):
            if request["client_id"] == client_id:
                del self.active_requests[request_id]

    def register_handler(self, message_type: MessageType, handler: Callable) -> None:
        """Registra un manejador para un tipo de mensaje específico."""
        self.message_handlers[message_type] = handler

    async def broadcast(self, message: MCPMessage, target_model: Optional[str] = None) -> None:
        """Envía un mensaje a todos los clientes o a los clientes de un modelo específico."""
        message_data = json.dumps({
            "message_id": message.message_id,
            "message_type": message.message_type.value,
            "timestamp": message.timestamp.isoformat(),
            "payload": message.payload,
            "metadata": message.metadata
        })

        if target_model:
            if target_model in self.model_clients:
                for client_id in self.model_clients[target_model]:
                    if client_id in self.clients:
                        await self.clients[client_id].send(message_data)
        else:
            for client in self.clients.values():
                await client.send(message_data) 