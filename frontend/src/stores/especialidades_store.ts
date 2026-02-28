import type { Especialidad } from '@/interface/Especialidad'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/ApiService'

const url = 'especialidades/'
const defaultEspecialidad: Especialidad = {
  id: 0,
  nombre: '',
  descripcion: ''
}
const useEspecialidadesStore = defineStore('especialidades', () => {

  const especialidades = ref<Array<Especialidad>>([])
  const especialidad = ref<Especialidad>({ ...defaultEspecialidad })

  async function buscar_especialidad(id: number) {
    const busqueda = especialidades.value.find((esp) => esp.id === id)
    if (busqueda) 
      especialidad.value = { ...busqueda }
    else
      try {
        await getOne(id)
        return especialidad.value
      } catch (error) {
        throw error 
      }
    return especialidad.value
  }
  async function getAll() {
    try {
      // Solicitar el listado de especialidades.
      especialidades.value = await ApiService.getAll(url) || []
    } catch (error: any) {
      especialidades.value = []
      throw error
    }
  }
  async function getOne(id: number) {
    try {
      const respuesta = await ApiService.getOne(url, id)
      if (respuesta && respuesta.id)
        // Respuesta tiene la especialidad.
        especialidad.value = respuesta 
      else
        especialidad.value = {...defaultEspecialidad}
    } catch (error: any) {
      console.error('Error en getOne:', error.message) 
      especialidad.value = {...defaultEspecialidad}
      throw error // Propagamos el error limpio
    }
  }
  async function create(obj_especialidad: Especialidad) {
    try {
      const respuesta = await ApiService.create(url, obj_especialidad)
      if (respuesta && respuesta.objeto) {
        const nuevaEspecialidad = respuesta.objeto
        especialidades.value.push({ ...nuevaEspecialidad })
        especialidad.value = { ...nuevaEspecialidad }
        return nuevaEspecialidad
      }
      throw new Error('Respuesta de creación inesperada del servidor (cuerpo malformado).')
    } catch (error: any) {
      throw error
    }
  }
  async function update(obj_especialidad: Especialidad) {
    if (!obj_especialidad.id)
      throw new Error('Especialidad: No se puede actualizar un especialidad sin ID.')
    try {
      const respuesta = await ApiService.update(url, obj_especialidad.id, obj_especialidad)
      if (respuesta && respuesta.estado === 'ok' && respuesta.objeto) {
        const nuevaEspecilidad = respuesta.objeto
        const index = especialidades.value.findIndex(esp => 
            esp.id === obj_especialidad.id)
        if (index !== -1) {
          especialidades.value[index] = { ...nuevaEspecilidad }
        }
        especialidad.value = { ...nuevaEspecilidad }
        return nuevaEspecilidad
      }
      throw new Error(respuesta.mensaje || 'Error al actualizar.')
    } catch (error: any) {
      throw error
    }
  }
  async function destroy(id: number) {
    try {
      await ApiService.destroy(url, id)
      especialidades.value = especialidades.value.filter(esp =>
        esp.id !== id);    
      especialidad.value = {...defaultEspecialidad}
      return true
    } catch (error: any) {
      throw error
    }
  }
  function reset() {
    especialidades.value = []
    especialidad.value = {...defaultEspecialidad}
  }
  return { reset, defaultEspecialidad, especialidades, especialidad, buscar_especialidad, getAll, getOne, create, update, destroy }
})
export default useEspecialidadesStore