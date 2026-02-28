<script setup lang="ts">
import { toRefs, onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Icon } from "@iconify/vue"
import useVeterinariosStore from '../../stores/veterinarios_store'
import useEspecialidadesStore from '../../stores/especialidades_store'

import axios from 'axios'

const router = useRouter()
const { create, defaultVeterinario } = useVeterinariosStore()
const { especialidades } = toRefs(useEspecialidadesStore())
const { getAll: getall_especialidades } = useEspecialidadesStore()
const nuevoVeterinario = ref({ ...defaultVeterinario })
const idsEspecialidades = ref<number[]>([])

const mensaje = ref('')
const estado = ref('')

const tipoMensaje = computed(() => ({
  'mensaje-procesando': estado.value === 'procesando',
  'mensaje-exito': estado.value === 'exito',
  'mensaje-error': estado.value === 'error'
}));

function go_veterinarios_list() {
  router.push({ name: 'veterinarios_list' })
}

function limpiar_formulario() {
  nuevoVeterinario.value = { ...defaultVeterinario }
}

onMounted(async () => {
  limpiar_formulario()
  try {
      await getall_especialidades()
    } catch (error) {
      mensaje.value = "Error al cargar las especialidades disponibles."
    }
})

async function nuevo_veterinario() {
  if (!nuevoVeterinario.value.nombre || !nuevoVeterinario.value.apellido || 
      !nuevoVeterinario.value.matricula) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error'
    return
  }
  mensaje.value = 'Intentando crear el veterinario...'
  estado.value = 'procesando'
  try {
    nuevoVeterinario.value.especialidades = idsEspecialidades.value
    await create(nuevoVeterinario.value)
    mensaje.value = '¡Veterinario creado correctamente! Puede cargar otro.'
    estado.value = 'exito'
    limpiar_formulario()
    idsEspecialidades.value = []
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
      <h2>Crear Veterinario</h2>
      <button @click="go_veterinarios_list" class="boton boton-back">
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
    <form @submit.prevent="nuevo_veterinario" class="grud-frame">
      <div class="grud-field-group">
        <div class="grud-field">
          <label class="grud-field-name" for="nombre">
            Nombre:
            <abbr class="grud-abbr" 
              title="Nombre del veterinario (obligatorio)">*
            </abbr>
          </label>
          <input class="grud-input grud-data"
            id="nombre"
            type="text"
            v-model="nuevoVeterinario.nombre"
            placeholder="Ej: Pedro"
            maxlength="35"
            style="width: 42ch;"
            autofocus
            required/>
        </div>
        <div class="grud-field">
          <label class="grud-field-name" for="apellido">
            Apellido:
            <abbr class="grud-abbr" 
              title="Apellido del veterinario (obligatorio)">*
            </abbr>
          </label>
          <input class="grud-input grud-data"
            id="apellido"
            type="text"
            v-model="nuevoVeterinario.apellido"
            placeholder="Ej: Garcia"
            maxlength="35"
            style="width: 42ch;"
            required/>
        </div>
        <div class="grud-field">
          <label class="grud-lafield-namebel" for="matricula">
            Matrícula:
            <abbr class="grud-abbr" 
              title="Matrícula del veterinario (obligatorio)">*
            </abbr>
          </label>
          <input class="grud-input grud-data"
            id="matricula"
            type="text"
            v-model="nuevoVeterinario.matricula"
            pattern="^(MN|MP|mn|mp)\s?\d{4,6}$"
            placeholder="Ej: MN 12345"
            title="Debe empezar con MN o MP, seguido de 4 a 6 números"
            maxlength="9"
            required/>
        </div>
        <div class="grud-field">
          <label class="grud-field-name" for="telefono">
            Teléfono:
            <abbr class="grud-abbr" 
              title="Teléfono del veterinario (obligatorio)">*
            </abbr>
          </label>
          <input class="grud-input grud-data"
            id="telefono"
            type="tel"
            v-model="nuevoVeterinario.telefono"
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
              title="Email del veterinario (obligatorio)">*
            </abbr>
          </label>
          <input class="grud-input grud-data"
            id="email"
            type="email"
            v-model="nuevoVeterinario.email"
            placeholder="Ej: juan@ejemplo.com"
            maxlength="100"
            style="width: 42ch;"
            required/>
        </div>
      </div>
      <div class="grud-field-group">
        <fieldset class="grud-fieldset">
          <legend>Especialidades</legend>
          <div v-for="esp in especialidades" :key="esp.id" class="grud-item-checkbox">
            <input
              type="checkbox"
              :id="'esp' + esp.id"
              :value="esp.id"
              v-model="idsEspecialidades"
            >
            <label :for="'esp' + esp.id">{{ esp.nombre }}</label>
          </div>
        </fieldset>
      </div>
      <div class="grud-botones">
        <button class="boton boton-accept" type="submit" :disabled="estado === 'procesando'">
          <Icon class="icono" icon="mdi:content-save-plus"/>
          {{ estado === 'procesando' ? 'Guardando...' : 'Crear Veterinario' }}
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