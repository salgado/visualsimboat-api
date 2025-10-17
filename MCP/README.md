# VisualSimBoat MCP Server

Servidor MCP (Model Context Protocol) para controlar o simulador VisualSimBoat através do Claude Desktop.

## Instalação no Claude Desktop

### 1. Instalar uv e dependências

```bash
# Instalar uv se necessário
curl -LsSf https://astral.sh/uv/install.sh | sh

# No diretório MCP, criar ambiente virtual e instalar dependências
cd /Users/alexsalgado/Desktop/uff/planejamento-tese/codigos/visualsimboat-api/MCP
uv venv
uv add "mcp[cli]" httpx
```

### 2. Configurar no Claude Desktop

Adicione ao arquivo de configuração do Claude Desktop (`claude_desktop_config.json`):

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

### 3. Localização do arquivo de configuração

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/claude/claude_desktop_config.json`

## Pré-requisitos

1. **VisualSimBoat** deve estar rodando em `localhost:30010`
2. Python 3.8+ instalado
3. Dependências: `fastmcp` e `httpx`

## Tools disponíveis

- `engine_start` - Liga o motor
- `engine_stop` - Desliga o motor
- `set_throttle` - Define aceleração (0-100)
- `set_steering` - Define leme (-100 a 100)
- `emergency_stop` - Parada de emergência
- `get_gps` - Obtém posição GPS
- `get_camera_image` - Captura imagem de câmera

## Recursos (Resources)

- `boat_status` - Status completo do barco (GPS + info)

## Prompts

- `navegar_para` - Template para navegação até coordenadas GPS

## Testando o servidor

```bash
# No diretório MCP
python3 -m fastmcp main:app

# Ou usando o script
./run.sh
```

O servidor irá iniciar e tentar conectar ao VisualSimBoat automaticamente.