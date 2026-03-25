import type { Especie } from '@/interface/especie'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/api_service'

const url = 'especies/'
const defaultEspecie: Especie = {
  id: 0,
  nombre: '',
  nombre_cientifico: '',
  clase: '',
  esperanza_vida: 0,
  exotica: 0
}
const useEspeciesStore = defineStore('especies', () => {

  const especies = ref<Array<Especie>>([])
  const especie = ref<Especie>({ ...defaultEspecie })

  async function buscar_especie(id: number) {
    const busqueda = especies.value.find((esp) => esp.id === id)
    if (busqueda) {
      especie.value = { ...busqueda }
      return { 
        estado:'ok', 
        objeto: especie.value
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
      especies.value = respuesta.datos || []
      return respuesta
    } catch (error: any) {
      especies.value = []
      throw error
    }
  }

  async function getOne(id: number) {
    try {
      const respuesta = await ApiService.getOne(url, id)
      if (!respuesta.datos) 
        throw new Error('No se encontraron datos');
      else {
        especie.value = respuesta.datos
        return respuesta
      }
    } catch (error: any) {
      especie.value = { ...defaultEspecie }
      throw error
    }
  }

  async function create(obj_especie: Especie) {
    try {
      const respuesta = await ApiService.create(url, obj_especie)
      const nuevaEspecie = respuesta.objeto
      especies.value.push({ ...nuevaEspecie })
      especie.value = { ...nuevaEspecie }
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  async function update(obj_especie: Especie) {
    if (!obj_especie.id)
      throw {
        estado: 'error', 
        mensaje: 'Especie: No se puede actualizar (ID no válido).' 
      }
    try {
      const respuesta = await ApiService.update(url, obj_especie.id, obj_especie)
      const nuevaEspecie = respuesta.objeto
      const index = especies.value.findIndex(prop => prop.id === obj_especie.id)
      if (index !== -1) {
        especies.value[index] = { ...nuevaEspecie }
      }
      especie.value = { ...nuevaEspecie }
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  async function destroy(id: number) {
    try {
      const respuesta = await ApiService.destroy(url, id)
      especies.value = especies.value.filter(esp => esp.id !== id);    
      especie.value = { ...defaultEspecie }
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  function reset() {
    especies.value = []
    especie.value = { ...defaultEspecie }
  }

  return { reset, defaultEspecie, especies, especie, buscar_especie, getAll, getOne, create, update, destroy }
})

export default useEspeciesStore