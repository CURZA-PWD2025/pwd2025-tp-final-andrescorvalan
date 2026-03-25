<script setup lang="ts">
  import { toRefs, onMounted, ref, computed } from 'vue'
  import { Icon } from "@iconify/vue"
  import { recargarBD } from '@/router'

  import ListViewGenerico from '@/components/crud-generico/ListViewGenerico.vue'
  import { useListLogicGenerico } from '@/components/crud-generico/ListLogicGenerico'
  const { mensaje, estado, idEliminar, identEliminar, borrando, mostrarModal, loadEntidades, prepararEliminar, delEntidad, resetListLogicGenerico } = useListLogicGenerico()

  import useEspecialidadesStore from '@/stores/especialidades_store'
  const { especialidades } = toRefs(useEspecialidadesStore())
  const { getAll, destroy } = useEspecialidadesStore()
  
  const filtro = ref('')
  const especialidadesFiltradas = computed(() => {
    const busqueda = filtro.value.toLowerCase().trim()
      if (!busqueda) return especialidades.value
      return especialidades.value.filter(p => 
        p.nombre.toLowerCase().includes(busqueda) || 
        p.descripcion.toLowerCase().includes(busqueda)
      )
  })

  async function inicializar() {
    // Se lee la base de datos solo si es necesario
    if (recargarBD.value || especialidades.value.length === 0) {
      especialidades.value = []
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
    titulo="Listado de especialidades"
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
          placeholder="Buscar por nombre o descripción." 
          class="input-busqueda"
        />
      </div>
    </template>

    <template #botonera>
      <router-link class="boton boton-add" :to="{ name: 'especialidades_create' }">
      <Icon class="icono" icon="mdi:add"/>
      Agregar
    </router-link>
    </template>

    <template #listado>
      <!-- listado -->
      <article class="crud-list-item" v-for="especialidad in especialidadesFiltradas" :key="especialidad.id">
        <dl class="crud-field-name">Nombre:
          <span class="crud-data">{{ especialidad.nombre }}</span>
        </dl>
        <dl class="crud-field-name">Estado:
          <span class="crud-data">{{ (especialidad.activa == 1)?'Activa':'No activa' }}</span>
        </dl>

        <div class="crud-botones">
          <router-link class="boton boton-show" :to="{ name: 'especialidades_show', params: { id: especialidad.id } }">
            <Icon class="icono" icon="mdi:eye"/>
            Mostrar
          </router-link>
          <router-link class="boton boton-edit" :to="{ name: 'especialidades_update', params: { id: especialidad.id } }">
            <Icon class="icono" icon="mdi:edit"/>
            Editar
          </router-link>
          <button class="boton boton-delete" 
            @click="prepararEliminar(
              especialidad.id as number,
              `la especialidad ${especialidad.nombre}`
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