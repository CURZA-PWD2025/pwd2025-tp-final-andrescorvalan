| <script setup lang="ts">
  import { ref, toRefs, onMounted } from 'vue'

  import { useRoute, useRouter } from 'vue-router'
  const router = useRouter()
  const route = useRoute()

  import useEspeciesStore from '@/stores/especies_store'
  const { especie } = toRefs(useEspeciesStore())
  const { buscar_especie, defaultEspecie } = useEspeciesStore()

  import ShowViewGenerico from '@/components/crud-generico/ShowViewGenerico.vue'

  const mensajeError = ref('')

  onMounted(async () => {
    const id = Number(route.params.id)
    if (isNaN(id)) {
      router.push({ name: 'especies_list' })
      return
    }
    especie.value = { ...defaultEspecie }
    try {
      await buscar_especie(id)
    } catch (error: any) {
      mensajeError.value = error.mensaje || 'No se encontró la especie.'
    }
  })
</script>

<template>
  <ShowViewGenerico
  titulo="Detalles de la especie"
  :mensaje="mensajeError" 
  @volver="router.push({ name: 'especies_list' })">
    <template #detalles v-if="especie.id !== 0">
      <header class="ficha-encabezado">
        <icon-mdi-cat class="ficha-logo"/>
        <div>
          <h2>{{ especie.nombre }}</h2>
          <p>ID: {{ especie.id }}</p>
          <p>Nombre Científico: {{ especie.nombre_cientifico }}</p>
          <p>Clase: {{ especie.clase }}</p>
          <p>Esperanza de vida promedio: {{ especie.esperanza_vida }}</p>
          <p>Es exótica: {{ (especie.exotica == 1)?' Si':' No' }}</p>
        </div>
      </header>
    </template>
  </ShowViewGenerico>
</template>

<style scoped>
</style>