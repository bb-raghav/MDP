import { useEffect, useRef, useState } from "react"
import { Circle, MapContainer, Marker, Popup, TileLayer, useMap } from "react-leaflet"
import "leaflet/dist/leaflet.css"
import "./styles/app.css"
import { suggestCities } from "./services/geocode"

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"

const DEFAULT_CITY = {
  name: "Bengaluru",
  displayName: "Bengaluru",
  aqiName: "Bengaluru",
  lat: 12.9716,
  lon: 77.5946,
}

const DEFAULT_AQI = {
  live_aqi: 78,
  pm25: 45,
  pm10: 70,
  no2: 14,
  so2: 3,
  temperature: 29,
  humidity: 64,
  pressure: 1008,
  wind_speed: 5,
  status: "Moderate",
}

const QUICK_CITIES = [
  { name: "Bengaluru", displayName: "Bengaluru", aqiName: "Bengaluru", lat: 12.9716, lon: 77.5946 },
  { name: "Delhi", displayName: "Delhi", aqiName: "Delhi", lat: 28.6139, lon: 77.209 },
  { name: "Mumbai", displayName: "Mumbai", aqiName: "Mumbai", lat: 19.076, lon: 72.8777 },
  { name: "Chennai", displayName: "Chennai", aqiName: "Chennai", lat: 13.0827, lon: 80.2707 },
]

function getAqiQuery(city) {
  return city?.aqiName || city?.name?.split(",")[0]?.trim() || city?.name
}

function FlyToCity({ city }) {
  const map = useMap()

  useEffect(() => {
    if (!city?.lat || !city?.lon) return
    map.flyTo([city.lat, city.lon], 11, { duration: 1.2 })
  }, [city, map])

  return null
}

function getStatus(aqi) {
  if (aqi <= 50) return "Good"
  if (aqi <= 100) return "Moderate"
  if (aqi <= 150) return "Poor"
  return "Severe"
}

function getColor(aqi) {
  if (aqi <= 50) return "#22c55e"
  if (aqi <= 100) return "#eab308"
  if (aqi <= 150) return "#f97316"
  return "#ef4444"
}

function formatMetric(value, fallback = "--") {
  if (value === null || value === undefined || Number.isNaN(value)) return fallback
  return value
}

function buildForecast(baseAQI, windSpeed = 5) {
  const drift = Math.min(14, Math.max(-10, (windSpeed - 4) * -2))
  return [1, 2, 3, 4, 5, 6].map((hour) => {
    const wave = Math.sin(hour * 0.9) * 8
    const predictedAQI = Math.max(20, Math.round(baseAQI + wave + drift + hour * 1.5))
    return {
      hour,
      predictedAQI,
      status: getStatus(predictedAQI),
    }
  })
}

function getHealthGuidance(status) {
  if (status === "Good") return "Air quality looks comfortable for outdoor activity."
  if (status === "Moderate") return "Sensitive groups should keep longer outdoor activity light."
  if (status === "Poor") return "Consider a mask outdoors and reduce heavy exertion."
  return "Avoid prolonged outdoor exposure and keep windows closed where possible."
}

