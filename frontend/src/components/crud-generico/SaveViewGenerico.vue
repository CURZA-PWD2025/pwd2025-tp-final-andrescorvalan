<script setup lang="ts">
import { Icon } from "@iconify/vue"

// Props para recibir datos del padre
defineProps(['titulo', 'estado', 'mensaje', 'mostrarModal']);
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
    <!-- Ventana para mostrar un mensaje de procesamiento y su resultado (exito, error) -->
    <div v-if="mostrarModal" class="deshabilitar-interaccion">
      <div class="ventana-emergente" :class="estado === 'exito' ? 'ventana-emergente-exito' : 'ventana-emergente-error'">
        <Icon class="ventana-emergente-icono"
          :class="estado === 'exito' ? 'ventana-emergente-icono-exito' : 'ventana-emergente-icono-error'"
          :icon="estado === 'exito' ? 'mdi:check-circle' : 'mdi:alert-circle'" 
        />
        <h3>{{ estado === 'exito' ? '¡Excelente!' : 'Hubo un problema' }}</h3>
        <p>{{ mensaje }}</p>
        <button @click="$emit('cerrarModal')" class="boton boton-accept" style="width: 100%;" type="button">
          Entendido
        </button>
      </div>
    </div>

    <div v-if="estado === 'procesando'" class="deshabilitar-interaccion">
      <div class="ventana-emergente">
        <div class="icono-procesando"></div>
        <p>Procesando solicitud...</p>
      </div>
    </div>

    <form @submit.prevent="$emit('submit')" class="crud-frame">
      <!-- Slot para los campos del formulario -->
      <slot></slot>
      <!-- Botones del formulario -->
      <div class="crud-botones">
        <button class="boton boton-accept" type="submit" :disabled="estado === 'procesando'">
          <Icon class="icono" icon="mdi:content-save-plus"/>
          <p v-if="estado === 'procesando'">
            'Guardando...'
          </p>
          <p v-else>
            Grabar
          </p>
        </button>
        <button class="boton boton-reset" type="button" @click="$emit('reset')" :disabled="estado === 'procesando'">
          <Icon class="icono" icon="mdi:broom"/>
          Anular
        </button>
      </div>
    </form>
  </section>
</template>

<style scoped>
</style>