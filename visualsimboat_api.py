# visualsimboat_api.py
import os
import asyncio
import httpx
import json
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class VisualSimBoatAPI:
    def __init__(self, host: str = "localhost", port: int = 30010, timeout: float = 5.0):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}/remote"
        self.preset = "RC_BoatControl"
        self.function_url = f"{self.base_url}/preset/{self.preset}/function"
        self.client: Optional[httpx.AsyncClient] = None
        self.timeout = timeout
        self.temp_dir = "/tmp/visualsimboat"
        self.camera_mapping = {
            "front": "camera1.png",
            "port": "camera2.png",
            "starboard": "camera3.png",
            "aft": "camera4.png"
        }

        # Ensure temp directory exists
        if not os.path.exists(self.temp_dir):
            try:
                os.makedirs(self.temp_dir, exist_ok=True)
                logger.info(f"Created temp directory: {self.temp_dir}")
            except Exception as e:
                logger.error(f"Failed to create temp directory: {e}")

    async def __aenter__(self):
        self.client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()

    async def _call_function(self, function_name: str, parameters: Dict[str, Any] = None) -> Optional[Any]:
        url = f"{self.function_url}/{function_name}"
        payload = {"parameters": parameters or {}}
        try:
            response = await self.client.put(url, json=payload)
            if response.status_code == 200:
                return response.json()
            logger.error(f"HTTP {response.status_code} on {function_name}: {response.text}")
            return None
        except Exception as e:
            logger.error(f"API call failed: {function_name} | Error: {e}")
            return None

    # ========================
    # ⚙️ ENGINE & GEAR CONTROL
    # ========================

    async def engine_start(self) -> bool:
        result = await self._call_function("engine_start")
        return isinstance(result, dict) and "ReturnedValues" in result

    async def engine_stop(self) -> bool:
        result = await self._call_function("engine_stop")
        return isinstance(result, dict) and "ReturnedValues" in result

    async def gear_1(self) -> bool:
        result = await self._call_function("gear_1")
        return isinstance(result, dict) and "ReturnedValues" in result

    async def gear_2(self) -> bool:
        result = await self._call_function("gear_2")
        return isinstance(result, dict) and "ReturnedValues" in result

    async def gear_3(self) -> bool:
        result = await self._call_function("gear_3")
        return isinstance(result, dict) and "ReturnedValues" in result

    async def accelerate(self) -> bool:
        result = await self._call_function("accelerate")
        return isinstance(result, dict) and "ReturnedValues" in result

    # ========================
    # 🛠️ MOVEMENT CONTROL
    # ========================

    async def set_throttle(self, value: int) -> bool:
        value = max(0, min(100, value))
        result = await self._call_function("set_throttle", {"Value": value})
        success = isinstance(result, dict) and "ReturnedValues" in result
        if success:
            logger.info(f"Throttle set to {value}%")
        return success

    async def set_steering(self, value: int) -> bool:
        value = max(-100, min(100, value))
        result = await self._call_function("set_steering", {"Value": value})
        success = isinstance(result, dict) and "ReturnedValues" in result
        if success:
            logger.info(f"Steering set to {value}")
        return success

    # ========================
    # 📍 SENSORS & PERCEPTION
    # ========================

    async def get_gps(self) -> Optional[Dict[str, float]]:
        result = await self._call_function("get_GPS")
        if not result or not isinstance(result, dict):
            return None

        try:
            if "ReturnedValues" in result and len(result["ReturnedValues"]) > 0:
                coords_str = result["ReturnedValues"][0].get("Coordinates")
                if coords_str and isinstance(coords_str, str):
                    coords = json.loads(coords_str)
                    lat = float(coords.get("lat", 0.0))
                    lon = float(coords.get("long", 0.0))
                    return {"lat": lat, "lon": lon, "alt": 0.0}
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Failed to parse GPS response: {e} | Raw: {result}")
        return None

    async def get_info(self) -> Optional[Dict[str, Any]]:
        # Known issue: may return error due to preset
        result = await self._call_function("get_info")
        if isinstance(result, dict) and "errorMessage" not in result:
            return result
        return None

    async def get_camera_image(self, camera_id: str = "front") -> Optional[bytes]:
        filename = self.camera_mapping.get(camera_id)
        if not filename:
            logger.warning(f"Unknown camera ID: {camera_id}")
            return None

        filepath = os.path.join(self.temp_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)  # Remove old image

        result = await self._call_function("get_camera_image", {"CameraID": camera_id})
        if not result:
            return None

        await asyncio.sleep(0.5)  # Wait for save

        if os.path.exists(filepath):
            try:
                with open(filepath, "rb") as f:
                    logger.info(f"Loaded image: {filepath}")
                    return f.read()
            except Exception as e:
                logger.error(f"Failed to read {filepath}: {e}")
        else:
            logger.warning(f"Image not found: {filepath}")
        return None

    async def get_all_camera(self) -> Optional[Dict[str, bytes]]:
        # Remove old images
        for filename in self.camera_mapping.values():
            filepath = os.path.join(self.temp_dir, filename)
            if os.path.exists(filepath):
                os.remove(filepath)

        result = await self._call_function("get_all_camera")
        if not result:
            return None

        await asyncio.sleep(0.5)  # Wait for save

        images = {}
        for cam_id, filename in self.camera_mapping.items():
            filepath = os.path.join(self.temp_dir, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, "rb") as f:
                        images[cam_id] = f.read()
                    logger.info(f"Loaded: {filepath}")
                except Exception as e:
                    logger.warning(f"Failed to read {filepath}: {e}")
            else:
                logger.warning(f"Image not found: {filepath}")

        return images if images else None

    # ========================
    # 🔄 UTILITIES
    # ========================

    async def emergency_stop(self) -> bool:
        await self.set_throttle(0)
        await self.set_steering(0)
        logger.warning("Emergency stop: throttle=0, steering=0")
        return True

    async def connect(self) -> bool:
        gps = await self.get_gps()
        connected = gps is not None
        if connected:
            logger.info("Connected to VisualSimBoat.")
        else:
            logger.error("Failed to connect.")
        return connected