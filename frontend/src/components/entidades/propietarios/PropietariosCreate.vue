<script setup lang="ts">
import { ref } from 'vue'

import { useRouter } from 'vue-router'
const router = useRouter()

import SaveViewGenerico from '@/components//crud-generico/SaveViewGenerico.vue'
import { useSaveLogicGenerico } from '@/components//crud-generico/SaveLogicGenerico'
const { mensaje, estado, mostrarModal, saveEntidad, resetSaveLogicGenerico } = useSaveLogicGenerico()

import usePropietariosStore from '@/stores/propietarios_store'
const { create, defaultPropietario } = usePropietariosStore()
const newPropietario = ref({ ...defaultPropietario })

async function nuevo_propietario() {
  if (!newPropietario.value.nombre || !newPropietario.value.apellido || !newPropietario.value.dni) {
    mensaje.value = 'Debe completar todos los campos obligatorios (*).'
    estado.value = 'error'
    return
  }

  await saveEntidad(
    () => create(newPropietario.value)
  )
  if (estado.value==='exito')
    newPropietario.value = { ...defaultPropietario }
}
</script>

<template>
  <SaveViewGenerico
    titulo="Nuevo propietario"
    :estado="estado" 
    :mensaje="mensaje" 
    :mostrarModal="mostrarModal"
    @volver="router.push({name: 'propietarios_list'})"
    @submit="nuevo_propietario"
    @reset="newPropietario = { ...defaultPropietario }"
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
          v-model="newPropietario.nombre"
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
          v-model="newPropietario.apellido"
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
          v-model="newPropietario.dni"
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
          <!-- <abbr class="crud-abbr" 
            title="Teléfono del propietario (obligatorio)">*
          </abbr> -->
        </label>
        <input class="crud-input crud-data"
          id="telefono"
          type="tel"
          v-model="newPropietario.telefono"
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
          <!-- <abbr class="crud-abbr" 
            title="Email del propietario (obligatorio)">*
          </abbr> -->
        </label>
        <input class="crud-input crud-data"
          id="email"
          type="email"
          v-model="newPropietario.email"
          placeholder="Ej: juan@ejemplo.com"
          maxlength="100"
          style="width: 42ch;"
          />
      </div>
    </div>
  </SaveViewGenerico>   
</template>

<style scoped>
</style>