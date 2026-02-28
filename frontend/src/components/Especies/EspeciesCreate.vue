<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Icon } from "@iconify/vue"
import useEspeciesStore from '../../stores/especies_store'
import axios from 'axios'

const router = useRouter()
const { create, defaultEspecie } = useEspeciesStore()
const nuevaEspecie = ref({ ...defaultEspecie })
const mensaje = ref('')
const estado = ref('')

const tipoMensaje = computed(() => ({
  'mensaje-procesando': estado.value === 'procesando',
  'mensaje-exito': estado.value === 'exito',
  'mensaje-error': estado.value === 'error'
}));

function go_especies_list() {
    router.push({ name: 'especies_list' })
}

function limpiar_formulario() {
  nuevaEspecie.value = { ...defaultEspecie }
}

onMounted(() => {
  limpiar_formulario()
})

async function nueva_especie() {
  if (!nuevaEspecie.value.nombre || !nuevaEspecie.value.nombre_cientifico || 
      !nuevaEspecie.value.clase) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error'
    return
  }
  mensaje.value = 'Intentando crear la especie...'
  estado.value = 'procesando'
  try {
    await create(nuevaEspecie.value)
    mensaje.value = '¡Especie creada correctamente! Puede cargar otra.'
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
      <h2>Crear Especie</h2>
      <button @click="go_especies_list" class="boton boton-back">
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
    <form @submit.prevent="nueva_especie" class="grud-frame">
      <div class="grud-field-group">
        <div class="grud-field">
          <label class="grud-field-name" for="nombre">
            Nombre Común: 
            <abbr class="grud-abbr" 
              title="Nombre de la especie (obligatorio)">*
            </abbr>
          </label>
          <input class="grud-input grud-data"
            id="nombre"
            type="text"
            v-model="nuevaEspecie.nombre"
            placeholder="Ej: Perro"
            maxlength="35"
            style="width: 42ch;"
            autofocus
            required/>
        </div>
        <div class="grud-field">
          <label class="grud-field-name" for="nombcientif">
            Nombre Científico: 
            <abbr class="grud-abbr" 
              title="Nombre científico de la especie (obligatorio)">*
            </abbr>
          </label>
          <input class="grud-input grud-data"
            id="nombcientif"
            type="text"
            v-model="nuevaEspecie.nombre_cientifico"
            placeholder="Ej: Canis lupus familiaris"
            maxlength="35"
            style="width: 42ch;"
            required/>
        </div>
        <div class="grud-field">
          <label class="grud-field-name" for="clase">
            Clase: 
            <abbr class="grud-abbr" 
              title="Clase de la especie (obligatorio)">*
            </abbr>
          </label>
          <input class="grud-input grud-data"
            id="clase"
            type="text"
            v-model="nuevaEspecie.clase"
            placeholder="Ej: Mamífero"
            maxlength="35"
            style="width: 42ch;"
            required/>
        </div>
      </div>
      <div class="grud-botones">
        <button class="boton boton-accept" type="submit" :disabled="estado === 'procesando'">
          <Icon class="icono" icon="mdi:content-save-plus"/>
          {{ estado === 'procesando' ? 'Guardando...' : 'Crear Especie' }} 
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