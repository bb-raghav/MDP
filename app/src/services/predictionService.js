export function generatePredictedZones(
  lat,
  lng,
  liveAQI
) {
  return [
    {
      id: 1,
      lat: lat + 0.03,
      lng: lng + 0.02,
      aqi: liveAQI + 12,
    },

    {
      id: 2,
      lat: lat - 0.025,
      lng: lng - 0.015,
      aqi: liveAQI - 8,
    },

    {
      id: 3,
      lat: lat + 0.018,
      lng: lng - 0.028,
      aqi: liveAQI + 18,
    },
  ]
}