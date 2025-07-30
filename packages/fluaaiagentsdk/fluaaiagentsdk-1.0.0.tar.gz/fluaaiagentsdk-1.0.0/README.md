# SDK de Agentes Fluaai

SDK em Python para interagir com a API de Agentes da Fluaai, oferecendo integração simples com LLMs e operadores, suporte a streaming, e respostas estruturadas em classes tipadas.

## Instalação

```bash
pip install fluaai-agent-sdk
```

## Funcionalidades

- Invocação de agentes LLM e Operador
- Streaming em tempo real de respostas
- Tratamento consistente de diferentes engines
- Respostas tipadas com classes ou compatíveis com JSON
- Suporte a ferramentas e processamento de conversas

## Uso Básico

### Exemplo Simples

```python
import asyncio
from agent import Agent, StreamMode

async def main():
    # Invocar um agente e receber a resposta completa
    success, response = await Agent.agent_invoke(
        prompt="Olá, me fale sobre o Brasil",
        agent_id="seu_agent_id",
        api_key="sua_chave_api_key",
        stream_mode=StreamMode.DISABLED
    )
    
    if success:
        # Acesso como objeto tipado
        print(f"Engine: {response.engine}")
        print(f"Resposta: {response.output}")
        
        # Acesso como dicionário (compatibilidade)
        print(f"Engine: {response['engine']}")
        print(f"Resposta: {response['output']}")
        
        # Conversão para JSON
        json_str = response.to_json()
        print(f"JSON: {json_str[:100]}...")
    else:
        print(f"Erro: {response.output}")

asyncio.run(main())
```

### Streaming em Tempo Real

```python
import asyncio
from agent import Agent, StreamMode

async def main():
    # Receber resposta em tempo real via streaming
    async for success, chunk in Agent.agent_invoke(
        prompt="Gere uma imagem de montanhas",
        agent_id="seu_agent_id",
        api_key="sua_chave_api_key",
        stream_mode=StreamMode.ENABLED
    ):
        if success:
            # Acessar como objeto
            print(chunk.output, end="", flush=True)
            
            # Para agentes Operador, verificar status
            if chunk.engine == "operator" and chunk.status:
                if chunk.status == "completed":
                    print(f"\n[Tarefa concluída]")
                    print(f"URL ao vivo: {chunk.live_url}")
                    print(f"URL's das ações: {chunk.screenshots}")
        else:
            print(f"\nErro: {chunk.output}")

asyncio.run(main())
```

## Estrutura de Respostas

O SDK retorna respostas como objetos estruturados da classe `AgentResponse`:

### Classe AgentResponse

**Atributos principais:**
- `engine`: Engine do agente ("llm" ou "operator")
- `conversation_id`: ID da conversa
- `output`: Conteúdo da resposta

**Atributos para engine operator:**
- `task_id`: ID da tarefa do operador
- `live_url`: URL para visualizar a execução em tempo real
- `status`: Status da tarefa ("running", "completed", "failed")
- `screenshots`: Lista de URLs de screenshots das ações

**Métodos:**
- `to_dict()`: Converte para dicionário Python
- `to_json()`: Converte para string JSON
- `from_dict(data)`: Cria objeto a partir de dicionário
- `from_json(json_str)`: Cria objeto a partir de JSON

### Classe Message

**Atributos:**
- `role`: Papel da mensagem ("system", "user", "assistant", "tool")
- `content`: Conteúdo da mensagem
- `tool_calls`: Lista de chamadas de ferramentas (para assistentes)
- `tool_call_id`: ID da ferramenta (para mensagens de resultado)

## Formatos de Resposta por Engine

### 1. Engine 'llm' (LLM tradicional)

Resposta sem streaming:
```python
AgentResponse(
    engine="llm",
    output="Conteúdo completo da resposta do modelo de linguagem...",
)
```

### 2. Engine 'operator' (Operador)

Resposta sem streaming:
```python
AgentResponse(
    engine="operator",
    output="Resultado completo da tarefa do operador...",
    task_id="661d49e4-aada-4d90-abc7-baba34a7b762",
    live_url="https://live.anchorbrowser.io?sessionId=98e2dd75-33d6-44ab-9e4f-9298e8817cc5",
    status="completed",
    screenshots=[...]  # URLs de screenshots
)
```

## Trabalhando com Ferramentas

```python
success, response = await Agent.agent_invoke(...)
```

## Compatibilidade com Código Existente

Todo código que utilizava o formato de dicionário continuará funcionando:

```python
# Código existente continua compatível
success, response = await Agent.agent_invoke(...)
if success:
    output = response["output"]
    engine = response["engine"]
    
    if engine == "operator":
        status = response["args"]["status"]
        live_url = response["args"]["live_url"]
```