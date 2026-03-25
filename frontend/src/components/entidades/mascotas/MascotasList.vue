<script setup lang="ts">
  import { toRefs, onMounted, ref, computed } from 'vue'
  import { Icon } from "@iconify/vue"
  import { recargarBD } from '@/router'

  import AtencionesByMascota from '@/components/entidades/atenciones/AtencionesByMascota.vue'

  import ListViewGenerico from '@/components//crud-generico/ListViewGenerico.vue'
  import { useListLogicGenerico } from '@/components//crud-generico/ListLogicGenerico'
  const { mensaje, estado, idEliminar, identEliminar, borrando, mostrarModal, loadEntidades, prepararEliminar, delEntidad, resetListLogicGenerico } = useListLogicGenerico()

  import useMascotasStore from '@/stores/mascotas_store'
  const { mascotas } = toRefs(useMascotasStore())
  const { getAll, destroy } = useMascotasStore()

  const filtro = ref('')
  const mascotasFiltrados = computed(() => {
    const busqueda = filtro.value.toLowerCase().trim()
      if (!busqueda) return mascotas.value
      return mascotas.value.filter(p => 
        p.nombre.toLowerCase().includes(busqueda) || 
        p.propietario.apellido.toLowerCase().includes(busqueda) ||
        p.propietario.nombre.toString().includes(busqueda)
      )
  })

  async function inicializar() {
    // Se lee la base de datos solo si es necesario
    if (recargarBD.value || mascotas.value.length === 0) {
      mascotas.value = []
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
  
  const mostrarHistorial = ref(false)
  const idHistorial = ref<number | null>(null)
  
</script>

<template>
  <ListViewGenerico
    titulo="Listado de mascotas"
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
          placeholder="Buscar por nombre, propietario ..." 
          class="input-busqueda"
        />
      </div>
    </template>

    <template #botonera>
      <router-link class="boton boton-add" :to="{ name: 'mascotas_create' }">
      <Icon class="icono" icon="mdi:add"/>
      Agregar
    </router-link>
    </template>

    <template #listado>
      <div v-if="idHistorial" class="deshabilitar-interaccion">
         <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>Historia Clínica</h2>
            <button class="boton boton-close" @click="idHistorial = null">×</button>
          </div>
          <div class="modal-body">
            <AtencionesByMascota :mascotaId="idHistorial" />
          </div>
        </div>
      </div>

      <!-- listado -->
      <article class="crud-list-item" v-for="mascota in mascotasFiltrados" :key="mascota.id">
        <!-- <dl class="crud-field-name">ID:
          <span class="crud-data"> {{ mascota.id }}</span>
        </dl> -->
        <dl class="crud-field-name">Nombre:
          <span class="crud-data">{{ mascota.nombre }}</span>
        </dl>
        <dl class="crud-field-name">Propietario:
          <span class="crud-data">
            <!-- <router-link 
              :to="{ name: 'propietarios_show', params: { id: mascota.propietario.id } }"
              class="crud-link">
              {{ mascota.propietario.nombre }} {{ mascota.propietario.apellido }}
            </router-link> -->
            {{ mascota.propietario.nombre }} {{ mascota.propietario.apellido }}

          </span>
        </dl>
        <dl class="crud-field-name">Especie:
          <span class="crud-data">{{ mascota.especie.nombre }}</span>
        </dl>
        <button @click="idHistorial = (mascota.id as number); mostrarHistorial = true">
          Ver Historia Clínica
        </button>

        <div class="crud-botones">
          <router-link class="boton boton-show" :to="{ name: 'mascotas_show', params: { id: mascota.id } }">
            <Icon class="icono" icon="mdi:eye"/>
            Mostrar
          </router-link>
          <router-link class="boton boton-edit" :to="{ name: 'mascotas_update', params: { id: mascota.id } }">
            <Icon class="icono" icon="mdi:edit"/>
            Editar
          </router-link>
          <button class="boton boton-delete" 
          
            @click="prepararEliminar(
                mascota.id as number,
                `la mascota ${mascota.nombre} de ${mascota.propietario.nombre} ${mascota.propietario.apellido}`
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
  .modal-content {
    background: white;
    border-radius: 0.5rem;
    width: 90%;
    max-height: 85vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background-color: #f8f9fa;
    border-bottom: 2px solid #dee2e6;
    position: sticky;
    top: 0;
    z-index: 10;
  }
  .modal-body {
    padding: 1.5rem;
    overflow-y: auto;
    flex: 1;
  }
</style>