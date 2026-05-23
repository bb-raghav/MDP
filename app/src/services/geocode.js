import axios from "axios"

export async function searchCity(city) {
  try {
    const apiBase = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"
    const response = await axios.get(
      `${apiBase}/geocode/${city}`
    )

    return response.data

  } catch (error) {

    console.log(error)

    return null
  }
}