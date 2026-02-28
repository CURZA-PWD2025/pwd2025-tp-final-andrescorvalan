<script setup lang="ts">
  import { toRefs, onMounted } from 'vue'
  import { Icon } from "@iconify/vue"
  import useVeterinariosStore from '../../stores/veterinarios_store'
  import { useRoute, useRouter } from 'vue-router'
  import type { Especialidad } from '@/interface/Especialidad'

  const router = useRouter()
  const route = useRoute()
  const { veterinario } = toRefs(useVeterinariosStore())
  const { buscar_veterinario } = useVeterinariosStore()

  function go_veterinarios_list() {
      router.push({ name: 'veterinarios_list' })
  }

  onMounted(async () => {
    const id = Number(route.params.id)
    if (isNaN(id)) {
      router.push({ name: 'veterinarios_list' })
      return
    }
    veterinario.value.id=0
    //setTimeout(async () => { await buscar_veterinario(id) }, 2000)
    await buscar_veterinario(id)
  })
</script>

<template>
  <section class="grud">
    <header class="grud-encabezado">
      <h2>Detalles del Veterinario</h2>
      <button @click="go_veterinarios_list" class="boton boton-back">
        <Icon class="icono" icon="mdi:arrow-left"/>
        Volver al Listado
      </button>
    </header>
    <article class="grud-frame" v-if="veterinario.id !== 0">
      <dl class="grud-field-name">ID:
        <span class="grud-data"> {{ veterinario.id }}</span>
      </dl>
      <dl class="grud-field-name">Nombre:
        <span class="grud-data">{{ veterinario.nombre }}</span>
      </dl>
      <dl class="grud-field-name">Apellido:
        <span class="grud-data">{{ veterinario.apellido }}</span>
      </dl>
      <dl class="grud-field-name">Matricula:
        <span class="grud-data">{{ veterinario.matricula }}</span>
      </dl>
      <dl class="grud-field-name">Teléfono:
        <span class="grud-data">{{ veterinario.telefono }}</span>
      </dl>
      <dl class="grud-field-name">Email:
        <span class="grud-data">{{ veterinario.email }}</span>
      </dl>
      <dl class="grud-field-name">Especialidades:
        <span v-if="veterinario.especialidades.length > 0">
          {{ (veterinario.especialidades as Especialidad[]).map(e => e.nombre).join(', ') }}
        </span>
        <span v-else>
          Sin especialidades asignadas
        </span>
      </dl>
    </article>
    <div v-else class="grud-mensaje">
      <transition name="mensaje-fade" mode="out-in">
        <div role="alert" class="mensaje-alerta mensaje-procesando">
          <Icon class="icono-carga" icon="line-md:loading-twotone-loop" />
          Buscando información del veterinario...
        </div>
      </transition>
    </div>
  </section> 
</template>

<style scoped>
</style>
