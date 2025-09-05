#!/bin/bash
# test_api.sh
# Testa métodos individuais da API do VisualSimBoat com base em um número
# Uso: ./test_api.sh <número>
# Ex: ./test_api.sh 5

URL="http://localhost:30010/remote/preset/RC_BoatControl/function"
TMP_DIR="/tmp/visualsimboat"

# Função para mostrar o menu
show_menu() {
    echo "📌 VisualSimBoat API - Teste Individual por Número"
    echo "🚀 Escolha uma opção:"
    echo
    echo " 1. Iniciar motor (engine_start)"
    echo " 2. Parar motor (engine_stop)"
    echo " 3. Definir aceleração 50% (set_throttle)"
    echo " 4. Virar para a direita (set_steering +30)"
    echo " 5. Virar para a esquerda (set_steering -30)"
    echo " 6. Centralizar direção (set_steering 0)"
    echo " 7. Acelerar (accelerate)"
    echo " 8. Marcha 1 (gear_1)"
    echo " 9. Marcha 2 (gear_2)"
    echo "10. Marcha 3 (gear_3)"
    echo "11. Obter GPS (get_GPS)"
    echo "12. Obter informações do simulador (get_info)"
    echo "13. Capturar câmera frontal (get_camera_image)"
    echo "14. Capturar todas as câmeras (get_all_camera)"
    echo
    echo "0.  Mostrar este menu"
    echo "❌ Qualquer outro número: Sair"
    echo
}

# Função para chamar PUT e mostrar resposta com tratamento seguro de JSON
call_api() {
    local endpoint="$1"
    local data="$2"
    local response_file=$(mktemp)

    echo "🔹 Chamando: $endpoint"
    echo "   💾 Payload: $data"

    if curl -s -X PUT "$URL/$endpoint" \
         -H "Content-Type: application/json" \
         -d "$data" \
         -o "$response_file" && [ -s "$response_file" ]; then

        if python3 -c "import json, sys; json.dump(json.load(open('$response_file')), sys.stdout, indent=2)" 2>/dev/null > /tmp/json_ok.tmp 2>/dev/null; then
            echo "   📤 Resposta (JSON):"
            sed 's/^/   📤 /' /tmp/json_ok.tmp
            rm -f /tmp/json_ok.tmp
        else
            echo "   📤 Resposta (raw):"
            cat "$response_file" | sed 's/^/   📤 /'
        fi
    else
        echo "   📤 Erro: Falha na requisição ou resposta vazia"
    fi

    rm -f "$response_file"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Função para verificar imagens após captura
check_images() {
    echo "🔍 Verificando imagens salvas em $TMP_DIR"
    if [ -d "$TMP_DIR" ]; then
        if [ -n "$(ls "$TMP_DIR"/*.jpg 2>/dev/null)" ]; then
            echo "✅ Arquivos encontrados:"
            ls -la "$TMP_DIR"/*.jpg | while read line; do
                echo "   📄 $line"
            done
        else
            echo "❌ Nenhum arquivo .jpg encontrado em $TMP_DIR"
        fi
    else
        echo "❌ Diretório não existe: $TMP_DIR"
        echo "💡 Certifique-se de que o VisualSimBoat está configurado para salvar em /tmp/visualsimboat"
    fi
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# ========================
# EXECUÇÃO PRINCIPAL
# ========================

if [ $# -eq 0 ]; then
    show_menu
    exit 0
fi

case "$1" in
    0)
        show_menu
        ;;
    1)
        call_api "engine_start" '{"parameters": {}}'
        ;;
    2)
        call_api "engine_stop" '{"parameters": {}}'
        ;;
    3)
        call_api "set_throttle" '{"parameters": {"Value": 50}}'
        ;;
    4)
        call_api "set_steering" '{"parameters": {"Value": 30}}'
        ;;
    5)
        call_api "set_steering" '{"parameters": {"Value": -30}}'
        ;;
    6)
        call_api "set_steering" '{"parameters": {"Value": 0}}'
        ;;
    7)
        call_api "accelerate" '{"parameters": {}}'
        ;;
    8)
        call_api "gear_1" '{"parameters": {}}'
        ;;
    9)
        call_api "gear_2" '{"parameters": {}}'
        ;;
    10)
        call_api "gear_3" '{"parameters": {}}'
        ;;
    11)
        call_api "get_GPS" '{"parameters": {}}'
        ;;
    12)
        call_api "get_info" '{"parameters": {}}'
        ;;
    13)
        call_api "get_camera_image" '{"parameters": {"CameraID": "front"}}'
        check_images
        ;;
    14)
        call_api "get_all_camera" '{"parameters": {}}'
        check_images
        ;;
    *)
        echo "❌ Opção inválida. Use um número de 0 a 14."
        show_menu
        exit 1
        ;;
esac