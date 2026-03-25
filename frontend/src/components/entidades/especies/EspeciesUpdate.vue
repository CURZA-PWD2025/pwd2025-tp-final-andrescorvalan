<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { useRoute, useRouter } from 'vue-router'
const router = useRouter()
const route = useRoute()

import SaveFormGenerico from '@/components/crud-generico/SaveViewGenerico.vue'
import { useSaveLogicGenerico } from '@/components/crud-generico/SaveLogicGenerico'
const { mensaje, estado, mostrarModal, saveEntidad, findEntidad, resetSaveLogicGenerico } = useSaveLogicGenerico()

import useEspeciesStore from '@/stores/especies_store'
const { buscar_especie, update, defaultEspecie } = useEspeciesStore()
const editEspecie = ref({ ...defaultEspecie })

async function cargar_datos () {
  const id = Number(route.params.id)
  const datos = await findEntidad(id, buscar_especie)
  if (datos) {
      editEspecie.value = { ...datos }
  }
}

onMounted(async () => {
  cargar_datos()   
})

async function modificar_especie() {
  if (!editEspecie.value.nombre ||
      !editEspecie.value.nombre_cientifico ||
      !editEspecie.value.clase) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error' 
    return
  }
  await saveEntidad(() => update(editEspecie.value))
}
</script>

<template>
  <SaveFormGenerico
    titulo="Actualizar especia"
    :estado="estado" 
    :mensaje="mensaje" 
    :mostrarModal="mostrarModal"
    @volver="router.push({name: 'especies_list'})"
    @submit="modificar_especie"
    @reset="cargar_datos"
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
          v-model="editEspecie.nombre"
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
          v-model="editEspecie.nombre_cientifico"
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
          v-model="editEspecie.clase"
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
          v-model="editEspecie.esperanza_vida"
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
          v-model="editEspecie.exotica"
          style="width: 10ch;"required>
          <option value=1>Si</option>
          <option value=0>No</option>
        </select>
      </div>
    </div>
  </SaveFormGenerico>  
</template>

<style scoped>
</style>