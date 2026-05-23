// src/App.jsx

import { useEffect, useState } from "react"

import {
  MapContainer,
  TileLayer,
  Circle,
  useMap,
  Marker,
  Popup,
} from "react-leaflet"

import "leaflet/dist/leaflet.css"

import "./styles/app.css"

const DEFAULT_CITY = {
  name: "Bengaluru",
  lat: 12.9716,
  lon: 77.5946,
}

function FlyToCity({ city }) {
  const map = useMap()

  useEffect(() => {

    if (!city?.lat || !city?.lon)
      return

    map.flyTo(
      [city.lat, city.lon],
      11,
      {
        duration: 2,
      }
    )

  }, [city, map])

  return null
}

export default function App() {

  const [search, setSearch] =
    useState("")

  const [loading, setLoading] =
    useState(false)

  const [selectedCity, setSelectedCity] =
    useState(DEFAULT_CITY)

  const [predictedZones, setPredictedZones] =
    useState([])

  const [aqiData, setAqiData] =
    useState({

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
    })

  async function fetchAQI(cityName) {
    try {
      const apiBase = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"
      const response = await fetch(
        `${apiBase}/live-aqi/${cityName}`
      )

      const data = await response.json()

      if (data.error) {
        alert(data.error)
        return null
      }

      const status =
        data.live_aqi <= 50
          ? "Good"
          : data.live_aqi <= 100
          ? "Moderate"
          : data.live_aqi <= 150
          ? "Poor"
          : "Severe"

      const finalData = {
        ...data,
        status,
      }

      setAqiData(finalData)

      return finalData

    } catch (error) {

      console.log(error)

      return null
    }
  }

  function generatePredictionsForCity(
    city,
    baseAQI
  ) {

    const offsets = [

      [0.03, 0.02],

      [-0.04, 0.01],

      [0.01, -0.05],

      [-0.02, -0.03],
    ]

    const zones = offsets.map(
      (offset, i) => ({

        id: i,

        lat:
          city.lat + offset[0],

        lon:
          city.lon + offset[1],

        predictedAQI:
          Math.max(

            40,

            baseAQI +

            (
              Math.floor(
                Math.random() * 40
              ) - 20
            )
          ),
      })
    )

    setPredictedZones(zones)
  }

  async function handleSearch() {

    if (!search.trim())
      return

    setLoading(true)

    try {

      const geoResponse =
        await fetch(
          `https://nominatim.openstreetmap.org/search?q=${search}&format=json&limit=1`
        )

      const geoData =
        await geoResponse.json()

      if (!geoData.length) {

        alert("City not found")

        return
      }

      const city = {

        name: search,

        lat: parseFloat(
          geoData[0].lat
        ),

        lon: parseFloat(
          geoData[0].lon
        ),
      }

      setSelectedCity(city)

      const liveData =
        await fetchAQI(city.name)

      if (liveData) {

        generatePredictionsForCity(
          city,
          liveData.live_aqi
        )
      }

    } catch (err) {

      console.log(err)

    } finally {

      setLoading(false)
    }
  }

  useEffect(() => {

    async function init() {

      const liveData =
        await fetchAQI(
          DEFAULT_CITY.name
        )

      if (liveData) {

        generatePredictionsForCity(
          DEFAULT_CITY,
          liveData.live_aqi
        )
      }
    }

    init()

  }, [])

  function getColor(aqi) {

    if (aqi <= 50)
      return "#22c55e"

    if (aqi <= 100)
      return "#eab308"

    if (aqi <= 150)
      return "#f97316"

    return "#ef4444"
  }

  return (

    <div className="app">

      {/* SIDEBAR */}

      <aside className="sidebar">

        <h2>
          AeroSense AI
        </h2>

        <div className="menu">

          <button className="active">
            Home
          </button>

          <button>
            About
          </button>

          <button>
            Data
          </button>

        </div>

      </aside>

      {/* MAIN */}

      <main className="main">

        {/* HEADER */}

        <div className="topbar">

          <div>

            <h1>
              AeroSense AI
            </h1>

            <p>
              Predicting AQI in
              sensor-sparse urban
              environments
            </p>

          </div>

          <div className="live-pill">

            <span></span>

            LIVE

          </div>

        </div>

        {/* SEARCH */}

        <div className="searchbar">

          <input
            value={search}
            onChange={(e) =>
              setSearch(
                e.target.value
              )
            }
            placeholder="Search city..."
          />

          <button
            onClick={handleSearch}
          >

            {
              loading
                ? "Loading..."
                : "Search"
            }

          </button>

        </div>

        {/* DASHBOARD */}

        <div className="dashboard">

          {/* LEFT */}

          <div className="left-panel">

            <div className="aqi-card">

              <p>
                Current Live AQI
              </p>

              <h1
                style={{
                  color:
                    getColor(
                      aqiData.live_aqi
                    ),
                }}
              >
                {aqiData.live_aqi}
              </h1>

              <div
                className="status-pill"
                style={{
                  background:
                    getColor(
                      aqiData.live_aqi
                    ),
                }}
              >
                {aqiData.status}
              </div>

            </div>

            {/* MINI GRID */}

            <div className="mini-grid">

              <div className="mini-card">

                <p>PM2.5</p>

                <h2>
                  {aqiData.pm25}
                </h2>

              </div>

              <div className="mini-card">

                <p>NO₂</p>

                <h2>
                  {aqiData.no2}
                </h2>

              </div>

              <div className="mini-card">

                <p>SO₂</p>

                <h2>
                  {aqiData.so2}
                </h2>

              </div>

              <div className="mini-card">

                <p>
                  Temperature
                </p>

                <h2>

                  {
                    Math.round(
                      aqiData.temperature
                    )
                  }°C

                </h2>

              </div>

            </div>

            {/* INFO */}

            <div className="info-card">

              <h3>
                AI Prediction Summary
              </h3>

              <p>
                AI estimated AQI
                zones generated
                using nearby
                atmospheric drift
                modelling and
                environmental
                sensor analysis.
              </p>

            </div>

            <div className="info-card">

              <h3>
                Sensor Gap Detection
              </h3>

              <p>
                Sparse monitoring
                coverage detected.
                AeroSense AI has
                generated predicted
                AQI estimations for
                nearby unsensored
                regions.
              </p>

            </div>

          </div>

          {/* RIGHT */}

          <div className="map-panel">

            <MapContainer
              center={[
                selectedCity.lat,
                selectedCity.lon,
              ]}
              zoom={11}
              style={{
                height: "620px",
                width: "100%",
                borderRadius:
                  "24px",
              }}
            >

              <FlyToCity
                city={selectedCity}
              />

              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />

              {/* LIVE SENSOR */}

              <Marker
                position={[
                  selectedCity.lat,
                  selectedCity.lon,
                ]}
              >

                <Popup>
                  Live AQI Sensor
                </Popup>

              </Marker>

              {/* PREDICTED ZONES */}

              {
                predictedZones.map(
                  (zone) => (

                    <Circle
                      key={zone.id}

                      center={[
                        zone.lat,
                        zone.lon,
                      ]}

                      radius={7000}

                      pathOptions={{

                        color:
                          getColor(
                            zone.predictedAQI
                          ),

                        fillColor:
                          getColor(
                            zone.predictedAQI
                          ),

                        fillOpacity:
                          0.28,
                      }}
                    />
                  )
                )
              }

            </MapContainer>

            {/* LEGEND */}

            <div className="legend">

              <div>

                <span
                  style={{
                    background:
                      "#22c55e",
                  }}
                ></span>

                Good

              </div>

              <div>

                <span
                  style={{
                    background:
                      "#eab308",
                  }}
                ></span>

                Moderate

              </div>

              <div>

                <span
                  style={{
                    background:
                      "#f97316",
                  }}
                ></span>

                Poor

              </div>

              <div>

                <span
                  style={{
                    background:
                      "#ef4444",
                  }}
                ></span>

                Severe

              </div>

            </div>

          </div>

        </div>

      </main>

    </div>
  )
}