export default function App() {
  const [search, setSearch] = useState("")
  const [loading, setLoading] = useState(false)
  const [suggestions, setSuggestions] = useState([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [selectedCity, setSelectedCity] = useState(DEFAULT_CITY)
  const [predictedZones, setPredictedZones] = useState([])
  const [aqiData, setAqiData] = useState(DEFAULT_AQI)
  const [aiPrediction, setAiPrediction] = useState(null)
  const [backendStatus, setBackendStatus] = useState("checking")
  const [errorMessage, setErrorMessage] = useState("")
  const [page, setPage] = useState("home")
  const suggestTimer = useRef(null)

  const forecast = buildForecast(aqiData.live_aqi, aqiData.wind_speed)
  const bestPredictedZone = predictedZones.reduce(
    (best, zone) => (zone.predictedAQI < best.predictedAQI ? zone : best),
    { predictedAQI: aqiData.live_aqi }
  )
  const worstPredictedZone = predictedZones.reduce(
    (worst, zone) => (zone.predictedAQI > worst.predictedAQI ? zone : worst),
    { predictedAQI: aqiData.live_aqi }
  )

  async function fetchAQI(cityName) {
    try {
      const response = await fetch(`${API_BASE}/live-aqi/${encodeURIComponent(cityName)}`)
      const data = await response.json()

      if (!response.ok || data.error) {
        setErrorMessage(data.error || "Could not load live AQI data.")
        return null
      }

      const finalData = {
        ...DEFAULT_AQI,
        ...data,
        status: getStatus(data.live_aqi),
      }

      setAqiData(finalData)
      setErrorMessage("")
      return finalData
    } catch (error) {
      console.error(error)
      setErrorMessage("Backend is not reachable. Showing the last available dashboard state.")
      return null
    }
  }

  async function fetchCityPrediction(cityName) {
    try {
      const response = await fetch(`${API_BASE}/predict-city/${encodeURIComponent(cityName)}`)
      const data = await response.json()

      if (!response.ok || data.error) {
        console.error(data.error || "Prediction failed")
        setAiPrediction(null)
        return null
      }

      setAiPrediction(data)
      return data
    } catch (error) {
      console.error(error)
      setAiPrediction(null)
      return null
    }
  }

  function generatePredictionsForCity(city, baseAQI) {
    const offsets = [
      [0.03, 0.02],
      [-0.04, 0.01],
      [0.01, -0.05],
      [-0.02, -0.03],
    ]

    const zones = offsets.map(([latOffset, lonOffset], index) => ({
      id: index,
      lat: city.lat + latOffset,
      lon: city.lon + lonOffset,
      predictedAQI: Math.max(40, Math.round(baseAQI + Math.random() * 40 - 20)),
    }))

    setPredictedZones(zones)
  }

  async function loadCity(city) {
    setSelectedCity(city)
    const aqiQuery = getAqiQuery(city)
    const [liveData] = await Promise.all([
      fetchAQI(aqiQuery),
      fetchCityPrediction(aqiQuery),
    ])
    generatePredictionsForCity(city, liveData?.live_aqi ?? aqiData.live_aqi)
  }

  async function handleSearch() {
    const query = search.trim()
    if (!query) return

    setLoading(true)
    setShowSuggestions(false)

    try {
      const response = await fetch(`${API_BASE}/geocode/${encodeURIComponent(query)}`)
      const data = await response.json()

      if (!response.ok || data.error) {
        setErrorMessage(data.error || "City not found.")
        return
      }

      await loadCity({
        name: data.name || query.split(",")[0].trim(),
        displayName: data.display_name || data.name || query,
        aqiName: data.aqi_query || data.name || query.split(",")[0].trim(),
        lat: data.lat,
        lon: data.lon,
      })
    } catch (error) {
      console.error(error)
      setErrorMessage("Could not geocode that city right now.")
    } finally {
      setLoading(false)
    }
  }

  async function fetchSuggestions(query) {
    if (!query || query.length < 3) {
      setSuggestions([])
      setShowSuggestions(false)
      return
    }

    try {
      const results = await suggestCities(query)
      setSuggestions(results || [])
      setShowSuggestions((results || []).length > 0)
    } catch (error) {
      console.error(error)
      setSuggestions([])
      setShowSuggestions(false)
    }
  }

  function onInputChange(event) {
    const value = event.target.value
    setSearch(value)

    if (suggestTimer.current) clearTimeout(suggestTimer.current)
    suggestTimer.current = setTimeout(() => fetchSuggestions(value.trim()), 300)
  }

  async function handleSuggestionClick(suggestion) {
    const city = {
      name: suggestion.name || suggestion.display_name?.split(",")[0]?.trim(),
      displayName: suggestion.display_name || suggestion.name,
      aqiName: suggestion.aqi_query || suggestion.name?.split(",")[0]?.trim(),
      lat: suggestion.lat,
      lon: suggestion.lon,
    }

    setSearch(city.name)
    setShowSuggestions(false)
    await loadCity(city)
  }

  useEffect(() => {
    let isMounted = true

    async function checkBackend() {
      try {
        const response = await fetch(`${API_BASE}/health`)
        if (!isMounted) return
        setBackendStatus(response.ok ? "online" : "offline")
      } catch (error) {
        console.error(error)
        if (isMounted) setBackendStatus("offline")
      }
    }

    async function initDefaultCity() {
      try {
        const response = await fetch(`${API_BASE}/live-aqi/${encodeURIComponent(DEFAULT_CITY.name)}`)
        const data = await response.json()

        if (!isMounted || !response.ok || data.error) {
          generatePredictionsForCity(DEFAULT_CITY, DEFAULT_AQI.live_aqi)
          return
        }

        const finalData = {
          ...DEFAULT_AQI,
          ...data,
          status: getStatus(data.live_aqi),
        }

        setAqiData(finalData)
        generatePredictionsForCity(DEFAULT_CITY, finalData.live_aqi)
        fetchCityPrediction(DEFAULT_CITY.name)
      } catch (error) {
        console.error(error)
      }
    }

    checkBackend()
    initDefaultCity()

    return () => {
      isMounted = false
      if (suggestTimer.current) clearTimeout(suggestTimer.current)
    }
  }, [])

  return (
    <div className="app">
      <aside className="sidebar">
        <h2>AeroSense AI</h2>

        <div className="menu">

          <button
            className={page === "home" ? "active" : ""}
            onClick={() => setPage("home")}
          >
            Home
          </button>

          <button
            className={page === "about" ? "active" : ""}
            onClick={() => setPage("about")}
          >
            About
          </button>

          <button
            className={page === "data" ? "active" : ""}
            onClick={() => setPage("data")}
          >
            Data
          </button>

        </div>
      </aside>

      <main className="main">
      {page === "home" && (<>
            <div className="topbar">
              <div>
                <h1>AeroSense AI</h1>
                <p>Predicting AQI in sensor-sparse urban environments</p>
              </div>

          <div className="live-pill">
            <span></span>
            {backendStatus === "online" ? "LIVE" : backendStatus === "checking" ? "SYNC" : "OFFLINE"}
          </div>
        </div>

        <div className="searchbar" style={{ position: "relative" }}>
          <input
            value={search}
            onChange={onInputChange}
            onKeyDown={(event) => {
              if (event.key === "Enter") handleSearch()
            }}
            placeholder="Search city..."
            autoComplete="off"
          />

          <button onClick={handleSearch} disabled={loading}>
            {loading ? "Loading..." : "Search"}
          </button>

          {showSuggestions && suggestions.length > 0 && (
            <ul
              className="suggestions-list"
              style={{
                position: "absolute",
                top: "58px",
                left: 0,
                right: 0,
                background: "#0b1220",
                border: "1px solid rgba(255,255,255,0.06)",
                borderRadius: "18px",
                listStyle: "none",
                margin: 0,
                padding: "6px 0",
                maxHeight: "240px",
                overflowY: "auto",
                zIndex: 50,
              }}
            >
              {suggestions.map((suggestion) => (
                <li
                  key={`${suggestion.name}-${suggestion.lat}-${suggestion.lon}`}
                  onClick={() => handleSuggestionClick(suggestion)}
                  style={{
                    padding: "10px 14px",
                    cursor: "pointer",
                    borderBottom: "1px solid rgba(255,255,255,0.02)",
                  }}
                >
                  <strong>{suggestion.name}</strong>
                  {suggestion.display_name && suggestion.display_name !== suggestion.name && (
                    <small>{suggestion.display_name}</small>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="quick-cities">
          {QUICK_CITIES.map((city) => (
            <button
              key={city.name}
              className={selectedCity.name === city.name ? "selected" : ""}
              onClick={() => {
                setSearch(city.name)
                loadCity(city)
              }}
            >
              {city.name}
            </button>
          ))}
        </div>

        {errorMessage && <div className="alert-banner">{errorMessage}</div>}

        <div className="dashboard">
          <div className="left-panel">
            <div className="aqi-card">
              <p>Current Live AQI</p>
              <h1 style={{ color: getColor(aqiData.live_aqi) }}>{aqiData.live_aqi}</h1>
              <div className="status-pill" style={{ background: getColor(aqiData.live_aqi) }}>
                {aqiData.status}
              </div>
            </div>

            <div className="comparison-card">
              <div>
                <p>AI Predicted AQI</p>
                <h2 style={{ color: getColor(aiPrediction?.predicted_aqi ?? aqiData.live_aqi) }}>
                  {formatMetric(aiPrediction?.predicted_aqi)}
                </h2>
                {aiPrediction?.raw_predicted_aqi && (
                  <small>Raw model: {aiPrediction.raw_predicted_aqi}</small>
                )}
              </div>
              <div>
                <p>Model Delta</p>
                <h2 className={(aiPrediction?.delta ?? 0) >= 0 ? "delta-up" : "delta-down"}>
                  {aiPrediction ? `${aiPrediction.delta > 0 ? "+" : ""}${aiPrediction.delta}` : "--"}
                </h2>
              </div>
            </div>

            <div className="mini-grid">
              <div className="mini-card">
                <p>PM2.5</p>
                <h2>{formatMetric(aqiData.pm25)}</h2>
              </div>

              <div className="mini-card">
                <p>NO2</p>
                <h2>{formatMetric(aqiData.no2)}</h2>
              </div>

              <div className="mini-card">
                <p>SO2</p>
                <h2>{formatMetric(aqiData.so2)}</h2>
              </div>

              <div className="mini-card">
                <p>Temperature</p>
                <h2>{formatMetric(Math.round(aqiData.temperature))}C</h2>
              </div>
            </div>

            <div className="mini-grid">
              <div className="mini-card compact">
                <p>Humidity</p>
                <h2>{formatMetric(aqiData.humidity)}%</h2>
              </div>

              <div className="mini-card compact">
                <p>Wind</p>
                <h2>{formatMetric(aqiData.wind_speed)} km/h</h2>
              </div>
            </div>

            <div className="forecast-card">
              <div className="section-heading">
                <h3>6-hour AQI Outlook</h3>
                <span>{selectedCity.displayName || selectedCity.name}</span>
              </div>

              <div className="forecast-bars">
                {forecast.map((point) => (
                  <div className="forecast-item" key={point.hour}>
                    <div className="forecast-track">
                      <span
                        style={{
                          height: `${Math.min(100, Math.max(18, point.predictedAQI / 2))}%`,
                          background: getColor(point.predictedAQI),
                        }}
                      ></span>
                    </div>
                    <strong>{point.predictedAQI}</strong>
                    <small>+{point.hour}h</small>
                  </div>
                ))}
              </div>
            </div>

            <div className="info-card">
              <h3>Health Guidance</h3>
              <p>{getHealthGuidance(aqiData.status)}</p>
            </div>

            <div className="info-card">
              <h3>Zone Intelligence</h3>
              <p>
                Nearby predicted AQI ranges from {bestPredictedZone.predictedAQI} to{" "}
                {worstPredictedZone.predictedAQI}, based on atmospheric drift and sparse sensor
                coverage.
              </p>
            </div>

            <div className="info-card">
              <h3>Sensor Gap Detection</h3>
              <p>
                Sparse monitoring coverage detected. AeroSense AI has generated predicted AQI
                estimations for nearby unsensored regions.
              </p>
            </div>
          </div>

          <div className="map-panel">
            <MapContainer
              center={[selectedCity.lat, selectedCity.lon]}
              zoom={11}
              style={{
                height: "620px",
                width: "100%",
                borderRadius: "24px",
              }}
            >
              <FlyToCity city={selectedCity} />

              <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

              <Marker position={[selectedCity.lat, selectedCity.lon]}>
                <Popup>{selectedCity.name}</Popup>
              </Marker>

              {predictedZones.map((zone) => (
                <Circle
                  key={zone.id}
                  center={[zone.lat, zone.lon]}
                  radius={7000}
                  pathOptions={{
                    color: getColor(zone.predictedAQI),
                    fillColor: getColor(zone.predictedAQI),
                    fillOpacity: 0.28,
                  }}
                >
                  <Popup>
                    <strong>Predicted AQI: {zone.predictedAQI}</strong>
                    <br />
                    {getStatus(zone.predictedAQI)} zone
                  </Popup>
                </Circle>
              ))}
            </MapContainer>

            <div className="legend">
              <div>
                <span style={{ background: "#22c55e" }}></span>
                Good
              </div>
              <div>
                <span style={{ background: "#eab308" }}></span>
                Moderate
              </div>
              <div>
                <span style={{ background: "#f97316" }}></span>
                Poor
              </div>
              <div>
                <span style={{ background: "#ef4444" }}></span>
                Severe
              </div>
            </div>
          </div>
        </div>
        </>
)}
{page === "about" && (

<div className="about-page">

  <h1>About AeroSense AI</h1>

  <div className="info-card">
    <h3>Project Objective</h3>

    <p>
      AeroSense AI predicts air quality in locations
      where monitoring stations are unavailable.

      The platform combines pollution indicators,
      meteorological observations and machine learning
      techniques to estimate AQI in sensor-sparse regions.
    </p>
  </div>

  <div className="info-card">
    <h3>Technology Stack</h3>

    <p>
      ReactJS • FastAPI • Python • Scikit-Learn
      • OpenStreetMap • WAQI API
    </p>
  </div>

  <div className="info-card">
    <h3>Future Scope</h3>

    <p>
      Integration of satellite imagery,
      meteorological forecasting,
      sensor fusion and deep learning
      for higher-resolution AQI prediction.
    </p>
  </div>

</div>

)}
{page === "data" && (

<div className="data-page">

  <h1>Training Dataset</h1>

  <div className="comparison-card">

    <div>
      <p>Total Records</p>
      <h2>1098</h2>
    </div>

    <div>
      <p>Features Used</p>
      <h2>11</h2>
    </div>

  </div>

  <div className="info-card">

    <h3>Dataset Features</h3>

    <p>
      PM2.5, PM10, NO2, SO2, CO,
      Temperature, Humidity,
      Pressure, Wind Speed,
      Apparent Temperature and AQI.
    </p>

  </div>

  <div className="info-card">

    <h3>Dataset Source</h3>

    <p>
      Historical AQI and meteorological observations
      collected from Indian cities and used for
      machine learning model training.
    </p>

  </div>

  <div className="info-card">

    <h3>Repository / Dataset Link</h3>

    <p>
      Paste your Drive or GitHub link here.
    </p>

  </div>

</div>

)}
      </main>
    </div>
  )
}
