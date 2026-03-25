<script setup lang="ts">
  import { toRefs, onMounted, ref, computed } from 'vue'
  import { Icon } from "@iconify/vue"
  import { recargarBD } from '@/router'

  import ListViewGenerico from '@/components/crud-generico/ListViewGenerico.vue'
  import { useListLogicGenerico } from '@/components/crud-generico/ListLogicGenerico'
  const { mensaje, estado, idEliminar, identEliminar, borrando, mostrarModal, loadEntidades, prepararEliminar, delEntidad, resetListLogicGenerico } = useListLogicGenerico()

  import useEspeciesStore from '@/stores/especies_store'
  const { especies } = toRefs(useEspeciesStore())
  const { getAll, destroy } = useEspeciesStore()
  
  const filtro = ref('')
  const especiesFiltradas = computed(() => {
    const busqueda = filtro.value.toLowerCase().trim()
      if (!busqueda) return especies.value
      return especies.value.filter(p => 
        p.nombre.toLowerCase().includes(busqueda) || 
        p.nombre_cientifico.toLowerCase().includes(busqueda) ||
        p.clase.toLowerCase().includes(busqueda)
      )
  })

  async function inicializar() {
    // Se lee la base de datos solo si es necesario
    if (recargarBD.value || especies.value.length === 0) {
      especies.value = []
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
    titulo="Listado de especies"
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
          placeholder="Buscar por nombre, clase o nombre científico." 
          class="input-busqueda"
        />
      </div>
    </template>

    <template #botonera>
      <router-link class="boton boton-add" :to="{ name: 'especies_create' }">
      <Icon class="icono" icon="mdi:add"/>
      Agregar
    </router-link>
    </template>

    <template #listado>
      <!-- listado -->
      <article class="crud-list-item" v-for="especie in especiesFiltradas" :key="especie.id">
        <dl class="crud-field-name">Nombre Común:
          <span class="crud-data">{{ especie.nombre }}</span>
        </dl>
        <dl class="crud-field-name">Nombre Científico:
          <span class="crud-data">{{ especie.nombre_cientifico }}</span>
        </dl>
        <dl class="crud-field-name">Clase:
          <span class="crud-data"> {{ especie.clase }}</span>
        </dl>
        <div class="crud-botones">
          <router-link class="boton boton-show" :to="{ name: 'especies_show', params: { id: especie.id } }">
            <Icon class="icono" icon="mdi:eye"/>
            Mostrar
          </router-link>
          <router-link class="boton boton-edit" :to="{ name: 'especies_update', params: { id: especie.id } }">
            <Icon class="icono" icon="mdi:edit"/>
            Editar
          </router-link>
          <button class="boton boton-delete" 
            @click="prepararEliminar(
              especie.id as number,
              `la especie ${especie.nombre}`
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