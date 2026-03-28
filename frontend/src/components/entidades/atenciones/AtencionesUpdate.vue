<script setup lang="ts">
import { onMounted, ref, toRefs } from 'vue'

import { useRoute, useRouter } from 'vue-router'
const router = useRouter()
const route = useRoute()

import SaveViewGenerico from '@/components//crud-generico/SaveViewGenerico.vue'
import { useSaveLogicGenerico } from '@/components//crud-generico/SaveLogicGenerico'
const { mensaje, estado, mostrarModal, saveEntidad, findEntidad, resetSaveLogicGenerico } = useSaveLogicGenerico()

import useAtencionesStore from '@/stores/atenciones_store'
const { buscar_atencion, update, defaultAtencion } = useAtencionesStore()
const editAtencion = ref({ ...defaultAtencion })

import useVeterinariosStore from '@/stores/veterinarios_store'
import type { Veterinario } from '@/interface/veterinario'
const { veterinarios } = toRefs(useVeterinariosStore())
const { getAll: getall_veterinarios } = useVeterinariosStore()
const idVeterinario = ref<number>(0)

import useMascotasStore from '@/stores/mascotas_store'
import type { Mascota } from '@/interface/mascota'
const { mascotas } = toRefs(useMascotasStore())
const { getAll: getall_mascotas } = useMascotasStore()
const idMascota = ref<number>(0)

async function cargar_datos () {
  const id = Number(route.params.id)
  const datos = await findEntidad(id, buscar_atencion)
  if (datos) {
      editAtencion.value = { ...datos }
      idVeterinario.value = (datos.veterinario as Veterinario)?.id || 0
      idMascota.value = (datos.mascota as Mascota)?.id || 0
  }
}

onMounted(async () => {
  try {
      cargar_datos()
      await getall_mascotas()
      await getall_veterinarios()
    } catch (error) {
      mensaje.value = "Error al cargar las mascotas y/o veterinarios disponibles."
    }
})

async function modificar_atencion() {
  if (!editAtencion.value.fecha || !editAtencion.value.diagnostico || !editAtencion.value.tratamiento ||
      !idVeterinario || !idMascota) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error'
    return
  }
  editAtencion.value.mascota.id = idMascota.value
  editAtencion.value.veterinario.id = idVeterinario.value
  await saveEntidad(
    () => update(editAtencion.value),
  )
}
</script>

<template>
  <SaveViewGenerico
    titulo="Editar atención"
    :estado="estado" 
    :mensaje="mensaje" 
    :mostrarModal="mostrarModal"
    @volver="router.push({name: 'atenciones_list'})"
    @submit="modificar_atencion"
    @reset="cargar_datos"
    @cerrarModal="resetSaveLogicGenerico"
  >
    <div class="crud-field-group">
      <div class="crud-field"> 
        <label class="crud-field-name" for="fecha">
          Fecha:
          <abbr class="crud-abbr" 
            title="Fecha de la atención veterinaria (obligatorio)">*
          </abbr>
        </label>
        <input class="crud-input crud-data"
          id="fecha"
          type="date"
          v-model="editAtencion.fecha"
          style="width: 15ch;"
          autofocus
          required/>
      </div>
    </div>
     <div class="crud-field-group">
      <div class="crud-field"> 
        <label class="crud-field-name" for="veterinario">
          Veterinario:
          <abbr class="crud-abbr" 
            title="Veterinario que realiza la atención (obligatorio)">*
          </abbr>
        </label>
        <select class="crud-input crud-data" 
          id="veterinario"
          v-model="idVeterinario"
          style="width: 25ch;"
          required>
          <option value="" disabled>
            Seleccione un veterinario
          </option>
          <option v-for="elVete in veterinarios" :key="elVete.id" :value="elVete.id">
            {{ elVete.apellido }}, {{ elVete.nombre }}
          </option>
        </select>
      </div>
      <div class="crud-field">
        <label for="mascota" class="crud-field-name">
          Mascota:
          <abbr class="crud-abbr" 
            title="Mascota atendida (obligatorio)">*
          </abbr>
        </label>
        <select class="crud-input crud-data" 
          id="mascota" 
          v-model="idMascota" 
          style="width: 25ch;"
          required>
          <option value="" disabled>
            Seleccione una mascota
          </option>
          <option v-for="laMascota in mascotas" :key="laMascota.id" :value="laMascota.id">
            {{ laMascota.nombre }}, duaño/a: ({{  laMascota.propietario.apellido }})
          </option>
        </select>
      </div>
    </div>
    <div class="crud-field-group">
      <div class="crud-field">
        <label class="crud-field-name" for="diagnostico">
          Diagnostico:
          <abbr class="crud-abbr" 
            title="Diagnóstico del veterinario (obligatorio)">*
          </abbr>
        </label>
        <textarea class="crud-input crud-data"
          id="diagnostico"
          v-model="editAtencion.diagnostico"
          placeholder="Ej: Infección bucal"
          rows="5"
          style="width: 55ch; resize: none;"
          required>
        </textarea>
      </div>
      <div class="crud-field">
        <label class="crud-field-name" for="tratamiento">
          Tratamiento:
          <abbr class="crud-abbr" 
            title="Tratamiento indicado (obligatorio)">*
          </abbr>
        </label>
        <textarea class="crud-input crud-data"
          id="tratamiento"
          v-model="editAtencion.tratamiento"
          placeholder="Ej: Antibiótico Odontobiotic por 7 días"
          rows="5"
          style="width: 55ch; resize: none;"
          required>
        </textarea>
      </div>
        <div class="crud-field">
        <label class="crud-field-name" for="observaciones">
          Observaciones:
        </label>
        <textarea class="crud-input crud-data"
          id="observaciones"
          v-model="editAtencion.observaciones"
          placeholder="Ej: Buen estado general"
          rows="5"
          style="width: 55ch; resize: none;">
        </textarea>
      </div>
    </div>
  </SaveViewGenerico>
</template>

<style scoped>
</style>