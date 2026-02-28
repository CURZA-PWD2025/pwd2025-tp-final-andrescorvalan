import type { Especie } from '@/interface/Especie'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/ApiService'

const url = 'especies/'
const defaultEspecie: Especie = {
  id: 0,
  nombre: '',
  nombre_cientifico: '',
  clase: ''
}
const useEspeciesStore = defineStore('especies', () => {

  const especies = ref<Array<Especie>>([])
  const especie = ref<Especie>({ ...defaultEspecie })

  async function buscar_especie(id: number) {
    const busqueda = especies.value.find((esp) => esp.id === id)
    if (busqueda) 
      especie.value = { ...busqueda }
    else
      try {
        await getOne(id)
        return especie.value
      } catch (error) {
        throw error 
      }
    return especie.value
  }
  async function getAll() {
    try {
      // Solicitar el listado de especies.
      especies.value = await ApiService.getAll(url) || []
    } catch (error: any) {
      especies.value = []
      throw error
    }
  }
  async function getOne(id: number) {
    try {
      const respuesta = await ApiService.getOne(url, id)
      if (respuesta && respuesta.id)
        // Respuesta tiene la especie.
        especie.value = respuesta 
      else
        especie.value = {...defaultEspecie}
    } catch (error: any) {
      especie.value = {...defaultEspecie}
      throw error // Propagamos el error limpio
    }
  }
  async function create(obj_especie: Especie) {
    try {
      const respuesta = await ApiService.create(url, obj_especie)
      if (respuesta && respuesta.objeto) {
        const nuevaEspecie = respuesta.objeto
        especies.value.push({ ...nuevaEspecie })
        especie.value = { ...nuevaEspecie }
        return nuevaEspecie
      } 
      throw new Error('Respuesta de creación inesperada del servidor (cuerpo malformado).')
    } catch (error: any) {
      throw error
    }
  }
  async function update(obj_especie: Especie) {
    if (!obj_especie.id)
      throw new Error('Especie: No se puede actualizar un especie sin ID.')
    try {
      const respuesta = await ApiService.update(url, obj_especie.id, obj_especie)
      if (respuesta && respuesta.estado === 'ok' && respuesta.objeto) {
        const nuevaEspecie = respuesta.objeto
        const index = especies.value.findIndex(esp => 
          esp.id === obj_especie.id)
        if (index !== -1) {
          especies.value[index] = { ...nuevaEspecie }
        }
        especie.value = { ...nuevaEspecie }
        return nuevaEspecie
      }
      throw new Error(respuesta.mensaje || 'Error al actualizar.')
    } catch (error: any) {
      throw error
    }
  }
  async function destroy(id: number) {
    try {
      await ApiService.destroy(url, id)
      especies.value = especies.value.filter(esp =>
        esp.id !== id);    
      especie.value = {...defaultEspecie}
      return true
    } catch (error: any) {
      throw error
    }
  }
  function reset() {
    especies.value = []
    especie.value = {...defaultEspecie}
  }
  return { reset, defaultEspecie, especies, especie, buscar_especie, getAll, getOne, create, update, destroy }
})
export default useEspeciesStore