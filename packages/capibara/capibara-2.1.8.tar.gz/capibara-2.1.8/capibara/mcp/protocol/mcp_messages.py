from typing import Dict, Optional, List, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class MessageType(Enum):
    REQUEST = "request"
    RESPONSE = "response"
    ERROR = "error"
    HEARTBEAT = "heartbeat"
    CONTROL = "control"

class ControlType(Enum):
    LOAD_MODEL = "load_model"
    UNLOAD_MODEL = "unload_model"
    UPDATE_MODEL = "update_model"
    GET_STATUS = "get_status"
    SET_CONFIG = "set_config"

@dataclass
class MCPMessage:
    message_id: str
    message_type: MessageType
    timestamp: datetime
    payload: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class ModelRequest:
    model_id: str
    version: Optional[str]
    input_data: Dict[str, Any]
    priority: int = 1
    timeout: int = 30

@dataclass
class ModelResponse:
    request_id: str
    model_id: str
    version: str
    output_data: Dict[str, Any]
    processing_time: float
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class ModelError:
    request_id: str
    error_code: str
    error_message: str
    details: Optional[Dict[str, Any]] = None

@dataclass
class ControlMessage:
    control_type: ControlType
    target_model: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

@dataclass
class HeartbeatMessage:
    model_id: str
    status: str
    metrics: Dict[str, Any]
    timestamp: datetime

def create_request_message(model_request: ModelRequest) -> MCPMessage:
    """Crea un mensaje de solicitud."""
    return MCPMessage(
        message_id=f"req_{datetime.now().timestamp()}",
        message_type=MessageType.REQUEST,
        timestamp=datetime.now(),
        payload={
            "model_id": model_request.model_id,
            "version": model_request.version,
            "input_data": model_request.input_data,
            "priority": model_request.priority,
            "timeout": model_request.timeout
        }
    )

def create_response_message(model_response: ModelResponse) -> MCPMessage:
    """Crea un mensaje de respuesta."""
    return MCPMessage(
        message_id=f"resp_{datetime.now().timestamp()}",
        message_type=MessageType.RESPONSE,
        timestamp=datetime.now(),
        payload={
            "request_id": model_response.request_id,
            "model_id": model_response.model_id,
            "version": model_response.version,
            "output_data": model_response.output_data,
            "processing_time": model_response.processing_time,
            "metadata": model_response.metadata
        }
    )

def create_error_message(model_error: ModelError) -> MCPMessage:
    """Crea un mensaje de error."""
    return MCPMessage(
        message_id=f"err_{datetime.now().timestamp()}",
        message_type=MessageType.ERROR,
        timestamp=datetime.now(),
        payload={
            "request_id": model_error.request_id,
            "error_code": model_error.error_code,
            "error_message": model_error.error_message,
            "details": model_error.details
        }
    )

def create_control_message(control_message: ControlMessage) -> MCPMessage:
    """Crea un mensaje de control."""
    return MCPMessage(
        message_id=f"ctrl_{datetime.now().timestamp()}",
        message_type=MessageType.CONTROL,
        timestamp=datetime.now(),
        payload={
            "control_type": control_message.control_type.value,
            "target_model": control_message.target_model,
            "parameters": control_message.parameters
        }
    )

def create_heartbeat_message(heartbeat: HeartbeatMessage) -> MCPMessage:
    """Crea un mensaje de heartbeat."""
    return MCPMessage(
        message_id=f"hb_{datetime.now().timestamp()}",
        message_type=MessageType.HEARTBEAT,
        timestamp=datetime.now(),
        payload={
            "model_id": heartbeat.model_id,
            "status": heartbeat.status,
            "metrics": heartbeat.metrics,
            "timestamp": heartbeat.timestamp.isoformat()
        }
    ) 