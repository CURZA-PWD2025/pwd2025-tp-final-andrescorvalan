<script setup lang="ts">
  import { toRefs, onMounted, ref, computed } from 'vue'
  import { Icon } from "@iconify/vue"
  import useMascotasStore from '../../stores/mascotas_store'
  import { recargarBD } from '@/router'
  import type { Especie } from '@/interface/Especie'
  import type { Propietario } from '@/interface/Propietario'

  const { mascotas } = toRefs(useMascotasStore())
  const { getAll, destroy } = useMascotasStore()
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

  async function get_mascotas() {
    console.log("¿Debo recargar?:", recargarBD.value);
    console.log("Cantidad actual en store:", mascotas.value.length);
    if (!recargarBD.value && mascotas.value.length > 0) {
      console.log("CORTOCUITO: No recargo porque recargarBD es false");
      return
    }
    mensaje.value = 'Obteniendo el listado de mascotas.'
    estado.value = 'procesando'
    try {
      await getAll()
      if (mascotas.value.length > 0)
        mensaje.value = ''
      else
        mensaje.value = 'No se encontraron registros.'
      estado.value = 'exito'
      recargarBD.value = false
    } catch (error: any) {
      mensaje.value = `Error al cargar mascotas: ${error.message}`
      estado.value = 'error'
      recargarBD.value = true
    } finally {
      limpiarMensaje()
    }
  }

  onMounted(async () => {
    await get_mascotas()
  })

  async function refrescar() {
    recargarBD.value =true
    await get_mascotas()
  }

  async function ejecutarEliminar() {
    if (eliminar_id.value === null)
      return

    const id = eliminar_id.value
    eliminar_id.value = null
    mensaje.value = `Intentando eliminar la mascota con ID: ${id}.`
    estado.value = 'procesando'
    try {
      await destroy(id)    
      mensaje.value = `¡Éxito! Se ha eliminado la mascota con ID: ${id}.`
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
      <h2>Listado de Mascotas</h2>
      <div class="grud-botones">
        <button @click="refrescar" class="boton boton-refresh">
          <Icon class="icono" icon="mdi:refresh"/>
          Actualizar
        </button>
        <router-link class="boton boton-add" :to="{ name: 'mascotas_create' }">
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
    <div class="grud-list" v-if="mascotas.length > 0">        
      <article class="grud-list-item" v-for="mascota in mascotas" :key="mascota.id">
        <dl class="grud-field-name">ID:
          <span class="grud-data"> {{ mascota.id }}</span>
        </dl>
        <dl class="grud-field-name">Nombre:
          <span class="grud-data">{{ mascota.nombre }}</span>
        </dl>
        <dl class="grud-field-name">Propietario:
          <span class="grud-data">{{ mascota.propietario.apellido }}, {{ mascota.propietario.nombre }}</span>
        </dl>
        <div class="grud-botones">
          <router-link class="boton boton-show" :to="{ name: 'mascotas_show', params: { id: mascota.id } }">
            <Icon class="icono" icon="mdi:eye"/>
            Mostrar
          </router-link>
          <router-link class="boton boton-edit" :to="{ name: 'mascotas_update', params: { id: mascota.id } }">
            <Icon class="icono" icon="mdi:edit"/>
            Editar
          </router-link>
          <button class="boton boton-delete" @click.prevent="eliminar_id = (mascota.id as number)">
            <Icon class="icono" icon="mdi:delete"/>
            Eliminar
          </button>
        </div>
      </article>
    </div>
    <div v-else-if="estado !== 'procesando'" class="sin-registros">
      <p>No hay mascotas registradas. Haz clic en "Agregar" para crear una.</p>
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
            <p>¿Estás seguro que deseas eliminar la mascota con ID {{ eliminar_id }}?</p>
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