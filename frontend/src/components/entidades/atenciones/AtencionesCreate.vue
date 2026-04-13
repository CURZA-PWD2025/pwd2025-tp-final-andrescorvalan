<script setup lang="ts">
import { ref, toRefs, onMounted, computed } from 'vue'

import { useRouter } from 'vue-router'
const router = useRouter()

import SaveViewGenerico from '@/components/crud-generico/SaveViewGenerico.vue'
import { useSaveLogicGenerico } from '@/components//crud-generico/SaveLogicGenerico'
const { mensaje, estado, mostrarModal, saveEntidad, resetSaveLogicGenerico } = useSaveLogicGenerico()

import useAtencionesStore from '@/stores/atenciones_store'
const { create, defaultAtencion } = useAtencionesStore()
const newAtencion = ref({ ...defaultAtencion })

import useVeterinariosStore from '@/stores/veterinarios_store'
const { veterinarios } = toRefs(useVeterinariosStore())
const { getAll: getall_veterinarios } = useVeterinariosStore()
const idVeterinario = ref<number>(0)

import useMascotasStore from '@/stores/mascotas_store'
const { mascotas } = toRefs(useMascotasStore())
const { getAll: getall_mascotas } = useMascotasStore()
const idMascota = ref<number>(0)

onMounted(async () => {
  try {
      await getall_mascotas()
      await getall_veterinarios()
    } catch (error) {
      mensaje.value = "Error al cargar las mascotas y/o veterinarios disponibles."
    }
})

async function nueva_atencion() {
  if (!newAtencion.value.fecha || !newAtencion.value.diagnostico || !newAtencion.value.tratamiento ||
      !idVeterinario || !idMascota) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error'
    return
  }
  newAtencion.value.mascota.id = idMascota.value
  newAtencion.value.veterinario.id = idVeterinario.value
  await saveEntidad(
    () => create(newAtencion.value),
  )
  if (estado.value==='exito') {
      newAtencion.value = { ...defaultAtencion }
      idMascota.value = 0
      idVeterinario.value = 0
  }
}

const today = computed(() => {
  const date = new Date()
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  
  return `${year}-${month}-${day}`
});
</script>

<template>
  <SaveViewGenerico
    titulo="Nueva Atención"
    :estado="estado" 
    :mensaje="mensaje" 
    :mostrarModal="mostrarModal"
    @volver="router.back()"
    @submit="nueva_atencion"
    @reset="newAtencion = { ...defaultAtencion }; idMascota=0; idVeterinario=0"
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
          v-model="newAtencion.fecha"
          style="width: 15ch;"
          autofocus
          required
          :max="today"/>
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
          v-model="newAtencion.diagnostico"
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
          v-model="newAtencion.tratamiento"
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
          v-model="newAtencion.observaciones"
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