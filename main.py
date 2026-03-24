from fastapi import FastAPI, HTTPException, Header
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción pondrías la URL de tu app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


API_KEY = "a8e82be594b9484817baab945cbc3420"
ADMIN_TOKEN = "mi_clave_secreta_123" # Esta sería tu contraseña

# Función auxiliar para guardar el log
def registrar_consulta(tipo, ciudad):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_linea = f"[{ahora}] CONSULTA: {tipo} | CIUDAD: {ciudad}\n"
    
    with open("consultas.log", "a", encoding="utf-8") as f:
        f.write(log_linea)

@app.get("/clima/{ciudad}")
def obtener_clima(ciudad: str):
    registrar_consulta("Actual", ciudad) # Guardamos el log
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric&lang=es"
    res = requests.get(url)
    
    if res.status_code == 200:
        return res.json()
    raise HTTPException(status_code=404, detail="Ciudad no encontrada")

@app.get("/pronostico/{ciudad}")
def obtener_pronostico(ciudad: str):
    registrar_consulta("Extendido", ciudad) # Guardamos el log
    
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={ciudad}&appid={API_KEY}&units=metric&lang=es"
    res = requests.get(url)
    
    if res.status_code == 200:
        datos = res.json()
        # Filtramos para devolver algo limpio
        pronostico_limpio = [
            {"fecha": l["dt_txt"], "temp": l["main"]["temp"], "clima": l["weather"][0]["description"]}
            for l in datos["list"] if "12:00:00" in l["dt_txt"]
        ]
        return {"ciudad": datos["city"]["name"], "pronostico": pronostico_limpio}
    
    raise HTTPException(status_code=404, detail="Error en el pronóstico")

import os

# ... (tus otros endpoints siguen arriba)

@app.get("/logs")
def ver_logs(x_token: str = Header(None)):
    # Verificamos si envió el token correcto
    if x_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="No tienes permiso para ver esto")
    # Verificamos si el archivo existe para evitar errores
    if not os.path.exists("consultas.log"):
        return {"mensaje": "Aún no hay registros de consultas."}

    try:
        with open("consultas.log", "r", encoding="utf-8") as f:
            # Leemos todas las líneas y las devolvemos como una lista
            lineas = f.readlines()
            
            # Limpiamos los saltos de línea (\n) para que el JSON se vea bien
            historial = [linea.strip() for linea in lineas]
            
            return {
                "total_consultas": len(historial),
                "registros": historial
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer logs: {e}")