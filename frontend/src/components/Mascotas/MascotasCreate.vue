<script setup lang="ts">
import { toRefs, onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Icon } from "@iconify/vue"
import useMascotasStore from '../../stores/mascotas_store'
import usePropietariosStore from '../../stores/propietarios_store'
import useEspeciesStore from '../../stores/especies_store'
import axios from 'axios'

const router = useRouter()
const { create, defaultMascota } = useMascotasStore()
const { especies } = toRefs(useEspeciesStore())
const { propietarios } = toRefs(usePropietariosStore())
const { getAll: getall_especies } = useEspeciesStore()
const { getAll: getall_propietarios } = usePropietariosStore()
const nuevaMascota = ref({ ...defaultMascota })
const idEspecie = ref<number>(0)
const idPropietario = ref<number>(0)

const mensaje = ref('')
const estado = ref('')

const tipoMensaje = computed(() => ({
  'mensaje-procesando': estado.value === 'procesando',
  'mensaje-exito': estado.value === 'exito',
  'mensaje-error': estado.value === 'error'
}));

function go_mascotas_list() {
  router.push({ name: 'mascotas_list' })
}

function limpiar_formulario() {
  nuevaMascota.value = { ...defaultMascota }
}

onMounted(async () => {
  limpiar_formulario()
  try {
      await getall_especies()
      await getall_propietarios()
    } catch (error) {
      mensaje.value = "Error al cargar las especies y/o propietarios disponibles."
    }
})

async function nueva_mascota() {
  if (!nuevaMascota.value.nombre || !nuevaMascota.value.fecha_nac || 
      !idPropietario || !idEspecie) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error'
    return
  }
  mensaje.value = 'Intentando crear la mascota...'
  estado.value = 'procesando'
  try {
    nuevaMascota.value.especie.id = idEspecie.value
    nuevaMascota.value.propietario.id = idPropietario.value
    await create(nuevaMascota.value)
    mensaje.value = '¡Mascota creada correctamente! Puede cargar otra.'
    estado.value = 'exito'
    limpiar_formulario()
    idEspecie.value = 0
    idPropietario.value = 0
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
      <h2>Crear Mascota</h2>
      <button @click="go_mascotas_list" class="boton boton-back">
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
    <form @submit.prevent="nueva_mascota" class="grud-frame">
      <div class="grud-field-group">
        <div class="grud-field">
          <label class="grud-field-name" for="nombre">
            Nombre:
            <abbr class="grud-abbr" 
              title="Nombre de la mascota (obligatorio)">*
            </abbr>
          </label>
          <input class="grud-input grud-data"
            id="nombre"
            type="text"
            v-model="nuevaMascota.nombre"
            placeholder="Ej: Firulais"
            maxlength="35"
            style="width: 42ch;"
            autofocus
            required/>
        </div>
        <div class="grud-field"> 
          <label class="grud-field-name" for="fecha_nac">
            Fecha de Nacimiento:
            <abbr class="grud-abbr" 
              title="Fecha de nacimiento de la mascota (obligatorio)">*
            </abbr>
          </label>
          <input class="grud-input grud-data"
            id="fecha_nac"
            type="date"
            v-model="nuevaMascota.fecha_nac"
            style="width: 42ch;"
            required/>
        </div>
      </div>
      <div class="grud-field-group">
        <div class="grud-field"> 
          <label class="grud-field-name" for="propietario">
            Propietario
            <abbr class="grud-abbr" 
              title="Propietario de la mascota (obligatorio)">*:
            </abbr>
          </label>
          <select class="grud-input grud-data" 
            id="propietario"
            v-model="idPropietario" 
            required>
            <option value="" disabled>
              Seleccione un propietario
            </option>
            <option v-for="prop in propietarios" :key="prop.id" :value="prop.id">
              {{ prop.apellido }}, {{ prop.nombre }}
            </option>
          </select>
        </div>
        <div class="grud-field">
          <label for="especie" class="grud-field-name">
            Especie <abbr title="Especie de la mascota (obligatorio)">*</abbr>
          </label>
          <select class="grud-input grud-data" 
            id="especie" 
            v-model="idEspecie" 
            required>
            <option value="" disabled>
              Seleccione una especie
            </option>
            <option v-for="esp in especies" :key="esp.id" :value="esp.id">
              {{ esp.nombre }} ({{  esp.nombre_cientifico }})
            </option>
          </select>
        </div>
      </div>
      <div class="grud-botones">
        <button class="boton boton-accept" type="submit" :disabled="estado === 'procesando'">
          <Icon class="icono" icon="mdi:content-save-plus"/>
          {{ estado === 'procesando' ? 'Guardando...' : 'Crear Mascota' }}
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
  .form-input {
    width: 55ch;
  }
</style>