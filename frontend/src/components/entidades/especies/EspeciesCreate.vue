<script setup lang="ts">
import { ref } from 'vue'

import { useRouter } from 'vue-router'
const router = useRouter()

import SaveViewGenerico from '@/components/crud-generico/SaveViewGenerico.vue'
import { useSaveLogicGenerico } from '@/components/crud-generico/SaveLogicGenerico'
const { mensaje, estado, mostrarModal, saveEntidad, resetSaveLogicGenerico } = useSaveLogicGenerico()

import useEspeciesStore from '@/stores/especies_store'
const { create, defaultEspecie } = useEspeciesStore()
const newEspecie = ref({ ...defaultEspecie })

async function nueva_especie() {
  if (!newEspecie.value.nombre || !newEspecie.value.nombre_cientifico || 
      !newEspecie.value.clase) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error'
    return
  }
  await saveEntidad(
         () => create(newEspecie.value),
  )
  if (estado.value==='exito')
    newEspecie.value = { ...defaultEspecie }
}
</script>

<template>
  <SaveViewGenerico
    titulo="Nueva especie"
    :estado="estado" 
    :mensaje="mensaje" 
    :mostrarModal="mostrarModal"
    @volver="router.push({name: 'especies_list'})"
    @submit="nueva_especie"
    @reset="newEspecie = { ...defaultEspecie }"
    @cerrarModal="resetSaveLogicGenerico"
  >
    <div class="crud-field-group">
      <div class="crud-field">
        <label class="crud-field-name" for="nombre">
          Nombre Común: 
          <abbr class="crud-abbr" 
            title="Nombre de la especie (obligatorio)">*
          </abbr>
        </label>
        <input class="crud-input crud-data"
          id="nombre"
          type="text"
          v-model="newEspecie.nombre"
          placeholder="Ej: Perro"
          maxlength="35"
          style="width: 42ch;"
          autofocus
          required/>
      </div>
      <div class="crud-field">
        <label class="crud-field-name" for="nombcientif">
          Nombre Científico: 
          <abbr class="crud-abbr" 
            title="Nombre científico de la especie (obligatorio)">*
          </abbr>
        </label>
        <input class="crud-input crud-data"
          id="nombcientif"
          type="text"
          v-model="newEspecie.nombre_cientifico"
          placeholder="Ej: Canis lupus familiaris"
          maxlength="50"
          style="width: 42ch;"
          required/>
      </div>
      <div class="crud-field">
        <label class="crud-field-name" for="clase">
          Clase: 
          <abbr class="crud-abbr" 
            title="Clase de la especie (obligatorio)">*
          </abbr>
        </label>
        <input class="crud-input crud-data"
          id="clase"
          type="text"
          v-model="newEspecie.clase"
          placeholder="Ej: Mamífero"
          maxlength="35"
          style="width: 42ch;"
          required/>
      </div>
      <div class="crud-field">
        <label class="crud-field-name" for="esp_vida">
          Esperanza de vida: 
        </label>
        <input class="crud-input crud-data"
          id="esp_vida"
          type="numeric"
          pattern="[0-9]*"
          v-model="newEspecie.esperanza_vida"
          placeholder="Ej: 12"
          maxlength="3"
          minlength="1"
          style="width: 17ch;"/>
      </div>
      <div class="crud-field">
        <label class="crud-field-name" for="exotica">
          Exótica:
        </label>       
        <select class="crud-input crud-data" 
          id="exotica"
          v-model="newEspecie.exotica"
          style="width: 10ch;"required>
          <option value=1>Si</option>
          <option value=0>No</option>
        </select>
      </div>
    </div>
  </SaveViewGenerico>   
</template>

<style scoped>
</style>