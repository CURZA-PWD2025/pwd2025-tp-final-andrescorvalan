<script setup lang="ts">
import { onMounted, ref, toRefs } from 'vue'

import { useRoute, useRouter } from 'vue-router'
const router = useRouter()
const route = useRoute()

import SaveViewGenerico from '@/components//crud-generico/SaveViewGenerico.vue'
import { useSaveLogicGenerico } from '@/components//crud-generico/SaveLogicGenerico'
const { mensaje, estado, mostrarModal, saveEntidad, findEntidad, resetSaveLogicGenerico } = useSaveLogicGenerico()

import useMascotasStore from '@/stores/mascotas_store'
const { buscar_mascota, update, defaultMascota } = useMascotasStore()
const editMascota = ref({ ...defaultMascota })

import usePropietariosStore from '@/stores/propietarios_store'
import type { Propietario } from '@/interface/propietario'
const { propietarios } = toRefs(usePropietariosStore())
const { getAll: getall_propietarios } = usePropietariosStore()
const idPropietario = ref<number>(0)

import useEspeciesStore from '@/stores/especies_store'
import type { Especie } from '@/interface/especie'
const { especies } = toRefs(useEspeciesStore())
const { getAll: getall_especies } = useEspeciesStore()
const idEspecie = ref<number>(0)

async function cargar_datos () {
  const id = Number(route.params.id)
  const datos = await findEntidad(id, buscar_mascota)
  if (datos) {
      editMascota.value = { ...datos }
      idPropietario.value = (datos.propietario as Propietario)?.id || 0
      idEspecie.value = (datos.especie as Especie)?.id || 0
  }
}

onMounted(async () => {
  try {
      cargar_datos()
      await getall_especies()
      await getall_propietarios()
    } catch (error) {
      mensaje.value = "Error al cargar las especies y/o propietarios disponibles."
    }
})

async function modificar_mascota() {
  if (!editMascota.value.nombre ||
      !editMascota.value.fecha_nac  || 
      !idPropietario || !idEspecie) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error' 
    return
  }
  editMascota.value.especie.id = idEspecie.value
  editMascota.value.propietario.id = idPropietario.value
  await saveEntidad(() => update(editMascota.value))
}
</script>

<template>
  <SaveViewGenerico
    titulo="Editar mascota"
    :estado="estado" 
    :mensaje="mensaje" 
    :mostrarModal="mostrarModal"
    @volver="router.push({name: 'mascotas_list'})"
    @submit="modificar_mascota"
    @reset="cargar_datos"
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
          v-model="editMascota.nombre"
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
          v-model="editMascota.fecha_nac"
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
          v-model="editMascota.sexo"
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