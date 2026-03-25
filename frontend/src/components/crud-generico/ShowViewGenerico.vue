<script setup lang="ts">
import { Icon } from "@iconify/vue"

// Props para recibir datos del padre
defineProps(['titulo', 'mensaje']);
// Emits para generar eventos para el padre
defineEmits(['volver', 'submit', 'reset', 'cerrarModal']);
</script>

<template>
  <section class="crud">
    <header class="crud-encabezado">
      <h2>
        {{ titulo }}
      </h2>
      <button @click="$emit('volver')" class="boton boton-back" type="button">
        <Icon class="icono" icon="mdi:arrow-left"/>
        Volver
      </button>
    </header>
    
    <!-- Mensajes (cargando datos: exito, no hay registros)-->
    <div class="crud-mensaje">
       <transition name="mensaje-fade" mode="out-in">
        <div v-if="mensaje" :key="mensaje" role="alert" class="mensaje-alerta mensaje-procesando">
          {{ mensaje }}
        </div>
      </transition>
    </div>
    <!-- Detalles -->
    <article class="ficha" >
      <slot name="detalles">
        <div class="crud-mensaje">
          <div class="mensaje-alerta icono-procesando"></div>
        </div>
      </slot> 
    </article>
  </section> 
</template>

<style scoped>
</style>