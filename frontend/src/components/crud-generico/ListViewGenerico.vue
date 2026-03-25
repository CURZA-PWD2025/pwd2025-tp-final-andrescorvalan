<script setup lang="ts">
import { Icon } from "@iconify/vue"

// Props para recibir datos del padre
defineProps(['titulo', 'estado', 'borrando', 'mensaje', 'idEliminar', 'identEliminar','mostrarModal']);
// Emits para generar eventos para el padre
defineEmits(['refrescar', 'eliminar', 'cerrarModal']);
</script>

<template>
  <section class="crud">
    <header class="crud-encabezado">
      <h2>
        {{ titulo }}
      </h2>
      <div class="crud-controles">
        <slot name="buscador"></slot>
        <div class="crud-botones">
          <button @click="$emit('refrescar')" class="boton boton-refresh" :disabled="estado === 'leyendo'">
            <Icon class="icono" icon="mdi:refresh"/>
            Actualizar
          </button>
          <!-- Botones (Agregar...), Input para Buscar, etc - Definidos en list especificos-->
          <slot name="botonera"></slot> 
        </div>
      </div>
    </header>
    <!-- Mensajes (cargando datos: exito, no hay registros)-->
    <div class="crud-mensaje">
      <div v-if="estado==='cargando'" class="mensaje-alerta icono-procesando"></div>
      <transition  name="mensaje-fade" mode="out-in">
        <div v-if="estado==='cargaError'" :key="mensaje" role="alert" class="mensaje-alerta mensaje-error">
          {{ mensaje }}
        </div>
      </transition>  
       <transition  name="mensaje-fade" mode="out-in">
        <div v-if="estado==='cargaOk'" :key="mensaje" role="alert" class="mensaje-alerta mensaje-exito">
          {{ mensaje }}
        </div>
      </transition>  
    </div>
    <!-- Ventana para confirmar eliminacion y mostrar su resultado (exito, error) -->
    <div v-if="mostrarModal" class="deshabilitar-interaccion">
      <!-- Se presiono el boton eliminar -->
      <div v-if="idEliminar" >
        <div class="ventana-emergente">
          <!-- Se esta borrando -->
          <div v-if="borrando === true">
            <div class="icono-procesando"></div>
            {{ mensaje }}
          </div>
          <!-- Aun no se esta borrando, ventana de confirmacion -->
          <div v-else>
            <p>
              ¿Seguro que quieres eliminar {{ identEliminar }}?
            </p>
          </div>
          <!-- Botones Eliminar/borrando y Cancelar-->
          <div class="crud-botones">
            <button @click="$emit('eliminar')" :disabled="borrando" class="boton boton-delete">
              <span v-if="borrando">Borrando...</span>
              <span v-else>Sí, eliminar</span>
            </button>
            <button @click="$emit('cerrarModal')" :disabled="borrando" class="boton boton-cancel">
              Cancelar
            </button>
          </div>
        </div>
      </div>
      <div v-else>
        <!-- Se borro con exito -->
        <div v-if="estado === 'exito'" class="ventana-emergente ventana-emergente-exito">
          <Icon class="ventana-emergente-icono ventana-emergente-icono-exito" icon="mdi:check-circle"/>
          <h3>¡Excelente!</h3>
          <p>Se ha eliminado {{identEliminar}}.</p>
          <p class="mje-db">{{ mensaje }}</p>
          <button @click="$emit('cerrarModal')" class="boton boton-accept" style="width: 100%;" type="button">
            Entendido
          </button>
        </div>
        <!-- No se borro por algun error -->
        <div v-else-if="estado ==='error'" class="ventana-emergente ventana-emergente-error">
          <Icon class="ventana-emergente-icono ventana-emergente-icono-error" icon="mdi:close-circle"/>
          <h3>Hubo un problema</h3>
          <p>No se ha eliminado {{identEliminar}}.</p>
          <p class="mje-db">{{ mensaje }}</p>
          <button @click="$emit('cerrarModal')" class="boton boton-accept" style="width: 100%;" type="button">
            Entendido
          </button>
        </div>
      </div>
    </div>  
    <!-- Listado -->
    <div class="crud-list">        
      <slot name="listado"></slot><!-- El listado lo define el list especificos-->
    </div>
  </section> 
</template>

<style scoped>
  .crud-controles {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  :deep(.input-busqueda) {
    padding: 0.5rem;
    border-radius: 4px;
    border: 1px solid #ccc;
    width: 25ch;
  }

.mje-db {
  border: 1px solid gray;
  font-size: 0.7;
  color: gray;
  padding: 0.5rem;
}
</style>