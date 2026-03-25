| <script setup lang="ts">
  import { ref, toRefs, onMounted } from 'vue'
  import { Icon } from "@iconify/vue"
  
  import { useRoute, useRouter } from 'vue-router'
  const router = useRouter()
  const route = useRoute()

  import useVeterinariosStore from '@/stores/veterinarios_store'
  const { veterinario } = toRefs(useVeterinariosStore())
  const { buscar_veterinario, defaultVeterinario } = useVeterinariosStore()

  import type { Especialidad } from '@/interface/especialidad'

  import ShowViewGenerico from '@/components/crud-generico/ShowViewGenerico.vue'

  const mensajeError = ref('')

  onMounted(async () => {
    const id = Number(route.params.id)
    if (isNaN(id)) {
      router.push({ name: 'veterinarios_list' })
      return
    }
    veterinario.value = { ...defaultVeterinario }
    try {
      await buscar_veterinario(id)
    } catch (error: any) {
      mensajeError.value = error.mensaje || 'No se encontró el veterinario.'
    }
  })
</script>

<template>
  <ShowViewGenerico
    titulo="Detalles del veterinario"
    :mensaje="mensajeError" 
    @volver="router.push({ name: 'veterinarios_list' })">
    <template #detalles v-if="veterinario.id !== 0">
      <header class="ficha-encabezado">
        <Icon icon="mdi:doctor" class="ficha-logo" />
        <div>
          <h2>{{ veterinario.nombre }} {{ veterinario.apellido }} </h2>
          <p>ID: {{ veterinario.id }}</p>
          <p>Matricula: {{ veterinario.matricula }}</p>
          <p>Teléfono: {{ veterinario.telefono }}</p>
          <p>Email: {{ veterinario.email }}</p>
          <p v-if="veterinario.especialidades.length > 0">
            Especialidades: {{ (veterinario.especialidades as Especialidad[]).map(e => e.nombre).join(', ') }}
          </p>
          <p v-else>
            Especialidades: Sin especialidades asignadas
          </p>
        </div>
      </header>
    </template>
  </ShowViewGenerico>
</template>

<style scoped>
</style>