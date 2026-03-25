<script setup lang="ts">
import { onMounted, ref, toRefs } from 'vue'

import { useRoute, useRouter } from 'vue-router'
const router = useRouter()
const route = useRoute()

import SaveFormGenerico from '@/components//crud-generico/SaveViewGenerico.vue'
import { useSaveLogicGenerico } from '@/components//crud-generico/SaveLogicGenerico'
const { mensaje, estado, mostrarModal, saveEntidad, findEntidad, resetSaveLogicGenerico } = useSaveLogicGenerico()

import useVeterinariosStore from '@/stores/veterinarios_store'
const { buscar_veterinario, update, defaultVeterinario } = useVeterinariosStore()



import useEspecialidadesStore from '@/stores/especialidades_store'
import axios from 'axios' 

const { especialidades } = toRefs(useEspecialidadesStore())
const { getAll: getall_especialidades } = useEspecialidadesStore()

const editVeterinario = ref({ ...defaultVeterinario })
const idsEspecialidades = ref<number[]>([])



async function cargar_datos () {
  const id = Number(route.params.id)
   const datos = await findEntidad(id, buscar_veterinario)
  if (datos) {
      editVeterinario.value = { ...datos }
      idsEspecialidades.value = (datos.especialidades as any[]).map(e => e.id)
  }
}

onMounted(async () => {
  try {
      cargar_datos()
      await getall_especialidades()
    } catch (error) {
      mensaje.value = "Error al cargar las especies y/o propietarios disponibles."
    }
})

async function modificar_veterinario() {
  if (!editVeterinario.value.nombre ||
      !editVeterinario.value.apellido ||
      !editVeterinario.value.matricula) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error' 
    return
  }
  editVeterinario.value.especialidades = idsEspecialidades.value
  await saveEntidad(() => update(editVeterinario.value))
}
</script>

<template>
  <SaveFormGenerico
    titulo="Editar veterinario"
    :estado="estado" 
    :mensaje="mensaje" 
    :mostrarModal="mostrarModal"
    @volver="router.push({name: 'veterinarios_list'})"
    @submit="modificar_veterinario"
    @reset="cargar_datos"
    @cerrarModal="resetSaveLogicGenerico"
  >
    <div class="crud-field-group">
      <div class="crud-field">
        <label class="crud-field-name" for="nombre">
          Nombre:
          <abbr class="crud-abbr"
            title="Nombre del veterinario (obligatorio)">*
          </abbr>
        </label>
        <input class="crud-input crud-data"
          id="nombre"
          type="text"
          v-model="editVeterinario.nombre"
          placeholder="Ej: Pedro"
          maxlength="35"
          style="width: 42ch;"
          autofocus
          required/>
      </div>
      <div class="crud-field">
        <label class="crud-field-name" for="apellido">
          Apellido:
          <abbr class="crud-abbr"
            title="Apellido del veterinario (obligatorio)">*
          </abbr>
        </label>
        <input class="crud-input crud-data"
          id="apellido"
          type="text"
          v-model="editVeterinario.apellido"
          placeholder="Ej: Garcia"
          maxlength="35"
          style="width: 42ch;"
          required/>
      </div>
      <div class="crud-field">
        <label class="crud-field-name" for="matricula">
          Matrícula:
          <abbr class="crud-abbr" 
            title="Matrícula del veterinario (obligatorio)">*
          </abbr>
        </label>
        <input class="crud-input crud-data"
          id="matricula"
          type="text"
          v-model="editVeterinario.matricula"
          pattern="^(MN|MP|mn|mp)\s?\d{4,6}$"
          placeholder="Ej: MN 12345"
          title="Debe empezar con MN o MP, seguido de 4 a 6 números"
          maxlength="15"
          required/>
      </div>
      <div class="crud-field">
        <label class="crud-field-name" for="telefono">
          Teléfono:
          <abbr class="crud-abbr" 
            title="Teléfono del veterinario (obligatorio)">*
          </abbr>
        </label>
        <input class="crud-input crud-data"
          id="telefono"
          type="tel"
          v-model="editVeterinario.telefono"
          placeholder="Cod. Área + Número (ej: 2991234567)"
          minlength="10"
          maxlength="15"
          style="width: 42ch;"
          pattern="[0-9+ ]{10,15}"
          title="Ingrese 10 dígitos (ej: 2991234567). Puede incluir +54"
          required/>
      </div>
      <div class="crud-field">
        <label class="crud-field-name" for="email">
          Email:
          <abbr class="crud-abbr" 
            title="Email del veterinario (obligatorio)">*
          </abbr>
        </label>
        <input class="crud-input crud-data"
          id="email"
          type="email"
          v-model="editVeterinario.email"
          placeholder="Ej: juan@ejemplo.com"
          maxlength="100"
          style="width: 42ch;"
          required/>
      </div>
    </div>
    <div class="crud-field-group">
      <fieldset class="crud-fieldset">
        <legend>Especialidades</legend>
        <div v-for="esp in especialidades" :key="esp.id" class="crud-item-checkbox">
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
  
  </SaveFormGenerico> 
</template>

<style scoped>
</style>