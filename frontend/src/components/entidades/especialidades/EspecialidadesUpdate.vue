<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { useRoute, useRouter } from 'vue-router'
const router = useRouter()
const route = useRoute()

import SaveViewGenerico from '@/components/crud-generico/SaveViewGenerico.vue'
import { useSaveLogicGenerico } from '@/components/crud-generico/SaveLogicGenerico'
const { mensaje, estado, mostrarModal, saveEntidad, findEntidad, resetSaveLogicGenerico } = useSaveLogicGenerico()

import useEspecialidadesStore from '@/stores/especialidades_store'
const { buscar_especialidad, update, defaultEspecialidad } = useEspecialidadesStore()
const editEspecialidad = ref({ ...defaultEspecialidad })

async function cargar_datos() {
  const id = Number(route.params.id)
  const entidad = await findEntidad(id, buscar_especialidad)
  if (entidad) {
      editEspecialidad.value = { ...entidad }
  }
}

onMounted(async () => {
  cargar_datos()
})

async function modificar_especialidad() {
  if (!editEspecialidad.value.nombre || !editEspecialidad.value.descripcion) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error' 
    return
  }
  await saveEntidad(() => update(editEspecialidad.value))
}
</script>

<template>
  <SaveViewGenerico
    titulo="Editar especialidad"
    :estado="estado" 
    :mensaje="mensaje" 
    :mostrarModal="mostrarModal"
    @volver="router.push({name: 'especialidades_list'})"
    @submit="modificar_especialidad"
    @reset="cargar_datos"
    @cerrarModal="resetSaveLogicGenerico"
  >
    <div class="crud-field-group">
      <div class="crud-field">
        <label class="crud-field-name" for="nombre">
          Nombre: 
          <abbr class="crud-abbr" 
            title="Nombre de la especialidad (obligatorio)">*
          </abbr>
        </label>
        <input class="crud-input crud-data"
          id="nombre"
          type="text"
          v-model="editEspecialidad.nombre"
          placeholder="Ej: Cirugía, Dermatología"
          maxlength="50"
          style="width: 55ch;"
          autofocus
          required/>
      </div>
       <div class="crud-field">
        <label class="crud-field-name" for="activa">
          Activa:
        </label>       
        <select class="crud-input crud-data" 
          id="activa"
          v-model="editEspecialidad.activa"
          style="width: 10ch;"required>
          <option value=1>Si</option>
          <option value=0>No</option>
        </select>
      </div>
      <div class="crud-field">
        <label class="crud-field-name" for="descripcion">
          Descripción: 
          <abbr class="crud-abbr" 
            title="Descripción de la especialidad (obligatorio)">*
          </abbr>
        </label>
          <textarea class="crud-input crud-data"
          id="descripcion"
          v-model="editEspecialidad.descripcion"
          placeholder="Ej: Clínica de Pequeños Animales"
          maxlength="100"
          rows="3"
          style="width: 55ch; resize: none;"
          required></textarea>
      </div>
    </div>
  </SaveViewGenerico>
</template>

<style scoped>
</style>