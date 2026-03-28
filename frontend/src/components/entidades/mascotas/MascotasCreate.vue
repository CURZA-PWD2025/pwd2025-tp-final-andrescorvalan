<script setup lang="ts">
import { ref, toRefs, onMounted } from 'vue'

import { useRouter } from 'vue-router'
const router = useRouter()

import SaveViewGenerico from  '@/components/crud-generico/SaveViewGenerico.vue'
import { useSaveLogicGenerico } from '@/components/crud-generico/SaveLogicGenerico'
const { mensaje, estado, mostrarModal, saveEntidad, resetSaveLogicGenerico } = useSaveLogicGenerico()

import useMascotasStore from '@/stores/mascotas_store'
const { create, defaultMascota } = useMascotasStore()
const newMascota = ref({ ...defaultMascota })

import usePropietariosStore from '@/stores/propietarios_store'
const { propietarios } = toRefs(usePropietariosStore())
const { getAll: getall_propietarios } = usePropietariosStore()
const idPropietario = ref<number>(0)

import useEspeciesStore from '@/stores/especies_store'
const { especies } = toRefs(useEspeciesStore())
const { getAll: getall_especies } = useEspeciesStore()
const idEspecie = ref<number>(0)

onMounted(async () => {
  try {
      await getall_especies()
      await getall_propietarios()
    } catch (error) {
      mensaje.value = "Error al cargar las especies y/o propietarios disponibles."
    }
})

async function nueva_mascota() {
  if (!newMascota.value.nombre || !newMascota.value.fecha_nac || 
      !idPropietario || !idEspecie) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error'
    return
  }
  newMascota.value.especie.id = idEspecie.value
  newMascota.value.propietario.id = idPropietario.value
  await saveEntidad(
    () => create(newMascota.value),
  )
  if (estado.value==='exito'){
    newMascota.value = { ...defaultMascota }
    idEspecie.value = 0
    idPropietario.value = 0
  }
}
</script>

<template>
  <SaveViewGenerico
    titulo="Nueva mascota"
    :estado="estado" 
    :mensaje="mensaje" 
    :mostrarModal="mostrarModal"
    @volver="router.push({name: 'mascotas_list'})"
    @submit="nueva_mascota"
    @reset="newMascota = { ...defaultMascota }; idPropietario=0; idEspecie=0"
    @cerrarModal="resetSaveLogicGenerico"
  >
    <div class="crud-field-group">
      <div class="crud-field">
        <label class="crud-field-name" for="nombre">
          Nombre:
          <abbr class="crud-abbr" 
            title="Nombre de la mascota (obligatorio)">*
          </abbr>
        </label>
        <input class="crud-input crud-data"
          id="nombre"
          type="text"
          v-model="newMascota.nombre"
          placeholder="Ej: Firulais"
          maxlength="35"
          style="width: 42ch;"
          autofocus
          required/>
      </div>
      <div class="crud-field"> 
        <label class="crud-field-name" for="fecha_nac">
          Fecha de Nacimiento:
          <abbr class="crud-abbr" 
            title="Fecha de nacimiento de la mascota (obligatorio)">*
          </abbr>
        </label>
        <input class="crud-input crud-data"
          id="fecha_nac"
          type="date"
          v-model="newMascota.fecha_nac"
          style="width: 30ch;"
          required/>
      </div>
      <div class="crud-field"> 
        <label class="crud-field-name" for="sexo">
          Sexo:
          <abbr class="crud-abbr" 
            title="Sexo de la mascota (obligatorio)">*
          </abbr>
        </label>
        <select class="crud-input crud-data" 
          id="sexo"
          v-model="newMascota.sexo"
          style="width: 10ch;"
          required>
          <option value="" disabled>
            Seleccione el sexo
          </option>
          <option value="Macho">Macho</option>
          <option value="Hembra">Hembra</option>
        </select>
      </div>
    </div>
    <div class="crud-field-group">
      <div class="crud-field"> 
        <label class="crud-field-name" for="propietario">
          Propietario:
          <abbr class="crud-abbr" 
            title="Propietario de la mascota (obligatorio)">*
          </abbr>
        </label>
        <select class="crud-input crud-data" 
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
      <div class="crud-field">
        <label for="especie" class="crud-field-name">
          Especie:
          <abbr class="crud-abbr" 
            title="Especie de la mascota (obligatorio)">*
          </abbr>
        </label>
        <select class="crud-input crud-data" 
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
  </SaveViewGenerico>
</template>

<style scoped>
</style>