# First Agent with MCP

Projeto de estudo que demonstra como conectar um agente de IA criado com **Python**, **LangChain** e **Claude (Anthropic)** a um servidor **MCP (Model Context Protocol)** para descobrir e utilizar ferramentas matemáticas.

Diferente do projeto anterior, em que as ferramentas eram definidas diretamente no agente, aqui elas ficam em um servidor MCP separado. O agente consulta esse servidor e usa as ferramentas disponíveis conforme a pergunta do usuário.

## Como funciona

O projeto possui dois componentes principais:

- `first-agent-with-mcp.py`: inicializa o modelo Claude, conecta-se ao servidor MCP, descobre as ferramentas e cria o agente.
- `mcp-math-server.py`: implementa um servidor MCP que disponibiliza ferramentas matemáticas.

A comunicação entre o agente e o servidor utiliza o transporte `stdio`. O próprio agente inicia o processo do servidor, então não é necessário abrir o servidor manualmente em outro terminal.

## Requisitos

- Python 3.10 ou superior
- Git
- Uma chave de API da Anthropic
- Faturamento/créditos habilitados no Anthropic Console para realizar chamadas à API

> A assinatura do Claude em claude.ai e o uso da Claude API são serviços separados. Consulte o [Anthropic Console](https://console.anthropic.com/) para criar a chave e configurar o faturamento. Os custos dependem do modelo e do uso; veja os [preços da API](https://docs.anthropic.com/en/docs/about-claude/pricing).

## 1. Clone o repositório

```bash
git clone https://github.com/kleitonfr/first-agent-with-mcp.git
cd first-agent-with-mcp
```

## 2. Crie e ative um ambiente virtual

### Windows — PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Se estiver usando o Prompt de Comando (cmd.exe):

```bat
.venv\Scripts\activate.bat
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Instale as dependências

Com o ambiente virtual ativado, execute:

```bash
python -m pip install --upgrade pip
pip install -U "langchain[anthropic]" langgraph langchain-mcp-adapters mcp python-dotenv
```

## 4. Crie uma chave da Claude API e adicione créditos

1. Acesse o [Anthropic Console](https://console.anthropic.com/).
2. Crie uma API key.
3. Configure o faturamento e adicione créditos de uso à organização, se necessário.

Sem faturamento habilitado ou saldo disponível, as chamadas à API podem falhar.

## 5. Configure a variável de ambiente

Na raiz do repositório, crie um arquivo chamado `.env` com o conteúdo:

```env
ANTHROPIC_API_KEY=sua_chave_aqui
```

Troque `sua_chave_aqui` pela sua chave real. O arquivo `.env` já está no `.gitignore`.

**Nunca compartilhe sua chave nem faça commit do arquivo `.env`.** Se a chave for exposta, revogue-a no Console e gere outra.

## 6. Execute o agente

Com o ambiente virtual ativado e o arquivo `.env` configurado, execute:

```bash
python first-agent-with-mcp.py
```

O script inicia automaticamente `mcp-math-server.py`, descobre as ferramentas expostas pelo servidor e executa algumas perguntas de exemplo, incluindo:

- Quanto é 2 + 2?
- Quanto é 15 multiplicado por 8, então dividido por 3?
- Quanto é 100 dividido por 0?

## Ferramentas matemáticas disponíveis

O servidor MCP disponibiliza estas ferramentas:

| Ferramenta | Finalidade |
|---|---|
| `add(a, b)` | Soma dois números |
| `subtract(a, b)` | Subtrai o segundo número do primeiro |
| `multiply(a, b)` | Multiplica dois números |
| `divide(a, b)` | Divide dois números e retorna uma mensagem de erro para divisão por zero |
| `square_root(a)` | Calcula a raiz quadrada de um número não negativo |

O Claude interpreta cada pergunta e decide quais ferramentas utilizar. Por exemplo, uma pergunta que envolva multiplicação e depois divisão pode levar o agente a chamar mais de uma ferramenta.

## Estrutura do projeto

```text
first-agent-with-mcp/
├── .gitignore
├── README.md
├── image.png
├── first-agent-with-mcp.py
└── mcp-math-server.py
```

## O que este projeto demonstra

- **MCP (Model Context Protocol):** uma forma padronizada de disponibilizar ferramentas para aplicações de IA.
- **MCP server:** expõe ferramentas matemáticas com `FastMCP`.
- **MCP client:** conecta-se ao servidor e descobre as ferramentas disponíveis.
- **Agente com ferramentas:** o LangChain permite que o modelo selecione e invoque ferramentas para responder às perguntas.
- **Execução assíncrona:** o cliente usa `asyncio` para trabalhar com a comunicação MCP.

## Tecnologias

- [Python](https://www.python.org/)
- [LangChain](https://www.langchain.com/)
- [LangGraph](https://www.langchain.com/langgraph)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
