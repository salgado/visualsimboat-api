# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python API client for controlling the VisualSimBoat maritime simulator. The project provides an async HTTP client that interfaces with VisualSimBoat's REST API to control boat navigation, engine operations, and sensor data collection.

## Architecture

### Core Components

- `VisualSimBoatAPI` class: Main async client that manages HTTP communication with the simulator
- Uses httpx for async HTTP requests with 5-second timeouts
- Default connection to `localhost:30010/remote/preset/RC_BoatControl/function/`
- All control functions are async and return success/failure status or data

### Key Control Categories

1. **Engine Control**: Start/stop engine operations
2. **Navigation**: Throttle (0-100%), steering (-100 to 100), gear selection (1-3)
3. **Sensors**: GPS positioning, camera capture from multiple viewpoints
4. **Safety**: Emergency stop functionality that resets all controls

## Development Commands

### Running Tests
```bash
python test_api.py
```
The test suite includes:
- Connection verification
- Individual component testing (engine, throttle, steering, gears, GPS, cameras)
- Emergency stop functionality
- Optional interactive navigation sequence test

### Testing Individual Components
The API client can be imported and used directly:
```python
from visualsimboat_api import VisualSimBoatAPI
api = VisualSimBoatAPI(host="localhost", port=30010)
await api.connect()  # Test connection first
```

## API Design Patterns

- All methods are async and require proper async context management
- Methods return `True/False` for success operations or `None/Dict` for data retrieval
- Error handling includes timeout protection and graceful degradation
- The client must be properly closed with `await api.close()`

## Dependencies

- `httpx`: Async HTTP client library
- `asyncio`: For async/await functionality
- No external configuration files - all settings passed via constructor

## Simulator Integration

The API expects VisualSimBoat simulator to be running and accessible. The simulator provides:
- REST API endpoints for boat control
- Camera capture capabilities (front, port, starboard, aft views)
- GPS positioning data
- Engine and navigation control interface

## Testing Philosophy

The test suite is designed for interactive validation with real simulator feedback, including visual confirmation prompts for navigation sequences. Tests are structured to be run against a live simulator instance for comprehensive validation.