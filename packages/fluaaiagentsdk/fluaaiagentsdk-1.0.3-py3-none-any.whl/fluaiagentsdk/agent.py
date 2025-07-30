from enum import Enum
import json
import logging
import re
import uuid
from typing import Tuple, Dict, AsyncGenerator, Union, Optional, Callable, List, Any
import aiohttp
from dataclasses import dataclass, field, asdict
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)

class AgentEngine(Enum):
    operator = "operator"
    llm = "llm"

class StreamMode(Enum):
    """Modo de streaming para controlar como os dados são retornados."""
    DISABLED = "disabled"
    ENABLED = "enabled"

@dataclass
class Message:
    """Representa uma mensagem na conversação do agente."""
    role: str
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_responses: Optional[List[Dict[str, Any]]] = None

@dataclass
class AgentResponse:
    """Representa a resposta de um agente."""
    engine: str = ""
    conversation_id: str = ""
    output: str = ""
    args: Dict[str, Any] = field(default_factory=dict)
    
    # Campos específicos para engine 'operator'
    task_id: Optional[str] = None
    live_url: Optional[str] = None
    status: Optional[str] = None
    screenshots: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Processamento após a inicialização para preencher campos específicos do engine."""
        # Se os campos específicos estão nos args, copiá-los para os atributos principais
        if self.args:
            if 'task_id' in self.args and not self.task_id:
                self.task_id = self.args.get('task_id')
            
            if 'live_url' in self.args and not self.live_url:
                self.live_url = self.args.get('live_url')
            
            if 'status' in self.args and not self.status:
                self.status = self.args.get('status')
            
            if 'screenshots' in self.args and not self.screenshots:
                self.screenshots = self.args.get('screenshots', [])
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte a resposta para um dicionário."""
        result = asdict(self)
        return result
    
    def to_json(self) -> str:
        """Converte a resposta para uma string JSON."""
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentResponse':
        """Cria uma instância de AgentResponse a partir de um dicionário."""
        # Extrair campos básicos
        response = cls(
            engine=data.get('engine', ''),
            conversation_id=data.get('conversation_id', ''),
            output=data.get('output', ''),
            args=data.get('args', {}),
        )
        
        # Aplicar post_init para processar campos adicionais
        response.__post_init__()
        
        return response
    
    @classmethod
    def from_json(cls, json_str: str) -> 'AgentResponse':
        """Cria uma instância de AgentResponse a partir de uma string JSON."""
        return cls.from_dict(json.loads(json_str))
    
    def __getitem__(self, key: str) -> Any:
        """
        Permite acessar campos como se fosse um dicionário para compatibilidade
        com código existente. Por exemplo: response['output']
        """
        if hasattr(self, key):
            return getattr(self, key)
        
        # Verificar em args como fallback
        if key in self.args:
            return self.args[key]
        
        # Levantar KeyError para comportamento consistente com dicionários
        raise KeyError(f"'{key}' não encontrado em AgentResponse")

