import axios from "axios"

export async function searchCity(city) {
  try {
    const apiBase = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"
    const response = await axios.get(
      `${apiBase}/geocode/${encodeURIComponent(city)}`
    )

    return response.data

  } catch (error) {

    console.error(error)

    return null
  }
}


export async function suggestCities(query) {
  try {
    const apiBase = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"
    const response = await axios.get(
      `${apiBase}/geocode-suggest/${encodeURIComponent(query)}`
    )
    return response.data.suggestions || []
  } catch (err) {
    console.error(err)
    return []
  }
}
