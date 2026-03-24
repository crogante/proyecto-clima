import requests

def consultar_clima():
    # Tu llave personal ya configurada
    api_key = "1da149bfd59d364430c975c5480e93d3"
    
    print("=== Consultor de Clima en Tiempo Real ===")
    ciudad = input("Introduce el nombre de la ciudad (ej: Rosario, Madrid, Tokyo): ")
    
    # Construimos la URL con unidades métricas (Celsius) y en español
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"

    try:
        # Hacemos la petición
        respuesta = requests.get(url)
        # Convertimos la respuesta de texto plano a un "diccionario" de Python (JSON)
        datos = respuesta.json()

        if datos["cod"] == 200:
            nombre = datos["name"]
            pais = datos["sys"]["country"]
            temp = datos["main"]["temp"]
            sensacion = datos["main"]["feels_like"]
            descripcion = datos["weather"][0]["description"]

            print(f"\n📍 Ciudad: {nombre}, {pais}")
            print(f"🌡️  Temperatura actual: {temp}°C")
            print(f"🤔 Sensación térmica: {sensacion}°C")
            print(f"☁️  Estado: {descripcion.capitalize()}")
        else:
            print(f"\n❌ Error: {datos['message'].capitalize()}. Verifica el nombre.")

    except requests.exceptions.ConnectionError:
        print("\n🌐 Error: No se pudo conectar a internet.")
    except Exception as e:
        print(f"\n⚠️ Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    consultar_clima()
    print("\n-----------------------------------------")
    input("Presiona Enter para cerrar...")