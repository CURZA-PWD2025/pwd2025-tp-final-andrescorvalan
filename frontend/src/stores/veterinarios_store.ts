import type { Veterinario } from '@/interface/veterinario'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/api_service'
import type { ApiRespuesta } from '@/interface/api_respuesta'


const url = 'veterinarios/'
const defaultVeterinario: Veterinario = {
  id: 0,
  nombre: '',
  apellido: '',
  matricula: '',
  telefono: '',
  email: '',
  especialidades: []
}

const useVeterinariosStore = defineStore('veterinarios', () => {

  const veterinarios = ref<Array<Veterinario>>([])
  const veterinario = ref<Veterinario>({ ...defaultVeterinario })

  async function buscar_veterinario(id: number): Promise<ApiRespuesta> {
    const encontrado = veterinarios.value.find((veterinario) => veterinario.id === id)
    if (encontrado) {
      veterinario.value = { ...encontrado }
      return {
        estado: 'ok',
        mensaje: 'Encontrado localmente',
        objeto: veterinario.value
      }
    }
    try {
      const respuesta = await getOne(id) 
      respuesta.objeto = respuesta.datos 
      veterinario.value = { ...respuesta.objeto }
      return respuesta
    } catch (error) {
      throw error 
    }
  }

  async function getAll() {
    try {
      const respuesta = await ApiService.getAll(url)
      veterinarios.value = respuesta.datos || []
      return respuesta
    } catch (error: any) {
      veterinarios.value = []
      throw error
    }
  }

  async function getOne(id: number) {
    try {
      const respuesta = await ApiService.getOne(url, id)
      if (!respuesta.datos) 
        throw new Error('No se encontraron datos');
      else {
        veterinario.value = respuesta.datos
        return respuesta
      }
    } catch (error: any) {
      veterinario.value = { ...defaultVeterinario }
      throw error
    }
  }

  async function create(obj_veterinario: Veterinario) {
    try {
      const respuesta = await ApiService.create(url, obj_veterinario)
      const nuevoVeterinario = respuesta.objeto
      veterinarios.value.push({ ...nuevoVeterinario })
      veterinario.value = { ...nuevoVeterinario }
      await getAll()
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  async function update(obj_veterinario: Veterinario) {
    if (!obj_veterinario.id)
      throw {
        estado: 'error',
        mensaje: 'Veterinario: No se puede actualizar un veterinario sin ID.'
      }
    try {
      const respuesta = await ApiService.update(url, obj_veterinario.id, obj_veterinario)
      const nuevoVeterinario = respuesta.objeto
      const index = veterinarios.value.findIndex(vete => vete.id === obj_veterinario.id)
      if (index !== -1) {
        veterinarios.value[index] = { ...nuevoVeterinario }
      }
      veterinario.value = { ...nuevoVeterinario }
      await getAll()
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  async function destroy(id: number) {
    try {
      const respuesta = await ApiService.destroy(url, id)
      veterinarios.value = veterinarios.value.filter(vete => vete.id !== id);    
      veterinario.value = {...defaultVeterinario}
      await getAll()
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  function reset() {
    veterinarios.value = []
    veterinario.value = { ...defaultVeterinario }
  }

  return { reset, defaultVeterinario, veterinarios, veterinario, buscar_veterinario, getAll, getOne, create, update, destroy }
})

export default useVeterinariosStore