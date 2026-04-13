<script setup lang="ts">
  import { ref, toRefs, onMounted } from 'vue'
  
  import { useRoute, useRouter } from 'vue-router'
  const router = useRouter()
  const route = useRoute()

  import useEspecialidadesStore from '@/stores/especialidades_store'
  const { especialidad } = toRefs(useEspecialidadesStore())
  const { buscar_especialidad, defaultEspecialidad } = useEspecialidadesStore()

  import ShowViewGenerico from '@/components/crud-generico/ShowViewGenerico.vue'

  const mensajeError = ref('')

  onMounted(async () => {
    const id = Number(route.params.id)
    if (isNaN(id)) {
      router.push({ name: 'especialidades_list' })
      return
    }
    especialidad.value = { ...defaultEspecialidad }
    try {
      await buscar_especialidad(id)
    } catch (error: any) {
      mensajeError.value = error.mensaje || 'No se encontró la especialidad.'
    }
  })
</script>

<template>
  <ShowViewGenerico
    titulo="Detalles de la especialidad"
    :mensaje="mensajeError" 
    @volver="router.push({ name: 'especialidades_list' })">
    <template #detalles v-if="especialidad.id !== 0">
      <header class="ficha-encabezado">
        <icon-mdi-certificate class="ficha-logo" />
        <div>
          <h2>{{ especialidad.nombre }}</h2>
          <p>ID: {{ especialidad.id }}</p>
          <p>Estado: {{ (especialidad.activa == 1)?'Activa':'No activa' }}</p>
          <p>Descripción: {{ especialidad.descripcion }}</p>
        </div>
      </header>
    </template>
  </ShowViewGenerico>
</template>

<style scoped>  
</style>
