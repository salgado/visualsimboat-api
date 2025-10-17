# Servidor MCP VisualSimBoat - Setup Completo

## Resumo do que foi feito

Criamos um servidor MCP (Model Context Protocol) funcional para controlar o simulador VisualSimBoat através do Claude Desktop.

## Estrutura do projeto

```
visualsimboat-api/
├── MCP/
│   ├── visualsimboat.py     # Servidor MCP principal
│   ├── pyproject.toml       # Configuração do projeto uv
│   ├── .venv/              # Ambiente virtual criado pelo uv
│   ├── requirements.txt     # Dependências (fastmcp, httpx)
│   ├── run.sh              # Script de execução
│   └── README.md           # Documentação
├── visualsimboat_api.py    # API Python para VisualSimBoat
├── CLAUDE.md              # Instruções para Claude Code
└── README.md              # Documentação principal
```

## Para restaurar após reset da máquina

### 1. Verificar se uv está instalado
```bash
which uv
# Se não estiver instalado:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Navegar para o diretório MCP
```bash
cd /Users/alexsalgado/Desktop/uff/planejamento-tese/codigos/visualsimboat-api/MCP
```

### 3. Reinstalar dependências
```bash
# O ambiente virtual já existe, mas pode precisar recriar
uv venv  # Se necessário
uv add "mcp[cli]" httpx
```

### 4. Testar o servidor
```bash
uv run visualsimboat.py
```
Deve executar sem erros (não mostra output, mas não deve dar erro).

### 5. Configurar no Claude Desktop

Arquivo: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "visualsimboat": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/alexsalgado/Desktop/uff/planejamento-tese/codigos/visualsimboat-api/MCP",
        "run",
        "visualsimboat.py"
      ]
    }
  }
}
```

### 6. Reiniciar Claude Desktop

## Tools disponíveis no servidor MCP

O servidor expõe 9 ferramentas para controle do VisualSimBoat:

1. **engine_start** - Liga o motor do barco
2. **engine_stop** - Desliga o motor do barco
3. **set_throttle(value: int)** - Define aceleração (0-100)
4. **set_steering(value: int)** - Define leme (-100 a 100)
5. **emergency_stop** - Parada de emergência
6. **get_gps** - Obtém posição GPS atual
7. **get_camera_image(camera_id: str)** - Captura imagem (front/port/starboard/aft)
8. **gear_1** - Seleciona marcha 1
9. **gear_2** - Seleciona marcha 2
10. **gear_3** - Seleciona marcha 3

## Arquivos importantes

### visualsimboat.py (servidor MCP)
- Implementa FastMCP seguindo a documentação oficial
- Inicializa API VisualSimBoat sob demanda
- Todas as tools são async e retornam strings descritivas

### pyproject.toml
- Configuração uv com Python >=3.10
- Dependências: mcp[cli], httpx

### Configuração Claude Desktop
- Usa `uv --directory` para executar no diretório correto
- Executa `visualsimboat.py` diretamente

## Problemas resolvidos

1. **Sintaxe FastMCP**: Migrou de `fastmcp` para `mcp.server.fastmcp`
2. **Lifecycle**: Removeu `@mcp.on_startup`/`@mcp.on_shutdown` e implementou lazy loading
3. **Execução**: Usa `mcp.run(transport='stdio')` seguindo a documentação
4. **uv**: Configurado para funcionar com o formato `uv --directory ... run script.py`
5. **Python version**: Ajustado para >=3.10 (requerido pelo mcp[cli])

## Validação

Para verificar se está funcionando:
1. `uv run visualsimboat.py` não deve dar erro
2. No Claude Desktop, deve aparecer o ícone de tools
3. Deve listar as 9 ferramentas VisualSimBoat

## Dependências do sistema

- **uv**: Gerenciador de pacotes Python
- **Python 3.10+**: Requerido pelo mcp[cli]
- **VisualSimBoat**: Deve estar rodando em localhost:30010

## Notas importantes

- O servidor MCP conecta automaticamente ao VisualSimBoat na primeira chamada de tool
- Se VisualSimBoat não estiver rodando, as tools retornarão erro
- Todas as images de câmera são salvas em `/tmp/visualsimboat/`
- O servidor é stateless - cada tool call reconecta se necessário