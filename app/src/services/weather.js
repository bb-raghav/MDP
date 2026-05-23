import axios from "axios"

export async function fetchWeatherData(city) {

  try {
    const apiBase = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"
    const response = await axios.get(
      `${apiBase}/live-aqi/${city}`
    )

    return response.data

  } catch (err) {

    console.log(err)

    return null
  }
}