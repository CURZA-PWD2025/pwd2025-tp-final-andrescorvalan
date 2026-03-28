<script setup lang="ts">
  import { toRefs, onMounted, ref, computed } from 'vue'
  import { Icon } from "@iconify/vue"
  import { recargarBD } from '@/router'

  import ListViewGenerico from '@/components//crud-generico/ListViewGenerico.vue'
  import { useListLogicGenerico } from '@/components//crud-generico/ListLogicGenerico'
  const { mensaje, estado, idEliminar, identEliminar, borrando, mostrarModal, loadEntidades, prepararEliminar, delEntidad, resetListLogicGenerico } = useListLogicGenerico()

  import usePropietariosStore from '@/stores/propietarios_store'
  const { propietarios } = toRefs(usePropietariosStore())
  const { getAll, destroy } = usePropietariosStore()

  const filtro = ref('')
  const propietariosFiltrados = computed(() => {
    const busqueda = filtro.value.toLowerCase().trim()
      if (!busqueda) return propietarios.value

      return propietarios.value.filter(p => 
        p.nombre.toLowerCase().includes(busqueda) || 
        p.apellido.toLowerCase().includes(busqueda) ||
        p.telefono.includes(busqueda)
      )
  })

  async function inicializar() {
    // Se lee la base de datos solo si es necesario
    if (recargarBD.value || propietarios.value.length === 0) {
      propietarios.value = []
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
    titulo="Listado de propietarios"
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
          placeholder="Nombre, apellido o teléfono  ." 
          class="input-busqueda"
        />
      </div>
    </template>

    <template #botonera>
      <router-link class="boton boton-add" :to="{ name: 'propietarios_create' }">
      <Icon class="icono" icon="mdi:add"/>
      Agregar
    </router-link>
    </template>

    <template #listado>
      <article class="crud-list-item" v-for="propietario in propietariosFiltrados" :key="propietario.id">
        <dl class="crud-field-name">Nombre:
          <span class="crud-data">{{ propietario.nombre }}</span>
        </dl>
        <dl class="crud-field-name">Apellido:
          <span class="crud-data">{{ propietario.apellido }}</span>
        </dl>
        <dl class="crud-field-name">Teléfono:
          <span class="crud-data">{{ propietario.telefono }}</span>
        </dl>
        <div class="crud-botones">
          <router-link class="boton boton-show" :to="{ name: 'propietarios_show', params: { id: propietario.id } }">
            <Icon class="icono" icon="mdi:eye"/>
            Mostrar
          </router-link>
          <router-link class="boton boton-edit" :to="{ name: 'propietarios_update', params: { id: propietario.id } }">
            <Icon class="icono" icon="mdi:edit"/>
            Editar
          </router-link>
          
          <button class="boton boton-delete" 
            @click="prepararEliminar(
                propietario.id as number,
              `al propietario/a ${propietario.nombre} ${propietario.apellido}`
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