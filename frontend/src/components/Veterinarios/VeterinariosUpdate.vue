<script setup lang="ts">
import { onMounted, toRefs, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Icon } from "@iconify/vue"
import useVeterinariosStore from '../../stores/veterinarios_store'
import useEspecialidadesStore from '../../stores/especialidades_store'
import axios from 'axios' 

const router = useRouter()
const route = useRoute()
const { buscar_veterinario, update, defaultVeterinario } = useVeterinariosStore()
const { especialidades } = toRefs(useEspecialidadesStore())
const { getAll: getall_especialidades } = useEspecialidadesStore()

const veterinarioEdit = ref({ ...defaultVeterinario })
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
    await getall_especialidades()

    const resultado = await buscar_veterinario(id)    
    if (resultado && resultado.id !== 0) {
      veterinarioEdit.value = { ...resultado }
      if (resultado.especialidades) {
        idsEspecialidades.value = (resultado.especialidades as any[]).map(e => e.id)
      }
      mensaje.value = ''
      estado.value = ''
    } else {
      mensaje.value = 'No se encontró el registro.'
      estado.value = 'error'
    }
  } catch (error) {
    mensaje.value = 'Error de conexión al cargar el veterinario.'
    estado.value = 'error'
  }
}

onMounted(async () => {
  recargar_datos()   
})

async function modificar_veterinario() {
  if (!veterinarioEdit.value.nombre ||
      !veterinarioEdit.value.apellido ||
      !veterinarioEdit.value.matricula) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error' 
    return
  }
  mensaje.value = 'Intentando actualizar el veterinario.'
  estado.value = 'procesando'
  try { 
    const datosFinales = {
      ...veterinarioEdit.value,
      especialidades: idsEspecialidades.value
    }
    await update(datosFinales)
    await recargar_datos()
    mensaje.value = '¡Veterinario actualizado correctamente!' 
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
      <h2>Modificar Veterinario</h2>
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
    <form @submit.prevent="modificar_veterinario" class="grud-frame"> 
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
            v-model="veterinarioEdit.nombre"
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
            v-model="veterinarioEdit.apellido"
            placeholder="Ej: Garcia"
            maxlength="35"
            style="width: 42ch;"
            required/>
        </div>
        <div class="grud-field">
          <label class="grud-field-name" for="matricula">
            Matrícula:
            <abbr class="grud-abbr" 
              title="Matrícula del veterinario (obligatorio)">*
            </abbr>
          </label>
          <input class="grud-input grud-data"
            id="matricula"
            type="text"
            v-model="veterinarioEdit.matricula"
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
            v-model="veterinarioEdit.telefono"
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
            v-model="veterinarioEdit.email"
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
          <Icon class="icono" icon="mdi:content-save"/>
          Guardar Veterinario
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