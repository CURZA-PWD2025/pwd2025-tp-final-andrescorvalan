<script setup lang="ts">
  import { toRefs, onMounted, ref, computed } from 'vue'
  import { Icon } from "@iconify/vue"
  import useEspeciesStore from '../../stores/especies_store'
  import { recargarBD } from '@/router'

  const { especies } = toRefs(useEspeciesStore())
  const { getAll, destroy } = useEspeciesStore()
  const eliminar_id = ref<number | null>(null)
  const mensaje = ref('')
  const estado = ref('')

  const tipoMensaje = computed(() => ({
    'mensaje-procesando': estado.value === 'procesando',
    'mensaje-exito': estado.value === 'exito',
    'mensaje-error': estado.value === 'error'
  }));

  const limpiarMensaje = (ms = 4000) => {
    setTimeout(() => {
      mensaje.value = ''
      estado.value = ''
    }, ms)
  }

  async function get_especies() {
    if (!recargarBD.value && especies.value.length > 0) 
      return
    mensaje.value = 'Obteniendo el listado de especies.'
    estado.value = 'procesando'
    try {
      await getAll()
      if (especies.value.length > 0)
        mensaje.value = ''
      else
        mensaje.value = 'No se encontraron registros.'
      estado.value = 'exito'
      recargarBD.value = false
    } catch (error: any) {
      mensaje.value = `Error al cargar especies: ${error.message}`
      estado.value = 'error'
      recargarBD.value = true
    } finally {
      limpiarMensaje()
    }
  }

  onMounted(async () => {
    await get_especies()
  })

  async function refrescar() {
    recargarBD.value =true
    await get_especies()
  }

  async function ejecutarEliminar() {
    if (eliminar_id.value === null)
      return

    const id = eliminar_id.value
    eliminar_id.value = null
    mensaje.value = `Intentando eliminar la especie con ID: ${id}.`
    estado.value = 'procesando'
    try {
      await destroy(id)    
      mensaje.value = `¡Éxito! Se ha eliminado la especie con ID: ${id}.`
      estado.value = 'exito'
    } catch (error: any) {
      mensaje.value = error.message.includes('404')
        ?'Error de conexión o el registro no existe.'
        :`No se pudo eliminar: ${error.message}`
      estado.value = 'error'
      eliminar_id.value = null
    } finally {
      limpiarMensaje()
    }
  }
</script>

<template>
  <section class="grud">
    <header class="grud-encabezado">
      <h2>Listado de Especies</h2>
      <div class="grud-botones">
        <button @click="refrescar" class="boton boton-refresh">
          <Icon class="icono" icon="mdi:refresh"/>
          Actualizar
        </button>
        <router-link class="boton boton-add" :to="{ name: 'especies_create' }">
          <Icon class="icono" icon="mdi:add"/>
          Agregar
        </router-link>
      </div>
    </header>
    <!-- Mensajes -->
    <div class="grud-mensaje">
      <transition name="mensaje-fade" mode="out-in">
        <div v-if="mensaje" :key="mensaje" role="alert" class="mensaje-alerta" :class="tipoMensaje">
          {{ mensaje }}
        </div>
      </transition>
    </div>  
    <!-- listado -->
    <div class="grud-list" v-if="especies.length > 0">
      <article class="grud-list-item" v-for="especie in especies" :key="especie.id">
        <dl class="grud-field-name">ID:
          <span class="grud-data"> {{ especie.id }}</span>
        </dl>
        <dl class="grud-field-name">Nombre Común:
          <span class="grud-data">{{ especie.nombre }}</span>
        </dl>
        <dl class="grud-field-name">Nombre Científico:
          <span class="grud-data">{{ especie.nombre_cientifico }}</span>
        </dl> 
        <div class="grud-botones">
          <router-link class="boton boton-show" :to="{ name: 'especies_show', params: { id: especie.id } }">
            <Icon class="icono" icon="mdi:eye"/>
            Mostrar
          </router-link>
          <router-link class="boton boton-edit" :to="{ name: 'especies_update', params: { id: especie.id } }">
            <Icon class="icono" icon="mdi:edit"/>
            Editar
          </router-link>
          <button class="boton boton-delete" @click="eliminar_id = (especie.id as number)">
            <Icon class="icono" icon="mdi:delete"/>
            Eliminar
          </button>
        </div>
      </article>
    </div>
    <div v-else-if="estado !== 'procesando'" class="sin-registros">
      <p>No hay especies registradas. Haz clic en "Agregar" para crear una.</p>
    </div>
    <!-- Solicitar confirmación -->
    <div v-if="eliminar_id" class="deshabilitar-interaccion">
      <div class="ventana-emergente">
        <!-- Mensaje de Procesamiento (Si se esta borrando) -->
        <div v-if="estado === 'procesando'">
            <div class="icono-procesando"></div>
            <p>Intentando borrar el registro con ID {{ eliminar_id }}...</p>
            <p>Esto puede tardar unos segundos.</p>
        </div>
        <!-- Mensaje de Confirmación (Si aun no se esta borrando) -->
        <div v-else>
            <p>¿Estás seguro que deseas eliminar la especie con ID {{ eliminar_id }}?</p>
            <div class="grud-botones">
                <button @click="ejecutarEliminar" class="boton boton-delete">Sí, Eliminar</button>
                <button @click="eliminar_id = 0" class="boton boton-cancel">Cancelar</button>
            </div>
        </div>
      </div>
    </div>
  </section> 
</template>

<style scoped>
</style>