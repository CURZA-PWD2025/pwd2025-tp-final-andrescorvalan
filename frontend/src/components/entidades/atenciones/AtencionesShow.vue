<script setup lang="ts">
  import { ref, toRefs, onMounted } from 'vue'
  
  import { useRoute, useRouter } from 'vue-router'
  const router = useRouter()
  const route = useRoute()
  
  import useAtencionesStore from '@/stores/atenciones_store'
  const { atencion } = toRefs(useAtencionesStore())
  const { buscar_atencion, defaultAtencion } = useAtencionesStore()
  
  import ShowViewGenerico from '@/components//crud-generico/ShowViewGenerico.vue'

  const mensajeError = ref('')
  
  import type { Especialidad } from '@/interface/especialidad'

  const formatearFecha = (fechaStr: string) => {
    const date = new Date(fechaStr + 'T00:00:00')
    return date.toLocaleDateString('es-AR', {day: '2-digit', month: '2-digit', year: 'numeric'});
  };

  onMounted(async () => {
    const id = Number(route.params.id)
    if (isNaN(id)) {
      router.push({ name: 'atenciones_list' })
      return
    }
    atencion.value = { ...defaultAtencion }
    try {
      await buscar_atencion(id)
    } catch (error: any) {
      mensajeError.value = error.mensaje || 'No se encontró la atencion.'
    }
  })
</script>

<template>
  <ShowViewGenerico
    titulo="Detalles de la atencion"
    :mensaje="mensajeError" 
    @volver="router.push({ name: 'atenciones_list' })"
  >
    <template #detalles v-if="atencion.id !== 0">
      <header class="ficha-encabezado">
        <icon-mdi-medical-bag class="ficha-logo" />
        <div>
          <h2>Datos de la Atención Veterinaria</h2>
          <p>ID: {{ atencion.id }}</p>
          <p>Fecha: {{ formatearFecha(atencion.fecha) }}</p>
          <p>Mascota: {{ atencion.mascota.nombre }}</p>
          <p>Propietario: {{ atencion.mascota.propietario.nombre }} {{ atencion.mascota.propietario.apellido }}</p>
          <p>Diagnóstico: {{ atencion.diagnostico }}</p>
          <p>Tratamiento: {{ atencion.tratamiento }}</p>
          <p>Observaciones: {{ atencion.observaciones }}</p>
        </div>
      </header>
      <div class="ficha-detalles">
        <section class="ficha-tarjeta">
          <div class="ficha-tarjeta-titulo">
            <icon-mdi-paw /> Información de la Mascota
          </div>
          <div class="card-body">
            <div class="ficha-tarjeta-fila">
              <span>Nombre:</span>
              <strong>{{ atencion.mascota.nombre }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Fecha Nacimiento:</span>
              <strong>{{ formatearFecha(atencion.mascota.fecha_nac) }}</strong>
            </div>
           <div class="ficha-tarjeta-fila">
              <span>Sexo:</span>
              <strong>{{ atencion.mascota.sexo }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Especie:</span>
              <strong>{{ atencion.mascota.especie.nombre }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Nombre Científico:</span>
              <strong>{{ atencion.mascota.especie.nombre_cientifico }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Clase:</span> 
              <strong>{{ atencion.mascota.especie.clase }}</strong>
            </div>
          </div>
        </section>
        <section class="ficha-tarjeta">  
          <div class="ficha-tarjeta-titulo">
            <icon-mdi-account-group/> Datos del Propietario
          </div>
          <div class="card-body">
            <div class="ficha-tarjeta-fila">
              <span>Nombre:</span>
              <strong>{{ atencion.mascota.propietario.nombre }} {{ atencion.mascota.propietario.apellido }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>DNI:</span>
              <strong>{{ atencion.mascota.propietario.dni }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Teléfono:</span>
              <strong>{{ atencion.mascota.propietario.telefono }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Email:</span>
              <strong>{{ atencion.mascota.propietario.email }}</strong>
            </div>
          </div>
        </section>
        
        <section class="ficha-tarjeta">  
          <div class="ficha-tarjeta-titulo">
            <icon-mdi-doctor/> Datos del Veterinario
          </div>
          <div class="card-body">
            <div class="ficha-tarjeta-fila">
              <span>Nombre:</span>
              <strong>{{ atencion.veterinario.nombre }} {{ atencion.veterinario.apellido }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Matricula:</span>
              <strong>{{ atencion.veterinario.matricula }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Teléfono:</span>
              <strong>{{ atencion.veterinario.telefono }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Email:</span>
              <strong>{{ atencion.veterinario.email }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Especialidades:</span>
              <strong v-if="atencion.veterinario.especialidades.length > 0">
                {{ (atencion.veterinario.especialidades as Especialidad[]).map(e => e.nombre).join(' ') }}
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
</style>