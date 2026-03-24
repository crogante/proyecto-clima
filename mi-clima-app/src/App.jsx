import { useState } from 'react'
import axios from 'axios'

function App() {
  const [ciudad, setCiudad] = useState('')
  const [datos, setDatos] = useState(null)
  const [pronostico, setPronostico] = useState(null)
  const [error, setError] = useState(false)

  const buscarClima = async () => {
    setError(false)
    setDatos(null)
    setPronostico(null)
    try {
      const [climaRes, pronosticoRes] = await Promise.all([
        axios.get(`http://127.0.0.1:8000/clima/${ciudad}`),
        axios.get(`http://127.0.0.1:8000/pronostico/${ciudad}`)
      ]);
      
      console.log("Datos de clima recibidos:", climaRes.data);
      setDatos(climaRes.data)

      console.log("Datos de pronóstico recibidos:", pronosticoRes.data);
      setPronostico(pronosticoRes.data)

    } catch (err) {
      setError(true)
      setDatos(null)
      setPronostico(null)
    }
  }

  return (
    <div style={{ textAlign: 'center', marginTop: '50px', fontFamily: 'sans-serif' }}>
      <h1>🌤️ Weather App (FastAPI + React)</h1>
      <input 
        type="text" 
        placeholder="Ciudad (ej: Rosario)" 
        value={ciudad}
        onChange={(e) => setCiudad(e.target.value)}
        style={{ padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
      />
      <button onClick={buscarClima} style={{ padding: '10px 20px', marginLeft: '10px', cursor: 'pointer' }}>
        Consultar
      </button>

      {error && <p style={{ color: 'red' }}>❌ No se encontró la ciudad o el servidor está apagado.</p>}

      {datos && (
        <div style={{ marginTop: '20px', background: '#f0f0f0', padding: '20px', borderRadius: '15px', display: 'inline-block' }}>
          <h2>{datos.name}</h2>
          <p style={{ fontSize: '30px', fontWeight: 'bold' }}>{datos.main.temp}°C</p>
          <p>Sensación: {datos.main.feels_like}°C</p>
          <p>Estado: {datos.weather[0].description.toUpperCase()}</p>
        </div>
      )}

      {pronostico && (
        <div style={{ marginTop: '30px' }}>
          <h3>Pronóstico Extendido</h3>
          <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', flexWrap: 'wrap' }}>
            {pronostico.pronostico.map((dia, index) => (
              <div key={index} style={{ background: '#e0e0e0', padding: '15px', borderRadius: '10px' }}>
                <p><strong>{new Date(dia.fecha).toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric' })}</strong></p>
                <p>{dia.temp}°C</p>
                <p>{dia.clima}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default App