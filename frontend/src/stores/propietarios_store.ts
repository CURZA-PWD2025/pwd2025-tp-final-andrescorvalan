import type { Propietario } from '@/interface/propietario'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/api_service'

const url = 'propietarios/'
const defaultPropietario: Propietario = {
  id: 0,
  nombre: '',
  apellido: '',
  dni: '',
  telefono: '',
  email: ''
}
const usePropietariosStore = defineStore('propietarios', () => {

  const propietarios = ref<Array<Propietario>>([])
  const propietario = ref<Propietario>({ ...defaultPropietario })

  async function buscar_propietario(id: number) {
    const busqueda = propietarios.value.find((propietario) => propietario.id === id)
    if (busqueda) {
      propietario.value = { ...busqueda }
      return { 
        estado:'ok', 
        objeto: propietario.value
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
      propietarios.value = respuesta.datos || []
      return respuesta
    } catch (error: any) {
      propietarios.value = []
      throw error
    }
  }

  async function getOne(id: number) {
    try {
      const respuesta = await ApiService.getOne(url, id)
      if (!respuesta.datos) 
        throw new Error('No se encontraron datos');
      else {
        propietario.value = respuesta.datos
        return respuesta
      }
    } catch (error: any) {
      propietario.value = { ...defaultPropietario }
      throw error
    }
  }

  async function create(obj_propietario: Propietario) {
    try {
      const respuesta = await ApiService.create(url, obj_propietario)
      const nuevoPropietario = respuesta.objeto
      propietarios.value.push({ ...nuevoPropietario })
      propietario.value = { ...nuevoPropietario }
      return respuesta
    } catch (error: any) {
      throw error
    }
  }
  
  async function update(obj_propietario: Propietario) {
    if (!obj_propietario.id)
      throw { 
        estado: 'error', 
        mensaje: 'Propietario: No se puede actualizar (ID no válido).' 
      }
    try {
      const respuesta = await ApiService.update(url, obj_propietario.id, obj_propietario)
      const nuevoPropietario = respuesta.objeto
      const index = propietarios.value.findIndex(prop => prop.id === obj_propietario.id)
      if (index !== -1) {
        propietarios.value[index] = { ...nuevoPropietario }
      }
      propietario.value = { ...nuevoPropietario }
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  async function destroy(id: number) {
    try {
      const respuesta = await ApiService.destroy(url, id)
      propietarios.value = propietarios.value.filter(prop => prop.id !== id);    
      propietario.value = { ...defaultPropietario }
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  function reset() {
    propietarios.value = []
    propietario.value = { ...defaultPropietario }
  }
  
  return { reset, defaultPropietario, propietarios, propietario, buscar_propietario, getAll, getOne, create, update, destroy }
})

export default usePropietariosStore