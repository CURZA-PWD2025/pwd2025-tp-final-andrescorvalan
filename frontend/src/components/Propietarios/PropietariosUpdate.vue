<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Icon } from "@iconify/vue"
import usePropietariosStore from '../../stores/propietarios_store'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const { buscar_propietario, update, defaultPropietario } = usePropietariosStore()
const propietarioEdit = ref({ ...defaultPropietario })
const mensaje = ref('')
const estado = ref('')

const tipoMensaje = computed(() => ({
  'mensaje-procesando': estado.value === 'procesando',
  'mensaje-exito': estado.value === 'exito',
  'mensaje-error': estado.value === 'error'
}));

function go_propietarios_list() {
  router.push({ name: 'propietarios_list' })
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
    const resultado = await buscar_propietario(id)    
    if (resultado && resultado.id !== 0) {
      propietarioEdit.value = { ...resultado }
      mensaje.value = ''
      estado.value = ''
    } else {
      mensaje.value = 'No se encontró el registro.'
      estado.value = 'error'
    }
  } catch (error) {
    mensaje.value = 'Error de conexión al cargar el propietario.'
    estado.value = 'error'
  }
}

onMounted(async () => {
  recargar_datos()   
})

async function modificar_propietario() {
  if (!propietarioEdit.value.nombre ||
      !propietarioEdit.value.apellido ||
      !propietarioEdit.value.dni) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error' 
    return
  }
  mensaje.value = 'Intentando actualizar el propietario.'
  estado.value = 'procesando'
  try { 
    await update(propietarioEdit.value)
    mensaje.value = '¡Propietario actualizado correctamente!' 
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
      <h2>Modificar Propietario</h2>
      <button @click="go_propietarios_list" class="boton boton-back">
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
    <form @submit.prevent="modificar_propietario" class="grud-frame">
      <div class="grud-field-group">
        <div class="grud-field">
          <label class="grud-field-name" for="nombre">
            Nombre: 
            <abbr class="grud-abbr" 
              title="Nombre del propietario (obligatorio)">*
            </abbr>
          </label>
          <input class="grud-input grud-data"
            id="nombre"
            type="text"
            v-model="propietarioEdit.nombre"
            placeholder="Ej: Juan"
            maxlength="35"
            style="width: 42ch;"
            autofocus
            required/>
        </div>
        <div class="grud-field">
          <label class="grud-field-name" for="apellido">
            Apellido: 
            <abbr class="grud-abbr" 
              title="Apellido del propietario (obligatorio)">*
            </abbr>
          </label>
          <input class="grud-input grud-data"
            id="apellido"
            type="text"
            v-model="propietarioEdit.apellido"
            placeholder="Ej: Garcia"
            maxlength="35"
            style="width: 42ch;"
            required/>
        </div>
        <div class="grud-field">
          <label class="grud-field-name" for="dni">
            DNI: 
            <abbr class="grud-abbr" 
              title="DNI del propietario (obligatorio)">*
            </abbr>
          </label>
          <input class="grud-input grud-data"
            id="dni"
            type="numeric"
            pattern="[0-9]*"
            v-model="propietarioEdit.dni"
            placeholder="Ej: 12345678"
            maxlength="8"
            minlength="7"
            style="width: 12ch;"
            required/>
        </div>
      </div>      
      <div class="grud-field-group">
        <div class="grud-field">
          <label class="grud-field-name" for="telefono">
            Teléfono: 
            <abbr class="grud-abbr" 
              title="Teléfono del propietario (obligatorio)">*
            </abbr>
          </label>
          <input class="grud-input grud-data"
            id="telefono"
            type="tel"
            v-model="propietarioEdit.telefono"
            placeholder="Cod. Área + Número (ej: 2991234567)"
            minlength="10"
            maxlength="15"
            style="width: 42ch;"
            pattern="[0-9+ ]{10,15}"
            title="Ingrese 10 dígitos (ej: 2991234567). Puede incluir +54"
            required/>
        </div>
        <div class="grud-field">
          <label class="grud-field-name" for="email">
            Email: 
            <abbr class="grud-abbr" 
              title="Email del propietario (obligatorio)">*
            </abbr>
          </label>
          <input class="grud-input grud-data"
            id="email"
            type="email"
            v-model="propietarioEdit.email"
            placeholder="Ej: juan@ejemplo.com"
            maxlength="100"
            style="width: 42ch;"
            required/>
        </div>
      </div>
      <div class="grud-botones">
        <button class="boton boton-accept" type="submit" :disabled="estado === 'procesando'">
          <Icon class="icono" icon="mdi:content-save"/>
          Guardar Propietario
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
  input {
    width: 55ch; 
  }
</style>