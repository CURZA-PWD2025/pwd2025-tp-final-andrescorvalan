
<script setup lang="ts">
  import { useRouter } from 'vue-router'
  import { onMounted } from 'vue'

  const route = useRouter()

  onMounted(() => {
    route.push({ name: 'veterinarios_list' })
  })
</script>

<template>
  <h1>Administración de Veterinarios</h1>
  <router-view />
</template>

<style scoped></style>
