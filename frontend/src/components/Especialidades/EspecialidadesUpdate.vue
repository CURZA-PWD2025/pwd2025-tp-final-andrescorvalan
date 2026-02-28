<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Icon } from "@iconify/vue"
import useEspecialidadesStore from '../../stores/especialidades_store'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const { buscar_especialidad, update, defaultEspecialidad } = useEspecialidadesStore()
const especialidadEdit = ref({ ...defaultEspecialidad })
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

async function recargar_datos () {
  const id = Number(route.params.id)
  if (isNaN(id) || id <= 0) {
    mensaje.value = 'ID no válido.'
    estado.value = 'error'
    return
  }
  estado.value = 'procesando'
  mensaje.value = 'Cargando datos...'
  try {
    const resultado = await buscar_especialidad(id)    
    if (resultado && resultado.id !== 0) {
      especialidadEdit.value = { ...resultado }
      mensaje.value = ''
      estado.value = ''
    } else {
      mensaje.value = 'No se encontró el registro.'
      estado.value = 'error'
    }
  } catch (error) {
    mensaje.value = 'Error de conexión al cargar la especialidad.'
    estado.value = 'error'
  }
}

onMounted(async () => {
  recargar_datos()   
})

async function modificar_especialidad() {
  if (!especialidadEdit.value.nombre ||
      !especialidadEdit.value.descripcion) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error' 
    return
  }
  mensaje.value = 'Intentando actualizar la especialidad.'
  estado.value = 'procesando'
  try { 
    await update(especialidadEdit.value)
    mensaje.value = '¡Especialidad actualizada correctamente!' 
    estado.value = 'exito'
  } catch (error: any) {
    let errorMensaje = ''
    if (axios.isAxiosError(error)) {
      if (error.response) {
         if (error.response.data && error.response.data.mensaje)
          errorMensaje = `${error.response.data.mensaje}`
         else 
          errorMensaje = `Error del servidor (Código: ${error.response.status}).`
      } else
        errorMensaje = 'No se pudo conectar al servidor. Verifique su conexión.'
    } else
      errorMensaje = error.message || 'Error desconocido.'
  
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
      <h2>Modificar Especialidad</h2>
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
    <form @submit.prevent="modificar_especialidad" class="grud-frame">
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
            v-model="especialidadEdit.nombre"
            placeholder="Ej: Cirugía, Dermatología..."
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
            v-model="especialidadEdit.descripcion"
            placeholder="Ej: Clínica de Pequeños Animales"
            maxlength="100"
            rows="3"
            style="width: 42ch; resize: none;"
            required></textarea>
        </div>
      </div>
      <div class="grud-botones">
        <button class="boton boton-accept" type="submit" :disabled="estado === 'procesando'">
          <Icon class="icono" icon="mdi:content-save"/>
          Guardar Cambios
        </button>
        <button class="boton boton-reset" type="button" @click="recargar_datos" :disabled="estado === 'procesando'">
          <Icon class="icono" icon="mdi:restore"/>
          Reset
        </button>
      </div>
    </form>
  </section> 
</template>

<style scoped>
</style>