#!/bin/bash
# Script para executar o servidor MCP do VisualSimBoat com uv

cd "$(dirname "$0")"
/Users/alexsalgado/.local/bin/uv run --python 3.12 python -m fastmcp main:app