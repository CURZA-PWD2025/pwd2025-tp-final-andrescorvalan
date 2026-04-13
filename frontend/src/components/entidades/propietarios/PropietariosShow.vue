| <script setup lang="ts">
  import { ref, toRefs, onMounted } from 'vue'
  
  import { useRoute, useRouter } from 'vue-router'
  const router = useRouter()
  const route = useRoute()

  import usePropietariosStore from '@/stores/propietarios_store'
  const { propietario } = toRefs(usePropietariosStore())
  const { buscar_propietario, defaultPropietario } = usePropietariosStore()

  import ShowViewGenerico from '@/components//crud-generico/ShowViewGenerico.vue'

  const mensajeError = ref('')

  onMounted(async () => {
    const id = Number(route.params.id)
    if (isNaN(id)) {
      router.push({ name: 'propietarios_list' })
      return
    }
    propietario.value = { ...defaultPropietario }
    try {
      await buscar_propietario(id)
    } catch (error: any) {
      mensajeError.value = error.mensaje || 'No se encontró el propietario.'
    }
  })
</script>

<template>
  <ShowViewGenerico
    titulo="Detalles del propietario"
    :mensaje="mensajeError" 
    @volver="router.push({ name: 'propietarios_list' })">
    <template #detalles v-if="propietario.id !== 0">
      <header class="ficha-encabezado">
        <icon-mdi-account-group class="ficha-logo" />
        <div>
          <h2>{{ propietario.nombre }} {{ propietario.apellido }} </h2>
          <p>ID: {{ propietario.id }}</p>
          <p>DNI: {{ propietario.dni }}</p>
          <p>Teléfono: {{ propietario.telefono }}</p>
          <p>Email: {{ propietario.email }}</p>
        </div>
      </header>
    </template>
  </ShowViewGenerico>
</template>

<style scoped>
</style>