<script setup lang="ts">
  import { ref, toRefs, onMounted } from 'vue'
  import { Icon } from "@iconify/vue"
  
  import { useRoute, useRouter } from 'vue-router'
  const router = useRouter()
  const route = useRoute()
  
  import useTurnosStore from '@/stores/turnos_store'
  const { turno } = toRefs(useTurnosStore())
  const { buscar_turno, defaultTurno } = useTurnosStore()
  
  import ShowViewGenerico from '@/components//crud-generico/ShowViewGenerico.vue'

  const mensajeError = ref('')
  
  import type { Especialidad } from '@/interface/especialidad'

  const formatearFecha = (fechaStr: string) => {
    const date = new Date(fechaStr)
    return date.toLocaleDateString('es-AR', {day: '2-digit', month: '2-digit', year: 'numeric'});
  }; 

  const formatearFechaHora = (fechaStr: string) => {
    if (!fechaStr) return '---';
    const date = new Date(fechaStr);
    return date.toLocaleString('es-AR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  onMounted(async () => {
    const id = Number(route.params.id)
    if (isNaN(id)) {
      router.push({ name: 'turnos_list' })
      return
    }
    turno.value = { ...defaultTurno }
    try {
      await buscar_turno(id)
    } catch (error: any) {
      mensajeError.value = error.mensaje || 'No se encontró el turno.'
    }
  })
</script>

<template>
  <ShowViewGenerico
    titulo="Detalles del turno"
    :mensaje="mensajeError" 
    @volver="router.push({ name: 'turnos_proximos' })"
  >
    <template #detalles v-if="turno.id !== 0">
      <header class="ficha-encabezado">
        <Icon icon="mdi:medical-bag" class="ficha-logo" />
        <div>
          <h2>Datos del Turno</h2>
          <p>ID: {{ turno.id }}</p>
          <p>Fecha: {{ formatearFechaHora(turno.fecha_hora) }}</p>
          <p>Mascota: {{ turno.mascota.nombre }}</p>
          <p>Propietario: {{ turno.mascota.propietario.nombre }} {{ turno.mascota.propietario.apellido }}</p>
          <p>Motivo: >{{ turno.motivo }}</p>
          <p>Estado: <span :class="turno.estado.toLowerCase()">{{ turno.estado }}</span></p>
        </div>
      </header>
      <div class="ficha-detalles">
        <section class="ficha-tarjeta">
          <div class="ficha-tarjeta-titulo">
            <Icon icon="mdi:paw" /> Información de la Mascota
          </div>
          <div class="card-body">
            <div class="ficha-tarjeta-fila">
              <span>Nombre:</span>
              <strong>{{ turno.mascota.nombre }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Fecha Nacimiento:</span>
              <strong>{{ formatearFecha(turno.mascota.fecha_nac) }}</strong>
            </div>
           <div class="ficha-tarjeta-fila">
              <span>Sexo:</span>
              <strong>{{ turno.mascota.sexo }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Especie:</span>
              <strong>{{ turno.mascota.especie.nombre }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Nombre Científico:</span>
              <strong>{{ turno.mascota.especie.nombre_cientifico }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Clase:</span> 
              <strong>{{ turno.mascota.especie.clase }}</strong>
            </div>
          </div>
        </section>
        <section class="ficha-tarjeta">  
          <div class="ficha-tarjeta-titulo">
            <Icon icon="mdi:account-group" /> Datos del Propietario
          </div>
          <div class="card-body">
            <div class="ficha-tarjeta-fila">
              <span>Nombre:</span>
              <strong>{{ turno.mascota.propietario.nombre }} {{ turno.mascota.propietario.apellido }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>DNI:</span>
              <strong>{{ turno.mascota.propietario.dni }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Teléfono:</span>
              <strong>{{ turno.mascota.propietario.telefono }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Email:</span>
              <strong>{{ turno.mascota.propietario.email }}</strong>
            </div>
          </div>
        </section>
        
        <section class="ficha-tarjeta">  
          <div class="ficha-tarjeta-titulo">
            <Icon icon="mdi:doctor" /> Datos del Veterinario
          </div>
          <div class="card-body">
            <div class="ficha-tarjeta-fila">
              <span>Nombre:</span>
              <strong>{{ turno.veterinario.nombre }} {{ turno.veterinario.apellido }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Matricula:</span>
              <strong>{{ turno.veterinario.matricula }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Teléfono:</span>
              <strong>{{ turno.veterinario.telefono }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Email:</span>
              <strong>{{ turno.veterinario.email }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Especialidades:</span>
              <strong v-if="turno.veterinario.especialidades.length > 0">
                {{ (turno.veterinario.especialidades as Especialidad[]).map(e => e.nombre).join(', ') }}
              </strong>
              <strong v-else>
                Sin especialidades asignadas.
              </strong>
            </div>
          </div>
        </section>
      </div>
    </template>
  </ShowViewGenerico>
</template>

<style scoped>
 .pendiente {
    color: #0369a1;
  }
  .atendido {
    color: #15803d;
  }
  .ausente {
    color: magenta;
  }
</style>