class Agent:
    AGENT_API_URL = "https://fluaai-agent-integration.azurewebsites.net/chat"
    
    @staticmethod
    async def agent_invoke(
        prompt: str,
        agent_id: str = None,
        conversation_id: str = None,
        stream_mode: Union[StreamMode, str] = StreamMode.DISABLED,
        on_chunk: Optional[Callable[[str, Dict], None]] = None,
        # New auth parameters
        auth_token: str = None,
        api_key: str = None,
        channel: str = "integration",
    ) -> Union[Tuple[bool, Dict], AsyncGenerator[Tuple[bool, Dict], None]]:
        """
        Invoca um agente com opções de streaming flexíveis e autenticação.
        
        Args:
            prompt: Texto enviado ao agente
            agent_id: ID do agente
            conversation_id: ID da conversa (opcional, gera um novo se não fornecido)
            stream_mode: Modo de streaming (DISABLED, ENABLED)
            on_chunk: Callback opcional para processar chunks em tempo real
            auth_token: Token JWT para autenticação (opcional)
            api_key: Chave de API para autenticação (opcional)
            channel: Identificador da chamada (opcional)
            auth_type: Tipo de autenticação a ser usado (TOKEN ou API_KEY)
            
        Returns:
            Dependendo do stream_mode:
            - DISABLED: Tuple[bool, Dict] com resposta final
            - ENABLED: AsyncGenerator que retorna cada chunk
        """
        if conversation_id is None:
            conversation_id = str(uuid.uuid4())
            
        if isinstance(stream_mode, str):
            try:
                stream_mode = StreamMode(stream_mode.lower())
            except ValueError:
                stream_mode = StreamMode.DISABLED
                logger.warning(f"Modo de stream inválido: '{stream_mode}'. Usando DISABLED como padrão.")
    
        request_body = {
            "message": prompt,
            "agent_id": agent_id,
            "conversation_id": conversation_id,
            "channel": channel
        }
        
        # Set up headers with authentication
        headers = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }
        
        # Add authentication header based on type
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        elif api_key:
            headers["X-API-Key"] = api_key

        if stream_mode == StreamMode.ENABLED:
            return Agent._stream_response(request_body, headers, conversation_id)
        else:
            return await Agent._collect_response(request_body, headers, conversation_id, on_chunk)
    
    @staticmethod
    async def _stream_response(request_body: Dict, headers: Dict, conversation_id: str) -> AsyncGenerator[Tuple[bool, AgentResponse], None]:
        """Generator assíncrono que entrega cada chunk como AgentResponse."""
        handshake = {}
        args = {}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    Agent.AGENT_API_URL, 
                    json=request_body,
                    headers=headers
                ) as response:
                    if not response.ok:
                        error_msg = f"Erro na API de agentes: {response.status} {response.reason}"
                        logger.error(error_msg)
                        yield False, AgentResponse(
                            engine="",
                            conversation_id=conversation_id,
                            args={},
                            output=error_msg
                        )
                        return
                    
                    async for chunk in response.content.iter_chunks():
                        if chunk[0]:
                            text_chunk = chunk[0].decode('utf-8')
                            
                            # Processar handshake (primeira mensagem com metadados)
                            if "engine" in text_chunk and "conversation_id" in text_chunk:
                                try:
                                    handshake = json.loads(text_chunk)
                                    continue
                                except json.JSONDecodeError:
                                    logger.error(f"Erro ao decodificar handshake: {text_chunk}")
                                    continue
                            
                            # Processar chunks de texto e JSON para o operador
                            chunk_data = {"output": text_chunk}
                            
                            if handshake.get("engine") == AgentEngine.operator.value:
                                try:
                                    chunk_json = json.loads(text_chunk)
                                    chunk_data = chunk_json
                                    args.update(chunk_json)
                                except json.JSONDecodeError:
                                    # Se não for JSON válido, trata como texto normal
                                    pass
                            
                            # Criar objeto de resposta para o chunk
                            response_obj = AgentResponse(
                                engine=handshake.get("engine", ""),
                                conversation_id=handshake.get("conversation_id", conversation_id),
                                args=args,
                                **chunk_data
                            )
                            
                            yield True, response_obj
        
        except Exception as e:
            error_msg = f"Erro ao chamar API de agentes em modo streaming: {str(e)}"
            logger.error(error_msg)
            yield False, AgentResponse(
                engine="",
                conversation_id=conversation_id,
                args={},
                output=error_msg
            )
    
    @staticmethod
    async def _collect_response(
        request_body: Dict, 
        headers: Dict, 
        conversation_id: str,
        on_chunk: Optional[Callable[[str, AgentResponse], None]] = None
    ) -> Tuple[bool, AgentResponse]:
        """Coleta todos os chunks e retorna a resposta completa como AgentResponse."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    Agent.AGENT_API_URL, 
                    json=request_body,
                    headers=headers
                ) as response:
                    if not response.ok:
                        error_msg = f"Erro na API de agentes: {response.status} {response.reason}"
                        logger.error(error_msg)
                        return False, AgentResponse(
                            engine="",
                            conversation_id=conversation_id,
                            args={},
                            output=error_msg
                        )
                    
                    args = {}
                    handshake = {}
                    content_parts = []
                    
                    async for chunk in response.content.iter_chunks():
                        if chunk[0]:
                            text_chunk = chunk[0].decode('utf-8')

                            # Processar handshake (primeira mensagem com metadados)
                            if "engine" in text_chunk and "conversation_id" in text_chunk:
                                try:
                                    handshake = json.loads(text_chunk)
                                    continue
                                except json.JSONDecodeError:
                                    logger.error(f"Erro ao decodificar handshake: {text_chunk}")
                                    continue

                            # Processar chunks JSON para o operador
                            if handshake.get("engine") == AgentEngine.operator.value:
                                try:
                                    chunk_json = json.loads(text_chunk)
                                    args.update(chunk_json)
                                    text_chunk = chunk_json.get("output", "")
                                except json.JSONDecodeError:
                                    # Se não for JSON válido, trata como texto normal
                                    pass
                            
                            content_parts.append(text_chunk)
                            
                            # Callback opcional para chunks individuais
                            if on_chunk:
                                chunk_response = AgentResponse(
                                    engine=handshake.get("engine", ""),
                                    conversation_id=handshake.get("conversation_id", conversation_id),
                                    args=args,
                                    output=text_chunk
                                )
                                on_chunk(text_chunk, chunk_response)

                    # Montar resposta final completa
                    full_content = ''.join(content_parts)
                    
                    return True, AgentResponse(
                        engine=handshake.get("engine", ""),
                        conversation_id=handshake.get("conversation_id", conversation_id),
                        args=args,
                        output=full_content
                    )
        
        except Exception as e:
            error_msg = f"Erro ao chamar API de agentes: {str(e)}"
            logger.error(error_msg)
            return False, AgentResponse(
                engine="",
                conversation_id=conversation_id,
                args={},
                output=error_msg
            )

