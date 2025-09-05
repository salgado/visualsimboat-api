# interactive_test.py
import asyncio
import logging
from visualsimboat_api import VisualSimBoatAPI  # Certifique-se de que o arquivo anterior está salvo como visualsibmboat_api.py

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def print_menu():
    """Exibe o menu de opções."""
    print("\n" + "="*50)
    print("       🚤 VISUALSIMBOAT - MENU INTERATIVO")
    print("="*50)
    print("1.  Conectar ao simulador")
    print("2.  Iniciar motor")
    print("3.  Parar motor")
    print("4.  Definir aceleração (0-100%)")
    print("5.  Definir direção (-100 a 100)")
    print("6.  Selecionar marcha 1")
    print("7.  Selecionar marcha 2")
    print("8.  Selecionar marcha 3")
    print("9.  Acelerar (incremental)")
    print("10. Obter posição GPS")
    print("11. Capturar imagem da câmera frontal")
    print("12. Capturar imagens de todas as câmeras")
    print("13. Parada de emergência (aceleração=0, direção=0)")
    print("14. Obter informações da API")
    print("0.  Sair")
    print("="*50)


async def main():
    async with VisualSimBoatAPI() as api:
        print("🚀 Iniciando cliente VisualSimBoat...")

        while True:
            print_menu()
            try:
                choice = input("Escolha uma opção [0-14]: ").strip()
                if choice == "0":
                    print("👋 Encerrando teste. Até logo!")
                    break

                # Test connection first
                if choice not in ["1"] and choice != "14":  # Allow info without connect
                    gps = await api.get_gps()
                    if gps is None:
                        print("⚠️  Você precisa estar conectado. Tente a opção 1 primeiro.")
                        continue

                # Menu de opções
                if choice == "1":
                    connected = await api.connect()
                    if connected:
                        info = await api.get_info()
                        if info:
                            version = info.get("version", "desconhecida")
                            print(f"✅ Conectado! Simulador: VisualSimBoat v{version}")
                        else:
                            print("✅ Conectado, mas não foi possível obter informações.")
                    else:
                        print("❌ Falha ao conectar. Verifique se o simulador está rodando.")

                elif choice == "2":
                    if await api.engine_start():
                        print("✅ Motor ligado.")
                    else:
                        print("❌ Falha ao ligar o motor.")

                elif choice == "3":
                    if await api.engine_stop():
                        print("✅ Motor desligado.")
                    else:
                        print("❌ Falha ao desligar o motor.")

                elif choice == "4":
                    try:
                        value = int(input("Digite a aceleração (0-100): "))
                        if await api.set_throttle(value):
                            print(f"✅ Aceleração definida para {value}%.")
                        else:
                            print("❌ Falha ao definir aceleração.")
                    except ValueError:
                        print("❌ Valor inválido. Deve ser um número entre 0 e 100.")

                elif choice == "5":
                    try:
                        value = int(input("Digite o ângulo de direção (-100 a 100, negativo = esquerda): "))
                        if await api.set_steering(value):
                            print(f"✅ Direção definida para {value}.")
                        else:
                            print("❌ Falha ao definir direção.")
                    except ValueError:
                        print("❌ Valor inválido. Deve ser um número entre -100 e 100.")

                elif choice == "6":
                    if await api.gear_1():
                        print("✅ Marcha 1 engatada.")
                    else:
                        print("❌ Falha ao engatar marcha 1.")

                elif choice == "7":
                    if await api.gear_2():
                        print("✅ Marcha 2 engatada.")
                    else:
                        print("❌ Falha ao engatar marcha 2.")

                elif choice == "8":
                    if await api.gear_3():
                        print("✅ Marcha 3 engatada.")
                    else:
                        print("❌ Falha ao engatar marcha 3.")

                elif choice == "9":
                    if await api.accelerate():
                        print("✅ Comando de aceleração enviado.")
                    else:
                        print("❌ Falha ao acelerar.")

                elif choice == "10":
                    gps = await api.get_gps()
                    if gps:
                        print(f"📍 GPS Atual: Lat {gps['lat']:.6f}, Lon {gps['lon']:.6f}, Alt {gps['alt']:.2f}m")
                    else:
                        print("❌ Não foi possível obter GPS.")

                elif choice == "11":
                    print("📸 Capturando imagem frontal...")
                    img_data = await api.get_camera_image("front")
                    if img_data:
                        filename = "test_front.jpg"
                        with open(filename, "wb") as f:
                            f.write(img_data)
                        print(f"✅ Imagem frontal salva como '{filename}'.")
                    else:
                        print("❌ Falha ao capturar imagem frontal.")

                elif choice == "12":
                    print("📸 Capturando imagens de todas as câmeras...")
                    images = await api.get_all_camera()
                    if images:
                        for name, data in images.items():
                            filename = f"test_{name}"
                            with open(filename, "wb") as f:
                                f.write(data)
                            print(f"✅ Salvo: {filename}")
                        print(f"✅ {len(images)} imagens salvas em diretório atual.")
                    else:
                        print("❌ Nenhuma imagem foi capturada.")

                elif choice == "13":
                    if await api.emergency_stop():
                        print("🛑 Parada de emergência ativada: aceleração=0, direção=0.")
                    else:
                        print("⚠️  Erro ao tentar parada de emergência.")

                elif choice == "14":
                    info = await api.get_info()
                    if info:
                        print("\n🔧 Informações da API:")
                        for k, v in info.items():
                            print(f"   {k}: {v}")
                    else:
                        print("❌ Não foi possível obter informações da API.")

                else:
                    print("❌ Opção inválida. Escolha um número entre 0 e 14.")

            except KeyboardInterrupt:
                print("\n\n👋 Interrompido pelo usuário. Encerrando...")
                break
            except Exception as e:
                print(f"❌ Erro inesperado: {e}")

    print("🔚 Cliente encerrado.")


if __name__ == "__main__":
    asyncio.run(main())