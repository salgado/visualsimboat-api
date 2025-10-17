"""
MCP FastMCP server para VisualSimBoat
Controle do simulador marítimo via MCP.
"""
import sys
sys.path.append('..')
from visualsimboat_api import VisualSimBoatAPI
from mcp.server.fastmcp import FastMCP
import base64
import json

# Criar servidor MCP
mcp = FastMCP("VisualSimBoat")

# Instância global da API
api = None

async def get_api():
    """Inicializa e retorna a instância da API VisualSimBoat."""
    global api
    if api is None:
        api = VisualSimBoatAPI()
        await api.__aenter__()
        connected = await api.connect()
        if not connected:
            raise RuntimeError("Não foi possível conectar ao VisualSimBoat.")
    return api

@mcp.tool()
async def engine_start() -> str:
    """Liga o motor do barco."""
    api_instance = await get_api()
    ok = await api_instance.engine_start()
    return "Motor ligado com sucesso" if ok else "Falha ao ligar motor"

@mcp.tool()
async def engine_stop() -> str:
    """Desliga o motor do barco."""
    api_instance = await get_api()
    ok = await api_instance.engine_stop()
    return "Motor desligado com sucesso" if ok else "Falha ao desligar motor"

@mcp.tool()
async def set_throttle(value: int) -> str:
    """Define a aceleração do barco.

    Args:
        value: Valor da aceleração (0-100)
    """
    api_instance = await get_api()
    ok = await api_instance.set_throttle(value)
    return f"Aceleração definida para {value}%" if ok else "Falha ao definir aceleração"

@mcp.tool()
async def set_steering(value: int) -> str:
    """Define o leme do barco.

    Args:
        value: Valor do leme (-100 a 100)
    """
    api_instance = await get_api()
    ok = await api_instance.set_steering(value)
    return f"Leme definido para {value}" if ok else "Falha ao definir leme"

@mcp.tool()
async def emergency_stop() -> str:
    """Parada de emergência: zera aceleração e leme."""
    api_instance = await get_api()
    await api_instance.emergency_stop()
    return "Parada de emergência executada com sucesso"

@mcp.tool()
async def get_gps() -> str:
    """Obtém a posição GPS atual do barco."""
    api_instance = await get_api()
    gps = await api_instance.get_gps()
    if gps:
        return f"GPS: Latitude {gps['lat']:.6f}, Longitude {gps['lon']:.6f}"
    return "Falha ao obter coordenadas GPS"

@mcp.tool()
async def get_camera_image(camera_id: str = "front") -> str:
    """Obtém imagem de uma câmera.

    Args:
        camera_id: ID da câmera (front, starboard, aft, port)
    """
    api_instance = await get_api()
    img = await api_instance.get_camera_image(camera_id)
    if img:
        return f"Imagem capturada da câmera {camera_id} ({len(img)} bytes)"
    return f"Falha ao capturar imagem da câmera {camera_id}"

@mcp.tool()
async def get_all_cameras() -> str:
    """Captura imagens de todas as câmeras e retorna JSON com base64.

    Retorna JSON com estrutura:
    {
        "front": "base64_data",
        "starboard": "base64_data",
        "aft": "base64_data",
        "port": "base64_data"
    }
    """
    api_instance = await get_api()
    images = await api_instance.get_all_camera()

    if not images:
        return json.dumps({"error": "Falha ao capturar imagens das câmeras"})

    result = {}
    for camera_id, img_data in images.items():
        result[camera_id] = base64.b64encode(img_data).decode('utf-8')

    return json.dumps(result)

@mcp.tool()
async def gear_1() -> str:
    """Seleciona marcha 1."""
    api_instance = await get_api()
    ok = await api_instance.gear_1()
    return "Marcha 1 selecionada" if ok else "Falha ao selecionar marcha 1"

@mcp.tool()
async def gear_2() -> str:
    """Seleciona marcha 2."""
    api_instance = await get_api()
    ok = await api_instance.gear_2()
    return "Marcha 2 selecionada" if ok else "Falha ao selecionar marcha 2"

@mcp.tool()
async def gear_3() -> str:
    """Seleciona marcha 3."""
    api_instance = await get_api()
    ok = await api_instance.gear_3()
    return "Marcha 3 selecionada" if ok else "Falha ao selecionar marcha 3"

if __name__ == "__main__":
    mcp.run(transport='stdio')