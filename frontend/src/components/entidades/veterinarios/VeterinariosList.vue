
<script setup lang="ts">
  import { toRefs, onMounted, ref, computed } from 'vue'
  import { Icon } from "@iconify/vue"
  import { recargarBD } from '@/router'

  import ListViewGenerico from '@/components//crud-generico/ListViewGenerico.vue'
  import { useListLogicGenerico } from '@/components//crud-generico/ListLogicGenerico'
  const { mensaje, estado, idEliminar, identEliminar, borrando, mostrarModal, loadEntidades, prepararEliminar, delEntidad, resetListLogicGenerico } = useListLogicGenerico()

  import type { Especialidad } from '@/interface/especialidad'

  import useVeterinariosStore from '@/stores/veterinarios_store'
  const { veterinarios } = toRefs(useVeterinariosStore())
  const { getAll, destroy } = useVeterinariosStore()
  
  const filtro = ref('')
  const veterinariosFiltrados = computed(() => {
    const busqueda = filtro.value.toLowerCase().trim()
      if (!busqueda) return veterinarios.value
      return veterinarios.value.filter(p => 
        p.nombre.toLowerCase().includes(busqueda) || 
        p.apellido.toLowerCase().includes(busqueda) ||
        p.telefono.includes(busqueda) ||
        p.especialidades.some(e => (e as Especialidad).nombre.toLowerCase().includes(busqueda))
      )
  })

  async function inicializar() {
    // Se lee la base de datos solo si es necesario
    if (recargarBD.value || veterinarios.value.length === 0) {
      veterinarios.value = []
      await loadEntidades(getAll)
      recargarBD.value = false
    }
  }

  onMounted(async () => {
    await inicializar()
  })

  async function refrescar() {
    recargarBD.value =true
    await inicializar()
  }
  
  const ejecutarEliminar = () => {
    if (idEliminar.value) 
      delEntidad(idEliminar.value, destroy)
  }
</script>

<template>
  <ListViewGenerico
    titulo="Listado de veterinarios"
    :estado="estado" 
    :mensaje="mensaje" 
    :mostrarModal="mostrarModal"
    :borrando="borrando"
    :idEliminar="idEliminar"
    :identEliminar="identEliminar"

    @refrescar="refrescar"
    @eliminar="ejecutarEliminar"
    @cerrarModal="resetListLogicGenerico"
  >
    <template #buscador>
      <div class="buscador-wrapper">
        <Icon icon="mdi:magnify" class="icono-busqueda" />
        <input 
          v-model="filtro" 
          type="text" 
          placeholder="Buscar por nombre, apellido o matrícula." 
          class="input-busqueda"
        />
      </div>
    </template>

    <template #botonera>
      <router-link class="boton boton-add" :to="{ name: 'veterinarios_create' }">
      <Icon class="icono" icon="mdi:add"/>
      Agregar
    </router-link>
    </template>

    <template #listado>
      <!-- listado -->
      <article class="crud-list-item" v-for="veterinario in veterinariosFiltrados" :key="veterinario.id">
        <dl class="crud-field-name">Nombre:
          <span class="crud-data">{{ veterinario.nombre }}</span>
        </dl>
        <dl class="crud-field-name">Apellido:
          <span class="crud-data">{{ veterinario.apellido }}</span>
        </dl>
        <dl class="crud-field-name">Teléfono:
          <span class="crud-data">{{ veterinario.telefono }}</span>
        </dl>
        <dl class="crud-field-name">Especialidad:
          <span v-if="veterinario.especialidades.length > 0">
            {{ (veterinario.especialidades[0] as Especialidad).nombre }}
            <span v-if="veterinario.especialidades.length > 1" class="indicador-mas">
              (+{{ veterinario.especialidades.length - 1 }})
            </span>
          </span>
          <span v-else>
            Sin especialidades asignadas
          </span>
        </dl>
        <div class="crud-botones">
          <router-link class="boton boton-show" :to="{ name: 'veterinarios_show', params: { id: veterinario.id } }">
            <Icon class="icono" icon="mdi:eye"/>
            Mostrar
          </router-link>
          <router-link class="boton boton-edit" :to="{ name: 'veterinarios_update', params: { id: veterinario.id } }">
            <Icon class="icono" icon="mdi:edit"/>
            Editar
          </router-link>
          <button class="boton boton-delete" 
            @click="prepararEliminar(
              veterinario.id as number,
              `al veterinario/a ${veterinario.nombre} ${veterinario.apellido}`
            )"
          >
            <Icon class="icono" icon="mdi:delete"/>
            Eliminar
          </button>
        </div>
      </article>
    </template>
  </ListViewGenerico>
</template>

<style scoped>
</style>