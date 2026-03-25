import { instance as axios } from '@/plugins/axios'

class ApiService {
  /**
   * Simula una latencia para pruebas de UI (Loading states)
   */
  private static async simulateDelay() {
    await new Promise(resolve => setTimeout(resolve, 1500))
  }

  static async getAll(url: string) {
    try {
      await ApiService.simulateDelay() 
      const { data } = await axios.get(url)
      
      if (data && data.estado === 'ok') return data
      
      throw { 
        estado: data?.estado || 'error', 
        mensaje: data?.mensaje || 'Error desconocido al obtener el listado.' 
      }
    } catch (error: any) {
      // Si el error ya tiene nuestro formato (fue lanzado por el throw de arriba)
      if (error.estado) throw error;

      throw {
        estado: error.response?.data?.estado || 'exception',
        mensaje: error.response?.data?.mensaje || 'Error de comunicación con el servidor.'
      }
    }
  }

  static async getOne(url: string, id: number) {
    try {
      await ApiService.simulateDelay() 
      const { data } = await axios.get(`${url}${id}`)
      
      if (data && data.estado === 'ok') return data

      throw { 
        estado: data?.estado || 'error', 
        mensaje: data?.mensaje || 'Registro no encontrado.' 
      }
    } catch (error: any) {
      if (error.estado) throw error;
      throw {
        estado: error.response?.data?.estado || 'exception',
        mensaje: error.response?.data?.mensaje || 'Error al obtener los datos del registro.'
      }
    }
  }

  static async create(url: string, payload: object) {
    try {
      await ApiService.simulateDelay() 
      const { data } = await axios.post(url, payload)
      
      if (data && data.estado === 'ok') return data 
      
      throw { 
        estado: data?.estado || 'error', 
        mensaje: data?.mensaje || 'Error al intentar crear el registro.'
      }
    } catch (error: any) {
      if (error.estado) throw error;
      throw {
        estado: error.response?.data?.estado || 'error',
        mensaje: error.response?.data?.mensaje || 'Error de red al intentar crear el registro.'
      }
    }
  }

  static async update(url: string, id: number, payload: object) {
    try {
      await ApiService.simulateDelay() 
      const { data } = await axios.put(`${url}${id}`, payload)
      
      if (data && data.estado === 'ok') return data 
      
      throw { 
        estado: data?.estado || 'error', 
        mensaje: data?.mensaje || 'Error al intentar actualizar el registro.'
      }
    } catch (error: any) {
      if (error.estado) throw error;
      throw {
        estado: error.response?.data?.estado || 'error',
        mensaje: error.response?.data?.mensaje || 'Error de red al intentar actualizar el registro.'
      }
    }
  }

  static async destroy(url: string, id: number) {
    try {
      await ApiService.simulateDelay() 
      const { data } = await axios.delete(`${url}${id}`)
      
      if (data && data.estado === 'ok') return data
      
      throw { 
        estado: data?.estado || 'error', 
        mensaje: data?.mensaje || 'Error al intentar eliminar el registro.'
      }
    } catch (error: any) {
      if (error.estado) throw error;
      throw {
        estado: error.response?.data?.estado || 'error',
        mensaje: error.response?.data?.mensaje || 'No se pudo eliminar el registro (posible restricción de integridad).'
      }
    }
  }

  static async execute(url: string) {
    try {
      await ApiService.simulateDelay() 
      const { data } = await axios.post(url)
      
      if (data && data.estado === 'ok') return data 
      
      throw { 
        estado: data?.estado || 'error', 
        mensaje: data?.mensaje || 'Error crítico en el proceso de base de datos.'
      }
    } catch (error: any) {
      if (error.estado) throw error;
      throw {
        estado: error.response?.data?.estado || 'exception',
        mensaje: error.response?.data?.mensaje || 'Excepción crítica en el servidor al procesar la base de datos.'
      }
    }
  }

  static async getByRelation(url: string, relationId: number) {
    try {
      await ApiService.simulateDelay() 
      const { data } = await axios.get(`${url}${relationId}`)
      
      if (data && data.estado === 'ok') return data

      throw { 
        estado: data?.estado || 'error', 
        mensaje: data?.mensaje || 'No se encontró información para esta relación.' 
      }
    } catch (error: any) {
      if (error.estado) throw error;
      throw {
        estado: error.response?.data?.estado || 'exception',
        mensaje: error.response?.data?.mensaje || 'Error al obtener el listado filtrado.'
      }
    }
  }
}

export default ApiService;