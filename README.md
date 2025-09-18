# visualsimboat-api

API Python assíncrona para controle remoto e percepção de um barco simulado via VisualSimBoat.

## Instalação

Requisitos:
- Python 3.8+
- httpx

Instale as dependências:
```bash
pip install httpx
```

## Uso Básico

```python
import asyncio
from visualsimboat_api import VisualSimBoatAPI

async def main():
	async with VisualSimBoatAPI(host="localhost", port=30010) as api:
		conectado = await api.connect()
		if not conectado:
			print("Falha na conexão!")
			return
		await api.engine_start()
		await api.set_throttle(50)  # 50% de aceleração
		await api.set_steering(20)  # leme para a direita
		gps = await api.get_gps()
		print("GPS:", gps)
		img = await api.get_camera_image("front")
		if img:
			with open("camera_front.png", "wb") as f:
				f.write(img)
		await api.emergency_stop()

asyncio.run(main())
```

## Principais Métodos

### Conexão e Utilidades
- `connect()`: Testa conexão com o simulador.
- `emergency_stop()`: Para imediatamente o barco (zera aceleração e leme).

### Motor e Engrenagem
- `engine_start()`: Liga o motor.
- `engine_stop()`: Desliga o motor.
- `gear_1()`, `gear_2()`, `gear_3()`: Seleciona a marcha.
- `accelerate()`: Acelera.

### Movimento
- `set_throttle(value)`: Define aceleração (0-100).
- `set_steering(value)`: Define leme (-100 a 100).

### Sensores
- `get_gps()`: Retorna latitude/longitude.
- `get_info()`: Retorna informações do simulador.
- `get_camera_image(camera_id)`: Retorna imagem de uma câmera (`front`, `starboard`, `aft`, `port`).
- `get_all_camera()`: Retorna imagens de todas as câmeras.

## Observações
- As funções são assíncronas (use `await`).
- Imagens são salvas temporariamente em `/tmp/visualsimboat`.
- O simulador deve estar rodando e acessível via HTTP.

---
Desenvolvido por salgado