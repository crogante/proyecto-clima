import requests
from datetime import datetime

def ver_pronostico():
    api_key = "a8e82be594b9484817baab945cbc3420"
    ciudad = input("¿De qué ciudad quieres el pronóstico?: ")
    
    # El endpoint 'forecast' nos da los próximos 5 días
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={ciudad}&appid={api_key}&units=metric&lang=es"

    try:
        res = requests.get(url)
        datos = res.json()

        if datos["cod"] == "200":
            print(f"\n📅 Pronóstico para {datos['city']['name']}, {datos['city']['country']}")
            print("=" * 45)

            # Recorremos la lista de predicciones (vienen cada 3 horas)
            for lectura in datos["list"]:
                # Extraemos la fecha y hora
                fecha_completa = lectura["dt_txt"] # Ejemplo: "2026-03-24 12:00:00"
                
                # Filtramos: Solo nos interesa ver qué pasará al mediodía (12:00)
                if "12:00:00" in fecha_completa:
                    dt = datetime.strptime(fecha_completa, "%Y-%m-%d %H:%M:%S")
                    dia_semana = dt.strftime("%A").capitalize() # Ej: Martes
                    fecha_corta = dt.strftime("%d/%m")        # Ej: 24/03

                    temp = lectura["main"]["temp"]
                    clima = lectura["weather"][0]["description"]
                    viento = lectura["wind"]["speed"]

                    print(f"👉 {dia_semana} {fecha_corta}:")
                    print(f"   🌡️  {temp}°C | ☁️  {clima.capitalize()}")
                    print(f"   💨 Viento: {viento} m/s")
                    print("-" * 30)
        else:
            print(f"❌ Error: {datos['message']}")

    except Exception as e:
        print(f"⚠️ Error de conexión: {e}")

if __name__ == "__main__":
    ver_pronostico()
    input("\nPresiona Enter para cerrar...")