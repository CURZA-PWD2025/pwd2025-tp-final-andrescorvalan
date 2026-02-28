<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Icon } from "@iconify/vue"
import useEspeciesStore from '../../stores/especies_store'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const { buscar_especie, update, defaultEspecie } = useEspeciesStore()
const especieEdit = ref({ ...defaultEspecie })
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
    const resultado = await buscar_especie(id)    
    if (resultado && resultado.id !== 0) {
      especieEdit.value = { ...resultado }
      mensaje.value = ''
      estado.value = ''
    } else {
      mensaje.value = 'No se encontró el registro.'
      estado.value = 'error'
    }
  } catch (error) {
    mensaje.value = 'Error de conexión al cargar la especie.'
    estado.value = 'error'
  }
}

onMounted(async () => {
  recargar_datos()   
})

async function modificar_especie() {
  if (!especieEdit.value.nombre ||
      !especieEdit.value.nombre_cientifico ||
      !especieEdit.value.clase) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error' 
    return
  }
  mensaje.value = 'Intentando actualizar la especie.'
  estado.value = 'procesando'
  try { 
    await update(especieEdit.value)
    mensaje.value = '¡Especie actualizada correctamente!' 
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
      <h2>Modificar Especie</h2>
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
    <form @submit.prevent="modificar_especie" class="grud-frame">
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
            v-model="especieEdit.nombre"
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
            v-model="especieEdit.nombre_cientifico"
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
            v-model="especieEdit.clase"
            placeholder="Ej: Mamífero"
            maxlength="35"
            style="width: 42ch;"
            required/>
        </div>
      </div>
      <div class="grud-botones">
        <button class="boton boton-accept" type="submit" :disabled="estado === 'procesando'">
          <Icon class="icono" icon="mdi:content-save"/>
          Guardar Especie
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