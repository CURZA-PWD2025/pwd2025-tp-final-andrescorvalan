import type { Atencion } from '@/interface/atencion'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/api_service'
import type { ApiRespuesta } from '@/interface/api_respuesta'

const url = 'atenciones/'

const defaultAtencion: Atencion = {
  id: 0,
  fecha: new Date().toISOString().split('T')[0] || '',
  diagnostico: '',
  tratamiento: '',
  observaciones: '',
  mascota: {
    id: 0,
    nombre: '',
    fecha_nac: '',
    sexo: '',
    propietario: { id: 0, nombre: '', apellido: '', dni: '', telefono: '', email: '' },
    especie: { id: 0, nombre: '', nombre_cientifico: '', clase: '', esperanza_vida: 0, exotica: 0 },
  },
  veterinario: {
    id: 0,
    nombre: '',
    apellido: '',
    matricula: '',
    telefono: '',
    email: '',
    especialidades: []
  }
}

const useAtencionesStore = defineStore('atenciones', () => {

  const atenciones = ref<Array<Atencion>>([])
  const atencion = ref<Atencion>({ ...defaultAtencion })

  async function buscar_atencion(id: number): Promise<ApiRespuesta> {
      const encontrado = atenciones.value.find((atencion) => atencion.id === id)
      if (encontrado) {
        atencion.value = { ...encontrado }
        return {
          estado: 'ok',
          mensaje: 'Encontrado localmente',
          objeto: atencion.value
        }
      }
      try {
        const respuesta = await getOne(id) 
        respuesta.objeto = respuesta.datos 
        atencion.value = { ...respuesta.objeto }
        return respuesta
      } catch (error) {
        throw error 
      }
    }

  async function getAll() {
    try {
      const respuesta = await ApiService.getAll(url)
      atenciones.value = respuesta.datos || []
      return respuesta
    } catch (error: any) {
      atenciones.value = []
      throw error
    }
  }

  async function getOne(id: number) {
    try {
      const respuesta = await ApiService.getOne(url, id)
      if (!respuesta.datos) 
        throw new Error('No se encontraron datos');
      else {
        atencion.value = respuesta.datos
        return respuesta
      }
    } catch (error: any) {
      atencion.value = { ...defaultAtencion }
      throw error
    }
  }

  async function getByMascota(id: number) {
    try {
      const respuesta = await ApiService.getByRelation(url+'mascota/', id)
      atenciones.value = respuesta.datos || []
      return respuesta
    } catch (error: any) {
      atenciones.value = []
      throw error
    }
  }

  async function create(obj_atencion: Atencion) {
    try {
      const respuesta = await ApiService.create(url, 
        {
          'fecha': obj_atencion.fecha,
          'diagnostico': obj_atencion.diagnostico,
          'tratamiento': obj_atencion.tratamiento,
          'observaciones': obj_atencion.observaciones,
          'mascota_id': obj_atencion.mascota.id,
          'veterinario_id': obj_atencion.veterinario.id
        }
      )
      const nuevaAtencion = respuesta.objeto
      atenciones.value.unshift({ ...nuevaAtencion })
      atencion.value = { ...nuevaAtencion }
      await getAll()
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  async function update(obj_atencion: Atencion) {
    if (!obj_atencion.id)
      throw {
        estado: 'error',
        mensaje: 'Atencion: No se puede actualizar una atencion sin ID.'
      }
    try {
      const respuesta = await ApiService.update(url, obj_atencion.id,  
        {
          'id': obj_atencion.id,
          'fecha': obj_atencion.fecha,
          'diagnostico': obj_atencion.diagnostico,
          'tratamiento': obj_atencion.tratamiento,
          'observaciones': obj_atencion.observaciones,
          'mascota_id': obj_atencion.mascota.id,
          'veterinario_id': obj_atencion.veterinario.id
        }
      )
      const nuevaAtencion = respuesta.objeto
      const index = atenciones.value.findIndex(masc => masc.id === obj_atencion.id)
      if (index !== -1) {
        atenciones.value[index] = { ...nuevaAtencion }
      }
      atencion.value = { ...nuevaAtencion }
      await getAll()
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  async function destroy(id: number) {
    try {
      const respuesta = await ApiService.destroy(url, id)
      atenciones.value = atenciones.value.filter(masc => masc.id !== id);    
      atencion.value = { ...defaultAtencion }
      await getAll()
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  function reset() {
    atenciones.value = []
    atencion.value = { ...defaultAtencion }
  }
  
  return { reset, defaultAtencion, atenciones, atencion, buscar_atencion, getAll, getOne, getByMascota, create, update, destroy }
})

export default useAtencionesStore