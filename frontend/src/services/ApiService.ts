import { instance as axios } from '@/plugins/axios'
import type { AxiosError } from 'axios'

interface BackendErrorResponse {
  estado: 'error' | 'not_found' | 'exception'
  mensaje: string
}

class ApiService {
  private static async simulateDelay() {
    // 1500 ms (1.5 segundos) de latencia simulada
    const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))
    await delay(1500)
  }

  private static handleAxiosError(error: unknown) {
    const axiosError = error as AxiosError<BackendErrorResponse>
    
    // Comprobar si hay respuesta del back
    if (axiosError.response) {
      const backendResponse = axiosError.response.data

      if (backendResponse && backendResponse.mensaje) {
        // Lanzar un nuevo error con el mensaje limpio.
        const estado = axiosError.response.status
        let errorMessage = backendResponse.mensaje

        errorMessage = `${estado} | ${errorMessage}`
        throw new Error(errorMessage)
      }
    }
    // Si no hay respuesta o no tiene el formato esperado, relanzar el error original.
    throw error
  }
  static async getAll(url: string) {
    try {
      // Aplicar latencia
      await ApiService.simulateDelay() 

      const { data } = await axios.get(url)
      return data
    } catch (error) {
      ApiService.handleAxiosError(error)
    }
  }

  static async getOne(url: string, id: number) {
    try {
      // Aplicar latencia
      await ApiService.simulateDelay() 

      const { data } = await axios.get(`${url}${id}`)
      return data
    } catch (error) {
      ApiService.handleAxiosError(error)
    }
  }

  static async create(url: string, payload: object) {
    try {
      // Aplicar latencia
      await ApiService.simulateDelay() 

      const { data } = await axios.post(url, payload)
      return data
    } catch (error) {
      ApiService.handleAxiosError(error)
    }
  }

  static async update(url: string, id: number, payload: object) {
    try {
      // Aplicar latencia
      await ApiService.simulateDelay() 
      const { data } = await axios.put(`${url}${id}`, payload)
      console.log('try update apiservice')
      console.log('data')
      console.log(data)
      return data
    } catch (error) {
      ApiService.handleAxiosError(error)
    }
  }

  static async destroy(url: string, id: number) {
    try {
      // Aplicar latencia
      await ApiService.simulateDelay() 

      const { data } = await axios.delete(`${url}${id}`)
      return data
    } catch (error) {
      ApiService.handleAxiosError(error)
    }
  }

  static async execute(url: string) {
    try {
      // Aplicar latencia
      await ApiService.simulateDelay() 

      const { data } = await axios.post(url)
      return data
    } catch (error) {
      ApiService.handleAxiosError(error)
    }
  }
}
export default ApiService