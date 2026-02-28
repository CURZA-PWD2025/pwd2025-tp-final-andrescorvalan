<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Icon } from "@iconify/vue"
import useEspecialidadesStore from '../../stores/especialidades_store'
import axios from 'axios'

const router = useRouter()
const { create, defaultEspecialidad } = useEspecialidadesStore()
const nuevaEspecialidad = ref({ ...defaultEspecialidad })
const mensaje = ref('')
const estado = ref('')

const tipoMensaje = computed(() => ({
  'mensaje-procesando': estado.value === 'procesando',
  'mensaje-exito': estado.value === 'exito',
  'mensaje-error': estado.value === 'error'
}));

function go_especialidades_list() {
    router.push({ name: 'especialidades_list' })
}

function limpiar_formulario() {
  nuevaEspecialidad.value = { ...defaultEspecialidad }
}

onMounted(() => {
  limpiar_formulario()
})

async function nueva_especialidad() {
  if (!nuevaEspecialidad.value.nombre || !nuevaEspecialidad.value.descripcion) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error'
    return
  }
  mensaje.value = 'Intentando crear la especialidad...'
  estado.value = 'procesando'
  try {
    await create(nuevaEspecialidad.value)
    mensaje.value = '¡Especialidad creada correctamente! Puede cargar otra.'
    estado.value = 'exito'
    limpiar_formulario()
  } catch (error: any) {
    let errorMensaje = ''
    if (axios.isAxiosError(error)) {
      if (error.response) {
        errorMensaje = error.response.data?.mensaje || `Error del servidor (Código: ${error.response.status}).`
      } else {
        errorMensaje = 'No se pudo conectar al servidor. Verifique su conexión.'
      }
    } else {
      errorMensaje = error.message || 'Ocurrió un error inesperado.'
    }
    mensaje.value = errorMensaje
    estado.value = 'error'
  } finally {
    setTimeout(() => {
      mensaje.value = ''
      estado.value = ''
    }, 4000)
  }
}
</script>

<template>
  <section class="grud">
    <header class="grud-encabezado">
      <h2>Crear Especialidad</h2>
      <button @click="go_especialidades_list" class="boton boton-back">
        <Icon class="icono" icon="mdi:arrow-left"/>
        Volver al Listado
      </button>
    </header>
    <!-- Mensajes -->
    <div class="grud-mensaje">
      <transition name="mensaje-fade" mode="out-in">
        <div v-if="mensaje" :key="mensaje" role="alert" class="mensaje-alerta" :class="tipoMensaje">
          {{ mensaje }}
        </div>
      </transition>
    </div>
    <form @submit.prevent="nueva_especialidad" class="grud-frame">
      <div class="grud-field-group">
        <div class="grud-field">
          <label class="grud-field-name" for="nombre">
            Nombre: 
            <abbr class="grud-abbr" 
              title="Nombre de la especialidad (obligatorio)">*
            </abbr>
          </label>
          <input class="grud-input grud-data"
            id="nombre"
            type="text"
            v-model="nuevaEspecialidad.nombre"
            placeholder="Ej: Cirugía, Dermatología"
            maxlength="35"
            style="width: 42ch;"
            autofocus
            required/>
        </div>
        <div class="grud-field">
          <label class="grud-field-name" for="descripcion">
            Descripción: 
            <abbr class="grud-abbr" 
              title="Descripción de la especialidad (obligatorio)">*
            </abbr>
          </label>
            <textarea class="grud-input grud-data"
            id="descripcion"
            v-model="nuevaEspecialidad.descripcion"
            placeholder="Ej: Clínica de Pequeños Animales"
            maxlength="100"
            rows="3"
            style="width: 42ch; resize: none;"
            required></textarea>
        </div>
      </div>
      <div class="grud-botones">
        <button class="boton boton-accept" type="submit" :disabled="estado === 'procesando'">
          <Icon class="icono" icon="mdi:content-save-plus"/>
          {{ estado === 'procesando' ? 'Guardando...' : 'Crear Especialidad' }}
        </button>
        <button class="boton boton-reset" type="button" @click="limpiar_formulario" :disabled="estado === 'procesando'">
          <Icon class="icono" icon="mdi:broom"/>
          Limpiar Campos
        </button>
      </div>
    </form>
    <div v-if="estado === 'procesando'" class="deshabilitar-interaccion">
      <div class="ventana-emergente">
        <div class="icono-procesando"></div>
        <p>Procesando solicitud...</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
</style>