<script setup lang="ts">
import { onMounted, toRefs, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Icon } from "@iconify/vue"
import useMascotasStore from '../../stores/mascotas_store'
import usePropietariosStore from '../../stores/propietarios_store'
import useEspeciesStore from '../../stores/especies_store'
import axios from 'axios'

import type { Especie } from '../../interface/Especie'
import type { Propietario } from '../../interface/Propietario'
const router = useRouter()
const route = useRoute()
const { buscar_mascota, update, defaultMascota } = useMascotasStore()
const { especies } = toRefs(useEspeciesStore())
const { propietarios } = toRefs(usePropietariosStore())
const { getAll: getall_especies } = useEspeciesStore()
const { getAll: getall_propietarios } = usePropietariosStore()
const mascotaEdit = ref({ ...defaultMascota })
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
    await getall_especies()
    await getall_propietarios()
    const resultado = await buscar_mascota(id)
    if (resultado && resultado.id !== 0) {
      mascotaEdit.value = { ...resultado }
      idPropietario.value = (resultado.propietario as Propietario)?.id || 0
      idEspecie.value = (resultado.especie as Especie)?.id || 0
      mensaje.value = ''
      estado.value = ''
    } else {
      mensaje.value = 'No se encontró el registro.'
      estado.value = 'error'
    }
  } catch (error) {
    mensaje.value = 'Error de conexión al cargar la mascota.'
    estado.value = 'error'
  }
}

onMounted(async () => {
  recargar_datos()   
})

async function modificar_mascota() {
  if (!mascotaEdit.value.nombre ||
      !mascotaEdit.value.fecha_nac  || 
      !idPropietario || !idEspecie) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error' 
    return
  }
  mensaje.value = 'Intentando actualizar la mascota.'
  estado.value = 'procesando'
  try {
    const datosFinales = {
      ...mascotaEdit.value,
    }
    datosFinales.especie.id = idEspecie.value
    datosFinales.propietario.id = idPropietario.value
    await update(datosFinales)
    mensaje.value = '¡Mascota actualizada correctamente!' 
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
      <h2>Modificar Mascota</h2>
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
    <form @submit.prevent="modificar_mascota" class="grud-frame"> 
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
            v-model="mascotaEdit.nombre"
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
            v-model="mascotaEdit.fecha_nac"
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
            <option v-for="esp in especies" :key="esp.id" :value="esp.id">
              {{ esp.nombre }} ({{  esp.nombre_cientifico }})
            </option>
          </select>
        </div>
      </div>
      <div class="grud-botones">
        <button class="boton boton-accept" type="submit" :disabled="estado === 'procesando'">
          <Icon class="icono" icon="mdi:content-save"/>
          Guardar Mascota
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
  .form-input {
    width: 55ch; 
  }
</style>