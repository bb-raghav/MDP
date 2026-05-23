import axios from "axios"

const TOKEN = import.meta.env.VITE_WAQI_API_KEY || ""

if (!TOKEN) {
  console.warn("VITE_WAQI_API_KEY environment variable is not set")
}

export async function getLiveAQI(city) {
  try {
    const response = await axios.get(
      `https://api.waqi.info/feed/${city}/?token=${TOKEN}`
    )

    const data = response.data.data

    return {
      city: data.city.name,
      aqi: data.aqi,
      lat: data.city.geo[0],
      lng: data.city.geo[1],
      pm25: data.iaqi?.pm25?.v || 0,
      no2: data.iaqi?.no2?.v || 0,
      so2: data.iaqi?.so2?.v || 0,
      temp: data.iaqi?.t?.v || 30,
    }
  } catch (err) {
    console.log(err)
    return null
  }
}