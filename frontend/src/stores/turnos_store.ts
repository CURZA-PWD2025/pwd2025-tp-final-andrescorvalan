import type { Turno } from '@/interface/turno'
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import ApiService from '@/services/api_service'
import type { ApiRespuesta } from '@/interface/api_respuesta'


const url = 'turnos/'

const obtenerFechaLocal = () => {
  const ahora = new Date()

  const fecha = ahora.toLocaleDateString('sv-SE') 
  const hora = ahora.toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' })
  return `${fecha}T${hora}` 
}

const defaultTurno: Turno = {
  id: 0,
  fecha_hora: obtenerFechaLocal(),
  motivo: '',
  estado: 'Pendiente',
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

const useTurnosStore = defineStore('turnos', () => {

  const incluirHistorial = ref(false)

  const turno = ref<Turno>({ ...defaultTurno })

  const turnos_proximos = ref<Array<Turno>>([])
  const turnos_historial = ref<Array<Turno>>([])

  const turnos = computed(() => {
    return [...turnos_proximos.value, ...turnos_historial.value];
  });

  async function buscar_turno(id: number): Promise<ApiRespuesta> {
    try {
      const respuesta = await getOne(id)
      respuesta.objeto = respuesta.datos 
      turno.value = { ...respuesta.objeto }
      return respuesta
    } catch (error) {
      throw error 
    }
  }
  
  async function getProximos() {
    try {
      const respuesta = await ApiService.getAll(url+'proximos/')
      turnos_proximos.value = respuesta.datos || []
      return respuesta
    } catch (error: any) {
      turnos_proximos.value = []
      throw error
    }
  }
  
  async function getHistorial() {
    try {
        const respuesta = await ApiService.getAll(url+'historial/')
        turnos_historial.value = respuesta.datos || []
        incluirHistorial.value = true
        return respuesta
    } catch (error: any) {
      turnos_historial.value = []
      incluirHistorial.value = false
      throw error
    }
  }

  async function getOne(id: number) {
    try {
      const respuesta = await ApiService.getOne(url, id)
      if (!respuesta.datos) 
        throw new Error('No se encontraron datos');
      else {
        turno.value = respuesta.datos
        return respuesta
      }
    } catch (error: any) {
      turno.value = { ...defaultTurno }
      throw error
    }
  }

  async function create(obj_turno: Turno) {
    try {
      const respuesta = await ApiService.create(url, 
        {
          'fecha_hora': obj_turno.fecha_hora,
          'motivo': obj_turno.motivo,
          'estado': obj_turno.estado,
          'mascota_id': obj_turno.mascota.id,
          'veterinario_id': obj_turno.veterinario.id
        }
      )
      const nuevoTurno = respuesta.objeto
      turnos_proximos.value.unshift({ ...nuevoTurno })
      turno.value = { ...nuevoTurno }
      await getProximos()
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  async function update(obj_turno: Turno) {
    if (!obj_turno.id)
      throw {
        estado: 'error',
        mensaje: 'Turno: No se puede actualizar un turno sin ID.'
      }
    try {
      const respuesta = await ApiService.update(url, obj_turno.id,  
        {
          'id': obj_turno.id,
          'fecha_hora': obj_turno.fecha_hora,
          'motivo': obj_turno.motivo,
          'estado': obj_turno.estado,
          'mascota_id': obj_turno.mascota.id,
          'veterinario_id': obj_turno.veterinario.id
        }
      )
      const nuevaTurno = respuesta.objeto
      const index = turnos_proximos.value.findIndex(masc => masc.id === obj_turno.id)
      if (index !== -1) {
        turnos_proximos.value[index] = { ...nuevaTurno }
      } else {
        const index = turnos_historial.value.findIndex(masc => masc.id === obj_turno.id)
        if (index !== -1) {
          turnos_historial.value[index] = { ...nuevaTurno }
        }
      }
      turno.value = { ...nuevaTurno }
      await getProximos()
      if (incluirHistorial.value) {
        await getHistorial()
      }
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  async function destroy(id: number) {
    try {
      const respuesta = await ApiService.destroy(url, id)
      turnos_proximos.value = turnos_proximos.value.filter(t => t.id !== id);
      turnos_historial.value = turnos_historial.value.filter(t => t.id !== id);      turno.value = { ...defaultTurno }
      await getProximos()
      return respuesta
    } catch (error: any) {
      throw error
    }
  }

  function reset() {
    turnos_proximos.value = []
    turnos_historial.value = []
    turno.value = { ...defaultTurno }
  }
  
  return { incluirHistorial,reset, defaultTurno, turnos,
     turnos_proximos, turnos_historial, turno, buscar_turno, 
     getProximos, getHistorial,getOne, create, update, destroy }
})

export default useTurnosStore