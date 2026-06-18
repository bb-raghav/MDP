import {
  MapContainer,
  TileLayer,
  Circle,
  Popup,
  useMap,
} from "react-leaflet"

import { useEffect } from "react"

import "leaflet/dist/leaflet.css"

function FlyToLocation({
  lat,
  lng,
}) {
  const map = useMap()

  useEffect(() => {
    map.flyTo(
      [lat, lng],
      10,
      {
        duration: 1.5,
      }
    )
  }, [lat, lng, map])

  return null
}

export default function PollutionMap({
  center,
  liveAQI,
  predictedZones,
}) {
  function getColor(aqi) {
    if (aqi <= 50)
      return "#00e400"

    if (aqi <= 100)
      return "#ffd700"

    if (aqi <= 150)
      return "#ff9500"

    return "#ff2d55"
  }

  return (
    <MapContainer
      center={[
        center.lat,
        center.lon,
      ]}
      zoom={10}
      style={{
        height: "650px",
        width: "100%",
        borderRadius: "28px",
      }}
    >
      <FlyToLocation
        lat={center.lat}
        lng={center.lon}
      />

      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      <Circle
        center={[
          center.lat,
          center.lon,
        ]}
        radius={2500}
        pathOptions={{
          color: getColor(
            liveAQI
          ),
          fillColor: getColor(
            liveAQI
          ),
          fillOpacity: 0.45,
        }}
      >
        <Popup>
          <div>
            <h3>
              Live Sensor AQI
            </h3>

            <p>
              AQI: {liveAQI}
            </p>
          </div>
        </Popup>
      </Circle>

      {predictedZones.map(
        (zone) => (
          <Circle
            key={zone.id}
            center={[
              zone.lat,
              zone.lon,
            ]}
            radius={4000}
            pathOptions={{
              color: getColor(
                zone.aqi
              ),
              fillColor: getColor(
                zone.aqi
              ),
              fillOpacity: 0.25,
            }}
          >
            <Popup>
              <div>
                <h3>
                  AI Predicted AQI
                </h3>

                <p>
                  Estimated AQI:
                  {" "}
                  {zone.aqi}
                </p>

                <small>
                  No physical sensor
                  detected in this
                  area.
                </small>
              </div>
            </Popup>
          </Circle>
        )
      )}
    </MapContainer>
  )
}
