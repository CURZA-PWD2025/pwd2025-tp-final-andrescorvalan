import type { Especialidad } from '@/interface/especialidad'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/api_service'

const url = 'especialidades/'
const defaultEspecialidad: Especialidad = {
  id: 0,
  nombre: '',
  descripcion: '',
  activa: 0
}
const useEspecialidadesStore = defineStore('especialidades', () => {

  const especialidades = ref<Array<Especialidad>>([])
  const especialidad = ref<Especialidad>({ ...defaultEspecialidad })

  async function buscar_especialidad(id: number) {
    const busqueda = especialidades.value.find((esp) => esp.id === id)
    if (busqueda) {
      especialidad.value = { ...busqueda }
      return { 
        estado:'ok', 
        objeto: especialidad.value
      }
    }
    try {
      return await getOne(id)
    } catch (error) {
      throw error 
    }
  }

  async function getAll() {
    try {
      const respuesta = await ApiService.getAll(url)
      especialidades.value = respuesta.datos || []
      return respuesta
    } catch (error: any) {
      especialidades.value = []
      throw error
    }
  }

  async function getOne(id: number) {
    try {
      const respuesta = await ApiService.getOne(url, id)
      if (!respuesta.datos) 
        throw new Error('No se encontraron datos');
      else {
        especialidad.value = respuesta.datos
        return respuesta
      }
    } catch (error: any) {
      especialidad.value = { ...defaultEspecialidad }
      throw error
    }
  }

  async function create(obj_especialidad: Especialidad) {
    try {
      const respuesta = await ApiService.create(url, obj_especialidad)
      const nuevaEspecialidad = respuesta.objeto
      especialidades.value.push({ ...nuevaEspecialidad })
      especialidad.value = { ...nuevaEspecialidad }
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  async function update(obj_especialidad: Especialidad) {
    if (!obj_especialidad.id)
      throw  {
        estado: 'error', 
        mensaje: 'Especialidad: No se puede actualizar un especialidad sin ID.'
      }
    try {
      const respuesta = await ApiService.update(url, obj_especialidad.id, obj_especialidad)
      const nuevaEspecilidad = respuesta.objeto
      const index = especialidades.value.findIndex(esp => esp.id === obj_especialidad.id)
      if (index !== -1) {
        especialidades.value[index] = { ...nuevaEspecilidad }
      }
      especialidad.value = { ...nuevaEspecilidad }
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  async function destroy(id: number) {
    try {
      const respuesta = await ApiService.destroy(url, id)
      especialidades.value = especialidades.value.filter(esp => esp.id !== id);    
      especialidad.value = { ...defaultEspecialidad }
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  function reset() {
    especialidades.value = []
    especialidad.value = { ...defaultEspecialidad }
  }

  return { reset, defaultEspecialidad, especialidades, especialidad, buscar_especialidad, getAll, getOne, create, update, destroy }
})

export default useEspecialidadesStore