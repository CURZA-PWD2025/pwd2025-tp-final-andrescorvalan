<script setup lang="ts">
import { ref } from 'vue'

import { useRouter } from 'vue-router'
const router = useRouter()

import SaveViewGenerico from '@/components/crud-generico/SaveViewGenerico.vue'
import { useSaveLogicGenerico } from '@/components/crud-generico/SaveLogicGenerico'
const { mensaje, estado, mostrarModal, saveEntidad, resetSaveLogicGenerico } = useSaveLogicGenerico()

import useEspecialidadesStore from '@/stores/especialidades_store'
const { create, defaultEspecialidad } = useEspecialidadesStore()
const newEspecialidad = ref({ ...defaultEspecialidad })

async function nueva_especialidad() {
  if (!newEspecialidad.value.nombre || !newEspecialidad.value.descripcion) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error'
    return
  }
  await saveEntidad(
    () => create(newEspecialidad.value),
  )
  if (estado.value==='exito')
    newEspecialidad.value = { ...defaultEspecialidad }
}
</script>

<template>
  <SaveViewGenerico
    titulo="Nueva especialidad"
    :estado="estado" 
    :mensaje="mensaje" 
    :mostrarModal="mostrarModal"
    @volver="router.push({name: 'especialidades_list'})"
    @submit="nueva_especialidad"
    @reset="newEspecialidad = { ...defaultEspecialidad }"
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
          v-model="newEspecialidad.nombre"
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
          v-model="newEspecialidad.activa"
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
          v-model="newEspecialidad.descripcion"
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