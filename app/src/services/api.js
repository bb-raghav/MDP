import axios from "axios"

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"

const API = axios.create({
  baseURL: API_BASE_URL
})

export async function predictAQI(inputData) {
  try {
    const response = await API.post("/predict", inputData)
    return response.data
  } catch (error) {
    console.log(error)
    return null
  }
}