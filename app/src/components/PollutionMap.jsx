import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup,
} from "react-leaflet";

import { useEffect, useState } from "react";

import axios from "axios";

import { useMap } from "react-leaflet";

function FixMapSize() {

  const map = useMap();

  useEffect(() => {
    setTimeout(() => {
      map.invalidateSize();
    }, 100);
  }, [map]);

  return null;
}

export default function PollutionMap() {

  const [pollutionPoints, setPollutionPoints] = useState([]);

  useEffect(() => {

    axios
      .get("http://127.0.0.1:8000/aqi-points")
      .then((response) => {
        setPollutionPoints(response.data);
      })
      .catch((error) => {
        console.error(error);
      });

  }, []);

  return (

    <div style={{ height: "420px", width: "100%" }}>

      <MapContainer
        center={[12.9716, 77.5946]}
        zoom={11}
        style={{
          height: "100%",
          width: "100%",
        }}
      >

        <FixMapSize />

        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {pollutionPoints.map((point, index) => (

          <CircleMarker
            key={index}
            center={[point.lat, point.lon]}
            radius={20}
            pathOptions={{
              color:
                point.aqi > 80
                  ? "red"
                  : point.aqi > 60
                  ? "orange"
                  : "green",

              fillOpacity: 0.6,
            }}
          >

            <Popup>

              <div>

                <h2 className="font-bold">
                  {point.name}
                </h2>

                <p>
                  AQI: {point.aqi}
                </p>

              </div>

            </Popup>

          </CircleMarker>
        ))}

      </MapContainer>

    </div>
  );
}