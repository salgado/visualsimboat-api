
"""
MCP FastMCP server para VisualSimBoat
Expondo tools, resources e prompts.
"""
from fastmcp import MCP, Tool, Resource, Prompt, tool, resource, prompt
from visualsimboat_api import VisualSimBoatAPI
import asyncio

mcp = MCP(title="VisualSimBoat MCP", description="Controle remoto do barco simulado via VisualSimBoatAPI")

# Inicialização do VisualSimBoatAPI
@mcp.on_startup
async def startup(ctx):
    ctx.api = VisualSimBoatAPI()
    await ctx.api.__aenter__()
    connected = await ctx.api.connect()
    if not connected:
        raise RuntimeError("Não foi possível conectar ao VisualSimBoat.")

@mcp.on_shutdown
async def shutdown(ctx):
    await ctx.api.__aexit__(None, None, None)

# TOOLS
@tool("engine_start", description="Liga o motor do barco.")
async def engine_start(ctx):
    ok = await ctx.api.engine_start()
    return {"status": "ok" if ok else "fail"}

@tool("engine_stop", description="Desliga o motor do barco.")
async def engine_stop(ctx):
    ok = await ctx.api.engine_stop()
    return {"status": "ok" if ok else "fail"}

@tool("set_throttle", description="Define a aceleração do barco (0-100)")
async def set_throttle(ctx, value: int):
    ok = await ctx.api.set_throttle(value)
    return {"status": "ok" if ok else "fail"}

@tool("set_steering", description="Define o leme do barco (-100 a 100)")
async def set_steering(ctx, value: int):
    ok = await ctx.api.set_steering(value)
    return {"status": "ok" if ok else "fail"}

@tool("emergency_stop", description="Parada de emergência: zera aceleração e leme.")
async def emergency_stop(ctx):
    await ctx.api.emergency_stop()
    return {"status": "ok"}

@tool("get_gps", description="Obtém a posição GPS atual do barco.")
async def get_gps(ctx):
    gps = await ctx.api.get_gps()
    return gps or {"status": "fail"}

@tool("get_camera_image", description="Obtém imagem de uma câmera. IDs: front, starboard, aft, port.")
async def get_camera_image(ctx, camera_id: str = "front"):
    img = await ctx.api.get_camera_image(camera_id)
    if img:
        return {"image": img.hex()}
    return {"status": "fail"}

# RESOURCES
@resource("boat_status", description="Status resumido do barco (GPS, motor ligado)")
async def boat_status(ctx):
    gps = await ctx.api.get_gps()
    info = await ctx.api.get_info()
    return {"gps": gps, "info": info}

# PROMPTS
@prompt("navegar_para", description="Prompt para navegar até uma coordenada GPS.")
async def navegar_para(ctx, lat: float, lon: float):
    # Exemplo: apenas retorna o destino
    return {"destino": {"lat": lat, "lon": lon}, "mensagem": "Função de navegação não implementada."}

app = mcp.app
