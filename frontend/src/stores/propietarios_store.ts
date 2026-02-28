import type { Propietario } from '@/interface/Propietario'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/ApiService'

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
    if (busqueda) 
      propietario.value = { ...busqueda }
    else
      try {
        await getOne(id)
        return propietario.value
      } catch (error) {
        throw error 
      }
    return propietario.value
  }
  async function getAll() {
    try {
      // Solicitar el listado de propietarios.
      propietarios.value = await ApiService.getAll(url) || []
    } catch (error: any) {
      propietarios.value = []
      throw error
    }
  }
  async function getOne(id: number) {
    try {
      const respuesta = await ApiService.getOne(url, id)
      if (respuesta && respuesta.id)
        // Respuesta tiene el propietario.
        propietario.value = respuesta 
      else
        propietario.value = {...defaultPropietario}
    } catch (error: any) {
      propietario.value = {...defaultPropietario}
      throw error
    }
  }
  async function create(obj_propietario: Propietario) {
    try {
      const respuesta = await ApiService.create(url, obj_propietario)
      if (respuesta && respuesta.objeto) {
        const nuevoPropietario = respuesta.objeto
        propietarios.value.push({ ...nuevoPropietario })
        propietarios.value = { ...nuevoPropietario }
        return nuevoPropietario
      } 
      throw new Error('Respuesta de creación inesperada del servidor (cuerpo malformado).')
    } catch (error: any) {
      throw error
    }
  }
  async function update(obj_propietario: Propietario) {
    if (!obj_propietario.id)
      throw new Error('Propietario: No se puede actualizar un propietario sin ID.')
    try {
      const respuesta = await ApiService.update(url, obj_propietario.id, obj_propietario)
      if (respuesta && respuesta.estado === 'ok' && respuesta.objeto) {
        const nuevoPropietario = respuesta.objeto
        const index = propietarios.value.findIndex(prop => 
          prop.id === obj_propietario.id)
        if (index !== -1) {
          propietarios.value[index] = { ...nuevoPropietario }
        }
        propietario.value = { ...nuevoPropietario }
        return nuevoPropietario
      }
      throw new Error(respuesta.mensaje || 'Error al actualizar.')
    } catch (error: any) {
      throw error
    }
  }
  async function destroy(id: number) {
    try {
      await ApiService.destroy(url, id)
      propietarios.value = propietarios.value.filter(prop =>
        prop.id !== id);    
      propietario.value = {...defaultPropietario}
      return true
    } catch (error: any) {
      throw error
    }
  }
  function reset() {
    propietarios.value = []
    propietario.value = {...defaultPropietario}
  }
  return { reset, defaultPropietario, propietarios, propietario, buscar_propietario, getAll, getOne, create, update, destroy }
})
export default usePropietariosStore