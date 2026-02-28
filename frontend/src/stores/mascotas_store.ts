import type { Mascota } from '@/interface/Mascota'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/ApiService'

const url = 'mascotas/'

const defaultMascota: Mascota = {
  id: 0,
  nombre: '',
  fecha_nac: '',
  propietario: {id: 0, nombre: '', apellido: '', dni: '', telefono: '',email: ''},
  especie: {id: 0, nombre: '', nombre_cientifico: '', clase: ''},
}

const useMascotasStore = defineStore('mascotas', () => {

  const mascotas = ref<Array<Mascota>>([])
  const mascota = ref<Mascota>({ ...defaultMascota })

  async function buscar_mascota(id: number) {
    const busqueda = mascotas.value.find((mascota) => mascota.id === id)
    if (busqueda) 
      mascota.value = { ...busqueda }
    else
      try {
        await getOne(id)
        return mascota.value
      } catch (error) {
        throw error 
      }
    return mascota.value
  }

  function reset_mascota() {
    mascota.value = { ...defaultMascota }
  }

  async function getAll() {
    try {
      // Solicitar el listado de mascotas.
      console.log("previo a apiservice.getall")
      mascotas.value = await ApiService.getAll(url) || []
    } catch (error: any) {
      mascotas.value = []
      throw error
    }
  }

  async function getOne(id: number) {
    try {
      const respuesta = await ApiService.getOne(url, id)
      if (respuesta && respuesta.id)
        // Respuesta tiene la mascota.
        mascota.value = respuesta 
      else
        mascota.value = { ...defaultMascota }
    } catch (error: any) {
       mascota.value = { ...defaultMascota }
      throw error // Propagar el error limpio
    }
  }

  async function create(obj_mascota: Mascota) {
    try {
      const respuesta = await ApiService.create(url, 
        {
          'nombre': obj_mascota.nombre,
          'fecha_nac': obj_mascota.fecha_nac,
          'propietario_id': obj_mascota.propietario.id,
          'especie_id': obj_mascota.especie.id
        }
      )
      if (respuesta && respuesta.estado === 'ok' && respuesta.objeto) {
        await getAll()
        // Respuesta.objeto tiene la mascota creada.
        mascota.value = respuesta.objeto 
        return respuesta.objeto
      } else {
        throw new Error('Respuesta de creación inesperada del servidor (cuerpo malformado).')
      }
    } catch (error: any) {
      throw error
    }
  }

  async function update(obj_mascota: Mascota) {
    if (!obj_mascota.id)
      throw new Error('Mascota: No se puede actualizar una mascota sin ID.')
    try {
      console.log('Actualizando mascota zzzz:', {
          'nombre': obj_mascota.nombre,
          'fecha_nac': obj_mascota.fecha_nac,
          'propietario_id': obj_mascota.propietario.id,
          'especie_id': obj_mascota.especie.id
        })
      const respuesta = await ApiService.update(url, obj_mascota.id,  
        {
          'nombre': obj_mascota.nombre,
          'fecha_nac': obj_mascota.fecha_nac,
          'propietario_id': obj_mascota.propietario.id,
          'especie_id': obj_mascota.especie.id
        }
      )
      if (respuesta && respuesta.estado === 'ok' && respuesta.objeto) {
        await getAll()
        if (respuesta.objeto) {
            mascota.value = respuesta.objeto
            return respuesta.objeto
        }
        return respuesta.mensaje
      } else {
          throw new Error('Respuesta de actualización inesperada del servidor (cuerpo malformado).')
      }
    } catch (error: any) {
      throw error
    }
  }

  async function destroy(id: number) {
    try {
      await ApiService.destroy(url, id)
      await getAll()
      return true
    } catch (error: any) {
      throw error
    }
  }
  function reset() {
    mascotas.value = []
    mascota.value = {...defaultMascota}
  }
  return { reset, defaultMascota, mascotas, mascota, buscar_mascota, reset_mascota, getAll, getOne, create, update, destroy }
})

export default useMascotasStore