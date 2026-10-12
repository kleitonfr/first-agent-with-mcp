"""
MCP MAth Server - O provedor da tool

Esse servidor expoe as ferramentas que podem ser chamadas remotamente.

Qualquer MCP client compatível pode acessar as ferramentas expostas pelo servidor.

"""
from mcp.server.fastmcp import FastMCP
import math

# Criando o MCP Server
mcp = FastMCP("Math")

@mcp.tool()
def add(a: float, b: float) -> float:
    """ Adiciona dois números juntos. Use para operações de adição. """
    return a + b

@mcp.tool()
def subtract(a: float, b: float) -> float:
    """ Subtrai dois números. Use para operações de subtração. """
    return a - b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """ Multiplica dois números. Use para operações de multiplicação. """
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> str:
    """ Divide dois números. Use para operações de divisão. """
    if b == 0:
        return "Error: Não pode dividir por zero"
    return str(a / b)

@mcp.tool()
def square_root(a: float) -> float:
    """ Calcula a raiz quadrada de um número. Use para operações de raiz quadrada. """
    return math.sqrt(a)

if __name__ == "__main__":
    mcp.run(transport="stdio")