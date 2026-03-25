<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { useRoute, useRouter } from 'vue-router'
const router = useRouter()
const route = useRoute()

import SaveFormGenerico from '@/components//crud-generico/SaveViewGenerico.vue'
import { useSaveLogicGenerico } from '@/components//crud-generico/SaveLogicGenerico'
const { mensaje, estado, mostrarModal, saveEntidad, findEntidad, resetSaveLogicGenerico } = useSaveLogicGenerico()

import usePropietariosStore from '@/stores/propietarios_store'
const { buscar_propietario, update, defaultPropietario } = usePropietariosStore()
const editPropietario = ref({ ...defaultPropietario })

async function cargar_datos () {
  const id = Number(route.params.id)
  const datos = await findEntidad(id, buscar_propietario)
  if (datos) {
      editPropietario.value = { ...datos }
  }
}

onMounted(async () => {
  cargar_datos()
})

async function modificar_propietario() {
  if (!editPropietario.value.nombre || !editPropietario.value.apellido || !editPropietario.value.dni) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error' 
    return
  }
  await saveEntidad(() => update(editPropietario.value))
}
</script>

<template>
  <SaveFormGenerico
    titulo="Actualizar propietario"
    :estado="estado" 
    :mensaje="mensaje" 
    :mostrarModal="mostrarModal"
    @volver="router.push({name: 'propietarios_list'})"
    @submit="modificar_propietario"
    @reset="cargar_datos"
    @cerrarModal="resetSaveLogicGenerico"
  >
    <div class="crud-field-group">
      <div class="crud-field">
        <label class="crud-field-name" for="nombre">
          Nombre: 
          <abbr class="crud-abbr" 
            title="Nombre del propietario (obligatorio)">*
          </abbr>
        </label>
        <input class="crud-input crud-data"
          id="nombre"
          type="text"
          v-model="editPropietario.nombre"
          placeholder="Ej: Juan"
          maxlength="35"
          style="width: 42ch;"
          autofocus
          required/>
      </div>
      <div class="crud-field">
        <label class="crud-field-name" for="apellido">
          Apellido: 
          <abbr class="crud-abbr" 
            title="Apellido del propietario (obligatorio)">*
          </abbr>
        </label>
        <input class="crud-input crud-data"
          id="apellido"
          type="text"
          v-model="editPropietario.apellido"
          placeholder="Ej: Garcia"
          maxlength="35"
          style="width: 42ch;"
          required/>
      </div>
      <div class="crud-field">
        <label class="crud-field-name" for="dni">
          DNI: 
          <abbr class="crud-abbr" 
            title="DNI del propietario (obligatorio)">*
          </abbr>
        </label>
        <input class="crud-input crud-data"
          id="dni"
          type="numeric"
          pattern="[0-9]*"
          v-model="editPropietario.dni"
          placeholder="Ej: 12345678"
          maxlength="10"
          minlength="7"
          style="width: 12ch;"
          required/>
      </div>
    </div>      
    <div class="crud-field-group">
      <div class="crud-field">
        <label class="crud-field-name" for="telefono">
          Teléfono:
        </label>
        <input class="crud-input crud-data"
          id="telefono"
          type="tel"
          v-model="editPropietario.telefono"
          placeholder="Cod. Área + Número (ej: 2991234567)"
          minlength="10"
          maxlength="15"
          style="width: 42ch;"
          pattern="[0-9+ ]{10,15}"
          title="Ingrese 10 dígitos (ej: 2991234567). Puede incluir +54"
          />
      </div>
      <div class="crud-field">
        <label class="crud-field-name" for="email">
          Email:
        </label>
        <input class="crud-input crud-data"
          id="email"
          type="email"
          v-model="editPropietario.email"
          placeholder="Ej: juan@ejemplo.com"
          maxlength="100"
          style="width: 42ch;"
          />
      </div>
    </div>
  </SaveFormGenerico>
</template>

<style scoped>
</style>