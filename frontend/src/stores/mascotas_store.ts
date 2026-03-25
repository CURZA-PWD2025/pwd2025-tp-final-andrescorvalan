import type { Mascota } from '@/interface/mascota'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/api_service'

const url = 'mascotas/'

const defaultMascota: Mascota = {
  id: 0,
  nombre: '',
  fecha_nac: '',
  sexo:'',
  propietario: {id: 0, nombre: '', apellido: '', dni: '', telefono: '',email: ''},
  especie: {id: 0, nombre: '', nombre_cientifico: '', clase: '', esperanza_vida:0, exotica: 0},
}

const useMascotasStore = defineStore('mascotas', () => {

  const mascotas = ref<Array<Mascota>>([])
  const mascota = ref<Mascota>({ ...defaultMascota })

  async function buscar_mascota(id: number) {
    const busqueda = mascotas.value.find((mascota) => mascota.id === id)
    if (busqueda) {
      mascota.value = { ...busqueda }
      return { 
        estado:'ok', 
        objeto: mascota.value
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
      mascotas.value = respuesta.datos || []
      return respuesta
    } catch (error: any) {
      mascotas.value = []
      throw error
    }
  }

  async function getOne(id: number) {
    try {
      const respuesta = await ApiService.getOne(url, id)
      if (!respuesta.datos) 
        throw new Error('No se encontraron datos');
      else {
        mascota.value = respuesta.datos
        return respuesta
      }
    } catch (error: any) {
       mascota.value = { ...defaultMascota }
      throw error
    }
  }

  async function create(obj_mascota: Mascota) {
    try {
      const respuesta = await ApiService.create(url, 
        {
          'nombre': obj_mascota.nombre,
          'fecha_nac': obj_mascota.fecha_nac,
          'sexo': obj_mascota.sexo,
          'propietario_id': obj_mascota.propietario.id,
          'especie_id': obj_mascota.especie.id
        }
      )
      const nuevaMascota = respuesta.objeto
      mascotas.value.push({ ...nuevaMascota })
      mascota.value = { ...nuevaMascota }
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  async function update(obj_mascota: Mascota) {
    if (!obj_mascota.id)
      throw {
        estado: 'error',
        mensaje: 'Mascota: No se puede actualizar una mascota sin ID.'
      }
    try {
      const respuesta = await ApiService.update(url, obj_mascota.id,  
        {
          'nombre': obj_mascota.nombre,
          'fecha_nac': obj_mascota.fecha_nac,
          'sexo': obj_mascota.sexo,
          'propietario_id': obj_mascota.propietario.id,
          'especie_id': obj_mascota.especie.id
        }
      )
      const nuevaMascota = respuesta.objeto
      const index = mascotas.value.findIndex(masc => masc.id === obj_mascota.id)
      if (index !== -1) {
        mascotas.value[index] = { ...nuevaMascota }
      }
      mascota.value = { ...nuevaMascota }
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  async function destroy(id: number) {
    try {
      const respuesta = await ApiService.destroy(url, id)
      mascotas.value = mascotas.value.filter(masc => masc.id !== id);    
      mascota.value = { ...defaultMascota }
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  function reset() {
    mascotas.value = []
    mascota.value = { ...defaultMascota }
  }
  
  return { reset, defaultMascota, mascotas, mascota, buscar_mascota, getAll, getOne, create, update, destroy }
})

export default useMascotasStore