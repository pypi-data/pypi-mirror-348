"""
Funções auxiliares para analisar respostas dos agentes.
"""
import re
from typing import List

from ..agent import Message


def extract_llm_final_response(output: str) -> str:
    """
    Extrai apenas a resposta final do LLM, removendo as partes de execução de ferramentas.
    
    Args:
        output: A saída completa do agente, incluindo chamadas de ferramentas
        
    Returns:
        A resposta final do LLM sem os marcadores de ferramentas
    """
    # Padrão para encontrar a última parte da resposta após a última chamada de ferramenta
    tool_pattern = r'__END_TOOL_RESULT__(.*?)$'
    match = re.search(tool_pattern, output, re.DOTALL)
    
    if match:
        # Se encontrou uma chamada de ferramenta, retorna o texto após a última ocorrência
        return match.group(1).strip()
    else:
        # Se não encontrou chamadas de ferramentas, retorna a mensagem original
        return output.strip()


def parse_agent_conversation(output: str) -> List[Message]:
    """
    Analisa a saída do agente e converte em uma lista de mensagens estruturadas.
    
    Args:
        output: A saída completa do agente
        
    Returns:
        Uma lista de objetos Message representando a conversa
    """
    messages = []
    
    # Extrair chamadas de ferramentas
    tool_calls_pattern = r'__EXECUTING_TOOL__(.*?)__END_EXECUTING_TOOL__'
    tool_results_pattern = r'__TOOL_RESULT__(.*?)__END_TOOL_RESULT__'
    
    # Encontrar todas as chamadas de ferramentas e seus resultados
    tool_calls = re.findall(tool_calls_pattern, output, re.DOTALL)
    tool_results = re.findall(tool_results_pattern, output, re.DOTALL)
    
    # Saída final do LLM (após a última chamada de ferramenta)
    final_response = extract_llm_final_response(output)
    
    # Mensagem inicial do assistente (pode ser vazia se ele começar com uma ferramenta)
    initial_text = output
    for pattern in [tool_calls_pattern, tool_results_pattern]:
        matches = re.findall(pattern, output, re.DOTALL)
        for match in matches:
            initial_text = initial_text.replace(f"__{pattern.split('__')[1]}__{match}__END_{pattern.split('__')[1]}__", "", 1)
    
    initial_text = initial_text.replace(final_response, "").strip()
    
    if initial_text:
        # Se houver texto inicial antes da primeira chamada de ferramenta
        messages.append(Message(role="assistant", content=initial_text))
    
    # Adicionar todas as chamadas de ferramentas e seus resultados
    for i in range(len(tool_calls)):
        try:
            tool_call_data = eval(tool_calls[i])  # Converte o JSON para dicionário
            tool_result_data = eval(tool_results[i])  # Converte o JSON para dicionário
            
            # Adicionar a chamada da ferramenta
            messages.append(Message(
                role="assistant", 
                content="", 
                tool_calls=[tool_call_data]
            ))
            
            # Adicionar o resultado da ferramenta
            messages.append(Message(
                role="tool", 
                content="",
                tool_responses=[tool_result_data]
            ))
        except (SyntaxError, ValueError) as e:
            # Em caso de erro ao processar o JSON
            print(f"Erro ao processar chamada de ferramenta: {e}")
    
    # Adicionar a resposta final do LLM
    if final_response:
        messages.append(Message(role="assistant", content=final_response))
    
    return messages