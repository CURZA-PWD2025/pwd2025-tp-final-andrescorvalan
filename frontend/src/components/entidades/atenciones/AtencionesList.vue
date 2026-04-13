<script setup lang="ts">
  import { toRefs, onMounted, ref, computed } from 'vue'
  import { recargarBD } from '@/router'

  import ListViewGenerico from '@/components//crud-generico/ListViewGenerico.vue'
  import { useListLogicGenerico } from '@/components//crud-generico/ListLogicGenerico'
  const { mensaje, estado, idEliminar, identEliminar, borrando, mostrarModal, loadEntidades, prepararEliminar, delEntidad, resetListLogicGenerico } = useListLogicGenerico()

  import useAtencionesStore from '@/stores/atenciones_store'
  const { atenciones } = toRefs(useAtencionesStore())
  const { getAll, destroy } = useAtencionesStore()

  const filtro = ref('')
  const atencionesFiltrados = computed(() => {
    const busqueda = filtro.value.toLowerCase().trim()
      if (!busqueda) return atenciones.value

      return atenciones.value.filter(p => 
        p.fecha.includes(busqueda) || 
        p.veterinario.apellido.toLowerCase().includes(busqueda) ||
        p.veterinario.nombre.toLowerCase().includes(busqueda) ||
        p.diagnostico.toLowerCase().includes(busqueda) ||
        p.mascota.nombre.toLowerCase().includes(busqueda) ||
        p.mascota.propietario.apellido.toLowerCase().includes(busqueda) ||
        p.mascota.propietario.nombre.toLowerCase().includes(busqueda)
      )
  })

  async function inicializar() {
    // Se lee la base de datos solo si es necesario
    if (recargarBD.value || atenciones.value.length === 0) {
      atenciones.value = []
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

  const formatearFecha = (fechaStr: string) => {
    const date = new Date(fechaStr + 'T00:00:00')
    return date.toLocaleDateString('es-AR', {day: '2-digit', month: '2-digit', year: 'numeric'});
  }
</script>

<template>
  <ListViewGenerico
    titulo="Listado de atenciones"
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
        <icon-mdi-magnify class="icono-busqueda"/>
        <input 
          v-model="filtro" 
          type="text" 
          placeholder="Buscar por nombre, propietario ..." 
          class="input-busqueda"
          title="Buscar por fecha, nombre de mascota, nombre o apellido del propietario, nombre o apellido del veterinario o diagnóstico"
        />
      </div>
    </template>

    <template #botonera>
      <router-link class="boton boton-add" :to="{ name: 'atenciones_create' }">
      <icon-mdi-add class="icono"/>
      Agregar
    </router-link>
    </template>

    <template #listado>
      <!-- listado -->
      <article class="crud-list-item" v-for="atencion in atencionesFiltrados" :key="atencion.id">
        <dl class="crud-field-name">Fecha:
          <span class="crud-data"> {{ formatearFecha(atencion.fecha) }}</span>
        </dl>
        <dl class="crud-field-name">Nombre de la mascota:
          <span class="crud-data">
              {{ atencion.mascota.nombre }}
          </span>
        </dl>
        <dl class="crud-field-name">Propietario:
              <span class="crud-data">
              {{ atencion.mascota.propietario.apellido }}, {{ atencion.mascota.propietario.nombre }}
              </span>
        </dl>
        <dl class="crud-field-name">Veterinario:
          <span class="crud-data">{{ atencion.veterinario.apellido }}, {{ atencion.veterinario.nombre }}</span>
        </dl>
        <dl class="crud-field-name">Diagnóstico:
          <span class="crud-data">{{ atencion.diagnostico }}</span>
        </dl>
    
        <div class="crud-botones">
          <router-link class="boton boton-show" :to="{ name: 'atenciones_show', params: { id: atencion.id } }">
            <icon-mdi-eye class="icono"/>
            Mostrar
          </router-link>
          <router-link class="boton boton-edit" :to="{ name: 'atenciones_update', params: { id: atencion.id } }">
            <icon-mdi-edit class="icono"/>
            Editar
          </router-link>
          <button class="boton boton-delete" 
            @click="prepararEliminar(
              atencion.id as number,
              `la atención de ${atencion.mascota.nombre} del dia ${formatearFecha(atencion.fecha)}`
              )"
          >
            <icon-mdi-delete class="icono"/>
            Eliminar
          </button>
        </div>
      </article>
    </template>
  </ListViewGenerico>
</template>

<style scoped>
</style>