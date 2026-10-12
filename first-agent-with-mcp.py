"""
Esse é o mesmo agent do my-first-agent, mas agora, em vez de definir as ferramentas
localmente com @tool, elas serão descobertas a partir de um MCP server em tempo de execução.

Pre-requisitos:

  pip install -qU langchain "langchain[anthropic]"
  pip install -U langgraph
  pip install langchain-mcp-adapters
  pip install mcp 
  pip install python-dotenv
  
setup:

    criar um arquivo .env com a variável de ambiente ANTHROPIC_API_KEY
    
    O outro arquivo onde será configurado o "mcp server" precisa está no mesmo diretório.
    
"""

import os
import asyncio
from dotenv import load_dotenv
import warnings

# uma forma de limpar o terminal. O Warning é um alerta sobre algo que merece atenção, mas não interrompe a execução do programa. Aqui, estamos ignorando os warnings do tipo UserWarning. Geralmente, isso é feito para evitar que mensagens de aviso poluam a saída do terminal, especialmente quando sabemos que esses avisos não são críticos para a execução do código.
warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv()

# STEP 1: Inicialize o modelo

from langchain.chat_models import init_chat_model

model = init_chat_model("claude-sonnet-4-6")


# STEP 2: Define as ferramentas

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

async def main():
    """
    As conexões MCP são assincronas porque elas envolvem I/O (Input/Output com outros servidores).
    """
    # pegar o cmainho absoluto do MECP server script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(current_dir, "mcp-math-server.py")

    client = MultiServerMCPClient(
        {
            "math-mcp-server": {
                "command": "python",
                "args": [server_path],
                "transport": "stdio",
            }
        }
    )

    tools = await client.get_tools()
    
    print("=" * 50)
    print(" MCP Agent - Ferramentas descobertas apartir do MCP Server")
    print("=" * 50)
    print(f"\n Encontrado {len(tools)} ferramentas apartir do MCP Server:\n")
    for t in tools:
        print(f" {t.name}: {t.description}...")
    print()
    
    # STEP 3: Criando o agente
    
    agent = create_agent(
        model,
        tools = tools,
    )
    
    
    # STEP 4: Executando o agente
    
    async def run_agent(question: str):
        print(f" User: {question}")
        print("=" * 50)
        
        result = await agent.ainvoke({
            "messages": [("user", question)],
        })
        
        for msg in result["messages"]:
            if msg.type == "human":
                continue
            elif msg.type == "ai":
                if msg.tool_calls:
                    for tc in msg.tool_calls:
                         print(f"🤖 Agent thinks → calling: {tc['name']}({tc['args']})")
                elif msg.content:
                    print(f" Agent: {msg.content}")
            elif msg.type == "tool":
                content = msg.content
                if isinstance(content, list):
                    texts = [item["text"] for item in content if isinstance(item, dict) and "text" in item]
                    content = ", ".join(texts) if texts else str(content)
                print(f"🔧 Tool result: {content}")

        print("=" * 55)
        print()
    
    
    
    await run_agent("Quanto é 2 + 2?")
    
    await run_agent("Quanto é 15 multiplicado por 8, então dividido por 3?")
    
    # edge cases: 
    await run_agent("Quanto é 100 devidido por 0?")
    
    
    
if __name__ == "__main__":
    asyncio.run(main())