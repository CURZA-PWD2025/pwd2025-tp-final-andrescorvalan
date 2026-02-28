import type { Veterinario } from '@/interface/Veterinario'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/ApiService'

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

  async function buscar_veterinario(id: number) {
    const busqueda = veterinarios.value.find((veterinario) => veterinario.id === id)
    if (busqueda) 
      veterinario.value =  { ...busqueda }
    else
      try {
        await getOne(id)
        return veterinario.value
      } catch (error) {
        throw error 
      }
    return veterinario.value
  }

  function reset_veterinario() {
    veterinario.value = { ...defaultVeterinario }
  }

  async function getAll() {
    try {
      // Solicitar el listado de veterinarios.
      veterinarios.value = await ApiService.getAll(url) || []
    } catch (error: any) {
      veterinarios.value = []
      throw error
    }
  }

  async function getOne(id: number) {
    try {
      const respuesta = await ApiService.getOne(url, id)
      if (respuesta && respuesta.id)
        // Respuesta tiene la veterinario.
        veterinario.value = respuesta 
      else
        veterinario.value = { ...defaultVeterinario }
    } catch (error: any) {
      veterinario.value = { ...defaultVeterinario }
      throw error // Propagar el error limpio
    }
  }

  async function create(obj_veterinario: Veterinario) {
    try {
      const respuesta = await ApiService.create(url, obj_veterinario)
      if (respuesta && respuesta.objeto) {
        await getAll()
        // Respuesta.objeto tiene la veterinario creada.
        veterinario.value = respuesta.objeto 
        return respuesta.objeto
      } else
        throw new Error('Respuesta de creación inesperada del servidor (cuerpo malformado).')
    } catch (error: any) {
      throw error
    }
  }

  async function update(obj_veterinario: Veterinario) {
    if (!obj_veterinario.id)
      throw new Error('Veterinario: No se puede actualizar un veterinario sin ID.')
    try {
      const respuesta = await ApiService.update(url, obj_veterinario.id, obj_veterinario)
      if (respuesta && respuesta.estado === 'ok' && respuesta.objeto) {
        await getAll()
        if (respuesta.objeto) {
            veterinario.value = respuesta.objeto
            return respuesta.objeto
        }
        return respuesta.mensaje
      } else
        throw new Error('Respuesta de actualización inesperada del servidor (cuerpo malformado).')
    } catch (error: any) {
      throw error
    }
  }

  async function destroy(id: number) {
    try {
      await ApiService.destroy(url, id)
      await getAll()
      veterinario.value = {...defaultVeterinario}
      return true
    } catch (error: any) {
      throw error
    }
  }
  function reset() {
    veterinarios.value = []
    veterinario.value = {...defaultVeterinario}
  }
  return { reset, defaultVeterinario, veterinarios, veterinario, buscar_veterinario, reset_veterinario, getAll, getOne, create, update, destroy }
})

export default useVeterinariosStore